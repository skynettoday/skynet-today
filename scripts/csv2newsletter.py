import os
import argparse
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

import pandas as pd
import inflect
import json

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from llm_utils import query_llm_simple, web_fetch_article_summary, MODEL_OPUS, MODEL_SONNET, MODEL_HAIKU
from verify_summary import verify_summary
from content_retrieval import get_arxiv_paper_contents

# Constants for text limits
MAX_ARTICLE_WORDS = 10000
CATEGORY_TEXT_PREVIEW_LENGTH = 500
EXCERPT_MAX_TOKENS = 100
SUMMARY_MAX_TOKENS = 4000
RANKING_MAX_TOKENS = 400
NEWSLETTER_EXCERPT_MAX_TOKENS = 256

CATEGORIES = [
    'Top News',
    'Tools',
    'Business',
    'Policy',
    'Concerns',
    'Analysis',
    'Expert Opinions',
    'Explainers',
    'Fun',
    'Research'
]


def label_from_url(url):
    """Readable label for a source whose title could not be fetched (paywalled/blocked).

    Turns .../2026/09/09/newsom-signs-ai-safety-bills-backed-by-anthropic-openai-01069928
    into "Newsom signs ai safety bills backed by anthropic openai" — better than printing
    the bare URL as the link text.
    """
    slug = clean_url(url).rstrip('/').split('/')[-1]
    slug = re.sub(r'\.(html?|php|aspx)$', '', slug)
    slug = re.sub(r'[-_]?\d{5,}$', '', slug)           # trailing story IDs
    words = [w for w in re.split(r'[-_]+', slug) if w and not w.isdigit()]
    if len(words) < 2:
        return clean_url(url)
    caps = {'ai': 'AI', 'openai': 'OpenAI', 'us': 'US', 'eu': 'EU', 'uk': 'UK',
            'gpt': 'GPT', 'llm': 'LLM', 'ceo': 'CEO', 'nyu': 'NYU', 'pypi': 'PyPI'}
    words = [caps.get(w.lower(), w) for w in words]
    label = ' '.join(words)
    return label[:1].upper() + label[1:]


def cell(row, key):
    """Read a CSV cell as a stripped string. Blank cells arrive from pandas as NaN."""
    val = row.get(key) if hasattr(row, 'get') else None
    return val.strip() if isinstance(val, str) else ''


def clean_url(url):
    """Remove query parameters from URL."""
    if '?' in url:
        return url.split('?')[0]
    return url


def apply_map_batch(func, args_list):
    """Execute function calls in parallel using ThreadPoolExecutor."""
    results = [None] * len(args_list)

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        future_to_idx = {executor.submit(func, *args): idx for idx, args in enumerate(args_list)}

        with tqdm(total=len(args_list)) as pbar:
            for future in as_completed(future_to_idx):
                idx = future_to_idx[future]
                results[idx] = future.result()
                pbar.update(1)

    return results


def get_article_category(row, article_text):
    # Any non-empty mark in the 'Top News?' column (an 'x' by convention) makes it a headline story.
    if cell(row, 'Top News?'):
        return 'Top News'

    # Legacy CSVs carried the category, or related URLs, in a 'Type' column.
    type_val = cell(row, 'Type')
    if type_val:
        if type_val in CATEGORIES:
            return type_val
        if type_val.startswith('http'):
            return 'Top News'

    title, url = row['Name'], row['URL']
    if 'arxiv' in url:
        return 'Research'

    # Use first N characters of article text if available, otherwise just title and URL
    text_preview = article_text[:CATEGORY_TEXT_PREVIEW_LENGTH] if article_text else "No text available"

    prompt = f'''
Title: {title}
Text Preview: {text_preview}
Link: {url}
'''.strip()

    system_prompt = '''
Your task is to classify articles about AI into one of the following types:
Business: Anything related to investments, funding, VCs, company updates, or market trends.
Research: Scientific studies, research in AI, or applying AI to do science in various fields. All links from arxiv and huggingface belong to Research.
Tools: New feature releases, product announcements; new AI software, tools, and applications of AI.
Concerns: Discussions and news about problems, harms, and any alarming things about AI, including govermnet investigations about AI.
Policy: News, analysis, and opinions related to government policies.
Analysis: Analyzes an existing topic about AI that's not the above topics (not news).
Expert Opinions: Opinion pieces from experts and not factual reporting. If it's not clear the opinion piece is from a domain expert, then it should be in Analysis.
Explainers: Explains a given topic in AI with the goal to educate the reader; tutorials, guides.
Fun: Anything silly, fun, and doesn't belong to the other types.

The user will provide the article title, link, and text preview.
After careful consideration, you will respond with ONLY the predicted article type, with no explanations, punctuation, formatting, or anything else.
Only respond with one of the above types (Business, Research, Tools, Concerns, Policy, Analysis, Expert Opinions, Explainers, Fun).
'''.strip()
    return query_llm_simple(
        system_prompt,
        prompt,
        model=MODEL_HAIKU,
        max_tokens=EXCERPT_MAX_TOKENS,
        debug_label=f"CATEGORY for {title[:30]}"
    )


def get_news_article(url, title=None):
    if 'arxiv' in url:
        text = get_arxiv_paper_contents(url)
        if text:
            return {
                'text': text,
                'top_image': None,
                'has_top_image': False
            }

    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.text:
            return {
                'title': article.title,
                'text': article.text,
                'top_image': article.top_image,
                'has_top_image': article.has_top_image()
            }
    except Exception as e:
        print(f'  newspaper download error for {url}: {e}')

    # Fallback: use web_fetch to get a detailed summary of the story
    try:
        text = web_fetch_article_summary(url, title=title)
        if text:
            return {
                'text': text,
                'top_image': None,
                'has_top_image': False
            }
    except Exception as e:
        print(f'  web_fetch fallback also failed for {url}: {e}')

    return None


def clip_text_words(text, max_words=MAX_ARTICLE_WORDS):
    """Clip text to maximum number of words."""
    words = text.split(" ")
    if len(words) > max_words:
        text = " ".join(words[:max_words])
    return text


def get_article_excerpt(row, article):
    if not article:
        return None
    system_prompt = '''
Given the title, subtitle, and text of an article about AI, write a short one sentence summary of its content that works as a continuation of the title.

**IMPORTANT** the summary:
* should be exactly one sentence long.
* should only have information not already provided in the title of the article.
* should not start with 'Summary: ' ; just output the content.
* should avoid 'marketing hype' (terms like 'revolutionizes' , 'groundbreaking', 'advanced' etc.) -- stick to the facts
* should work as a follow up sentence that follows the article title.
* should try to vary the opening words to not be repetitive
* Should be concise and to the point rather than overly detailed.

Examples:
* 'Google is testing a vibe-coding app called Opal' -> 'The app allows users to create and share mini web apps using text prompts and a visual workflow, aiming to make app development accessible to non-technical users.'
* 'GitHub Goes After Vibe Coding Fans with the Public Preview of GitHub Spark' -> 'Spark allows users to create full-stack apps from natural language prompts, and is available to Copilot Pro+ subscribers for $39 a month.'
'''.strip()

    prompt = f'''
Title: {row['Name']}
Text: {clip_text_words(article["text"])}
'''.strip()
    return query_llm_simple(
        system_prompt,
        prompt,
        model=MODEL_HAIKU,
        max_tokens=EXCERPT_MAX_TOKENS,
        debug_label=f"EXCERPT for {row['Name'][:30]}"
    )


def get_output_file_name(digest_number):
    """Generate output filename based on closest Monday and digest number."""
    today = date.today()

    # Calculate the difference between today and the most recent Monday
    delta_to_monday = {
        0: 0,
        1: -1,
        2: -2,
        3: -3,
        4: 3,
        5: 2,
        6: 1
    }[today.weekday()]
    closest_monday = today + timedelta(days=delta_to_monday)

    # Format the date as YYYY-MM-DD
    formatted_date = closest_monday.strftime("%Y-%m-%d")

    return f'{formatted_date}-{digest_number}.md'


def get_article_summary(title, news_article, related_articles=None):
    if not news_article:
        return ':/'

    # Determine if we have multiple articles to summarize
    has_related = related_articles and len(related_articles) > 0

    if has_related:
        system_prompt = '''
You are an expert writer and commentator hired to write summaries of articles for the newsletter Last Week in AI.
I will give you a main article and related articles with their text, and you will write a concise summary that covers all the stories.
The summary should contain the key technical details, be easy to understand, and run roughly 200-400 words (less for a simple story). Write short paragraphs of about three sentences, never more than five; use as many as the story needs rather than packing it into one or two dense blocks. Use a bulleted list when the story is either several parallel announcements or a dated sequence of four or more beats; keep an orienting sentence above the bullets and the analysis below them.
The reader should clearly understand the key points from all the stories after reading your summary.
Focus on the concrete details of the stories rather than context or implications.
Synthesize across the articles rather than summarizing each in turn.

Write in the newsletter's house style (scripts/STYLE_GUIDE.md is the full reference):
* Keep the specifics you use exact — figures, dates, names, unrounded numbers. Do not abstract
  them into vagueness, and do not add any fact the source does not state. Exact is not exhaustive.
* Stay on the headline event. Keep the background needed to follow it (a short recap of how a
  dispute began is fine), but cut adjacent events — another incident, another report, reactions
  to a different announcement — and secondary detail within the event: benchmark lists,
  system-card findings, a minor figure's affiliation, the least consequential beat of a timeline.
* Do NOT use bold, italics or any markdown emphasis. Proper nouns carry themselves.
* Mean sentence around 30 words, none over 45. One idea per sentence; split a sentence that
  carries a mechanism, a number, a date and a quote all at once.
* Connect paragraphs — causal, contrastive or topical. Avoid the "Framing clause: full independent
  clause" construction; a full stop usually reads better.
* Attribute every judgment or hedge to a named person or publication, or cut it. Never credit a
  claim to an outlet that did not make it, and never present your own inference as reported.
* No editorialising and no self-reference: no "the defining story", "what made this remarkable",
  "as noted above".
* Do not assert causation the source does not. If the source gives a sequence — X happened, then
  Y happened — write the sequence. Do not write "Y after X" or "prompting Y" unless the source says
  one caused the other. If a company denies a link, say so rather than asserting it.
* Quote verbatim or do not use quotation marks. Never adjust wording inside quotes, and make sure
  the words just outside the quote marks match what the speaker was actually responding to.
* Use your own sentence structures. Do not track the source's phrasing clause by clause; figures
  and names are facts and stay, but the sentences around them should be yours.
* State what the source states, including which party said it. If two sources conflict on a date,
  an affiliation, or a number, prefer the primary account — the researchers' own writeup, the
  ruling, the company post — over secondary coverage of it.
'''.strip()

        # Build user prompt with main article and related articles
        user_prompt = f'Main Article:\nTitle: {title}\n{clip_text_words(news_article["text"])}\n\n'

        user_prompt += 'Related Articles:\n'
        for i, related in enumerate(related_articles, 1):
            user_prompt += f'Related Article {i}:\nTitle: {related["title"]}\n{clip_text_words(related["text"])}\n\n'

        user_prompt = user_prompt.strip()
    else:
        system_prompt = '''
You are an expert writer and commentator hired to write summaries of articles for the newsletter Last Week in AI.
I will give you an article with associated text, and you will write a concise summary.
The summary should contain the key technical details, be easy to understand, and run roughly 200-400 words (less for a simple story). Write short paragraphs of about three sentences, never more than five; use as many as the story needs rather than packing it into one or two dense blocks. Use a bulleted list when the story is either several parallel announcements or a dated sequence of four or more beats; keep an orienting sentence above the bullets and the analysis below them.
The reader should clearly understand the key points from the article after reading your summary.
Focus on the concrete details of the story rather than context or implications.

Write in the newsletter's house style (scripts/STYLE_GUIDE.md is the full reference):
* Keep the specifics you use exact — figures, dates, names, unrounded numbers. Do not abstract
  them into vagueness, and do not add any fact the source does not state. Exact is not exhaustive.
* Stay on the headline event. Keep the background needed to follow it (a short recap of how a
  dispute began is fine), but cut adjacent events — another incident, another report, reactions
  to a different announcement — and secondary detail within the event: benchmark lists,
  system-card findings, a minor figure's affiliation, the least consequential beat of a timeline.
* Do NOT use bold, italics or any markdown emphasis. Proper nouns carry themselves.
* Mean sentence around 30 words, none over 45. One idea per sentence; split a sentence that
  carries a mechanism, a number, a date and a quote all at once.
* Connect paragraphs — causal, contrastive or topical. Avoid the "Framing clause: full independent
  clause" construction; a full stop usually reads better.
* Attribute every judgment or hedge to a named person or publication, or cut it. Never credit a
  claim to an outlet that did not make it, and never present your own inference as reported.
* No editorialising and no self-reference: no "the defining story", "what made this remarkable",
  "as noted above".
* Do not assert causation the source does not. If the source gives a sequence — X happened, then
  Y happened — write the sequence. Do not write "Y after X" or "prompting Y" unless the source says
  one caused the other. If a company denies a link, say so rather than asserting it.
* Quote verbatim or do not use quotation marks. Never adjust wording inside quotes, and make sure
  the words just outside the quote marks match what the speaker was actually responding to.
* Use your own sentence structures. Do not track the source's phrasing clause by clause; figures
  and names are facts and stay, but the sentences around them should be yours.
* State what the source states, including which party said it. If two sources conflict on a date,
  an affiliation, or a number, prefer the primary account — the researchers' own writeup, the
  ruling, the company post — over secondary coverage of it.
'''.strip()

        user_prompt = f'''
Title: {title}
{clip_text_words(news_article["text"])}
'''.strip()

    try:
        return query_llm_simple(system_prompt, user_prompt, max_tokens=SUMMARY_MAX_TOKENS, model=MODEL_OPUS, debug_label=f"SUMMARY for {title[:30]}")
    except Exception as e:
        print(f"Error generating summary for {title}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        raise


def rank_articles(articles):
    """Rank articles by importance using AI (currently unused - keeping for backwards compatibility)."""
    system_prompt = '''
You are an expert writer and commentator in AI.
The user will give you a list of articles, and you will rank them in order of importance.
The most important article should be ranked first, and the least important article should be ranked last.
Article index, title, and excerpts are given.
Format your response as a valid JSON list of article indices, starting with the character '[' and ending with the character ']'.
'''.strip()

    user_prompt = '\n'.join([
        f'{idx} | Title: {article["title"]} | Excerpt: {article["excerpt"]}\n'
        for idx, article in enumerate(articles)
    ])

    output = query_llm_simple(system_prompt, user_prompt, max_tokens=RANKING_MAX_TOKENS, model=MODEL_SONNET, debug_label=f"RANKING {len(articles)} articles")
    start = output.find('[')
    end = output.find(']')
    output = output[start:end+1]
    return json.loads(output)


def get_newsletter_excerpt(top_news):
    system_prompt = '''
You are an expert news writer. The user will give you the title, URL, and summary of a few articles to be featured in a newsletter about AI. You will return a short, catchy, and accurate headline for the entire newsletter, based on the featured article titles. Feel free to use emojis. End the headline with ", and more!". Respond only with the headline with nothing else. Use emojis throughout the headline.

Below are a few examples of such headlines. Please adhere to the style observed in these examples.

Gen AI at peak of inflated expectations, NYT bans AI companies from scraping its data, FEC may limit AI political ads before 2024, Hollywood boosts Gen AI spend amid strikes, and more!

OpenAI lawsuits, NASA to explore AI on spaceships, OpenAI vs. Microsoft, generated content flooding the Internet, and more!

Victims of false facial regonition matches, White House launches AI-based security contest, Spotify launches AI DJ globally, bots solve captchas better than humans, and more
'''.strip()

    return query_llm_simple(system_prompt, top_news, max_tokens=NEWSLETTER_EXCERPT_MAX_TOKENS, model=MODEL_HAIKU, debug_label="NEWSLETTER_EXCERPT")


def process_related_articles(related_articles_str, need_text=True):
    """Process comma-separated related article URLs and fetch their content.

    need_text=False fetches titles only, for sections that link related stories but do not
    summarize them. That skips the web_fetch fallback, which costs an LLM call per URL.
    """
    related_articles_data = []

    if not related_articles_str or not isinstance(related_articles_str, str):
        return related_articles_data

    related_urls = [url.strip() for url in related_articles_str.split(',') if url.strip()]

    for related_url in related_urls:
        clean_related_url = clean_url(related_url.strip())
        try:
            related_article = Article(clean_related_url)
            related_article.download()
            related_article.parse()

            if related_article.title and (related_article.text or not need_text):
                related_articles_data.append({
                    'title': related_article.title,
                    'text': related_article.text,
                    'url': clean_related_url
                })
                continue
        except Exception as e:
            print(f'  newspaper failed for related article {clean_related_url}: {e}')

        if not need_text:
            # Label-only: fall back to the bare URL rather than paying for an LLM fetch.
            related_articles_data.append({
                'title': label_from_url(clean_related_url),
                'text': '',
                'url': clean_related_url
            })
            continue

        # Fallback: use web_fetch to get a detailed summary
        try:
            text = web_fetch_article_summary(clean_related_url)
            if text:
                related_articles_data.append({
                    'title': label_from_url(clean_related_url),
                    'text': text,
                    'url': clean_related_url
                })
        except Exception as e:
            print(f'  web_fetch fallback also failed for related article {clean_related_url}: {e}')

    return related_articles_data


def build_top_news_section(articles, image_folder):
    """Build the Top News section of the newsletter."""
    parts = ['### Top News\n\n']
    image_name = ''

    # Use CSV order
    rank = list(range(len(articles)))

    # Process related articles first to get their content
    processed_articles = []
    for article in articles:
        related_articles_data = process_related_articles(article.get('related_urls'))
        processed_articles.append({
            **article,
            'related_articles_data': related_articles_data
        })

    # Generate summaries with related articles
    summaries = []
    warnings = []
    for article in processed_articles:
        try:
            summary = get_article_summary(article['title'], article['news_article'], article['related_articles_data'])
            summaries.append(summary)
        except:
            summaries.append(None)
            continue
        # Deterministic fidelity checks against the source text we already have in hand.
        sources = [(article['news_article'] or {}).get('text', '')]
        sources += [r.get('text', '') for r in (article['related_articles_data'] or [])]
        for w in verify_summary(summary, sources):
            warnings.append(f"[{article['title'][:60]}] {w}")

    if warnings:
        print(f"\n  !! {len(warnings)} fidelity warnings — review before publishing:")
        for w in warnings:
            print(f"     {w}")
        with open('summary_warnings.txt', 'w') as f:
            f.write('\n'.join(warnings) + '\n')
        print("     (also written to scripts/summary_warnings.txt)\n")

    for rank_idx in tqdm(rank, leave=False):
        try:
            article = processed_articles[rank_idx]
            summary = summaries[rank_idx] if rank_idx < len(summaries) else None
            if summary is None:
                summary = ''

            title, url, news_article = article['title'], article['url'], article['news_article']

            parts.append(f'#### [{title}]({url})\n')

            # Add related articles section at the top
            if article.get('related_articles_data') and len(article['related_articles_data']) > 0:
                parts.append('Related:')
                for related in article['related_articles_data']:
                    if related.get('title') and related.get('url'):
                        parts.append(f'\n * [{related["title"]}]({related["url"]})')
                parts.append('\n\n')

            if not news_article:
                parts.append(summary + '\n\n')
                continue

            if news_article.get('has_top_image', False) and news_article.get('top_image'):
                parts.append(f'![]({news_article["top_image"]})\n\n')

                if rank_idx == 0:
                    try:
                        image_response = requests.get(news_article['top_image'])
                        if image_response.status_code == 200:
                            image_name = clean_url(news_article['top_image']).split("/")[-1]
                            with open(image_folder / image_name, "wb") as img_file:
                                img_file.write(image_response.content)
                    except:
                        pass

            parts.append(summary + '\n\n')
        except:
            continue

    print("Top News section completed")
    return ''.join(parts), image_name


def build_other_category_section(category, articles):
    """Build a section for non-Top News categories."""
    parts = [f'#### {category}']

    # Use CSV order
    rank = list(range(len(articles)))

    first_article = articles[rank[0]]
    if first_article['news_article'] and first_article['news_article'].get('has_top_image'):
        parts.append(f'\n![]({first_article["news_article"]["top_image"]})')
    parts.append('\n\n')

    # Titles only — these stories are linked, not summarized, so skip the costly text fetch.
    related_lists = apply_map_batch(
        process_related_articles,
        [(article.get('related_urls'), False) for article in articles]
    )

    for rank_idx in tqdm(rank, leave=False):
        article = articles[rank_idx]
        title, url, excerpt = article['title'], article['url'], article['excerpt']
        parts.append(f'[{title}]({url}). {excerpt}')

        related = related_lists[rank_idx]
        if related:
            # Two trailing spaces force a <br> inside the SAME paragraph, so the related line
            # sits tight under its story instead of becoming a sibling <p> with an equal
            # 1.5rem gap above and below — which would read as unattached to either item.
            links = ', '.join(f'[{r["title"]}]({r["url"]})' for r in related)
            parts.append(f'  \nRelated: {links}')
        parts.append('\n\n')

    return ''.join(parts)


if __name__ == "__main__":
    __spec__ = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=False, default='news.csv')
    parser.add_argument('--force_overwrite', '-f', action='store_true')
    args = parser.parse_args()

    digest_number = args.digest_number
    inflect_engine = inflect.engine()
    digest_number_english = inflect_engine.number_to_words(inflect_engine.ordinal(digest_number)).replace(' ', '-')
    print(f'Parsing for the {digest_number_english} digest')

    image_folder = Path(f'../assets/img/digests/{digest_number}')
    print(f'Making image folder {image_folder}')
    image_folder.mkdir(parents=True, exist_ok=True)

    output_md = Path('../_posts/digests') / get_output_file_name(digest_number)

    print(f'Will save result to {output_md}')
    if os.path.isfile(output_md):
        if not args.force_overwrite:
            raise ValueError('Cannot overwrite existing output file!')

    print(f'Loading template from {args.template_file}')
    with open(args.template_file, 'r') as template_file:
        md_template = template_file.read()

    input_csv = args.input_csv
    if not input_csv:
        input_csv = f'Last Week in AI News Planning - Past - {digest_number}.csv'

    print(f'Reading {input_csv}')
    csv = pd.read_csv(input_csv, encoding='utf-8')
    rows = []
    for row_num, row in csv.iterrows():
        if 'arxiv' in row['URL'] and row['Name'].startswith('Title:'):
            # remove "Title:" from arxiv titles
            row['Name'] = row['Name'][6:]

        if 'arxiv' in row['URL'] and row['Name'].startswith('[]'):
            # remove "Title:" from arxiv titles
            row['Name'] = row['Name'].split(']')[1]

        # Remove arXiv ID format like '[2507.18074] ' from the beginning of titles
        if 'arxiv' in row['URL'] and ']' in row['Name']:
            # Remove everything up to and including the first ']' and any following whitespace
            row['Name'] = row['Name'].split(']', 1)[1].strip()

        if 'youtube' in row['URL']:
            continue

        row['URL'] = clean_url(row['URL'])
        rows.append(row)

    print('Getting news articles...')
    news_articles = [get_news_article(row['URL'], title=row['Name']) for row in tqdm(rows)]

    print('Getting article categories...')
    categories = apply_map_batch(
        get_article_category,
        [
            (row, news_article['text'][:500] if news_article and 'text' in news_article else "")
            for row, news_article in zip(rows, news_articles)
        ]
    )

    print('Getting article excerpts...')
    excerpts = apply_map_batch(
        get_article_excerpt,
        [
            (row, news_article)
            for row, news_article in zip(rows, news_articles)
        ]
    )

    articles_map = {category: [] for category in CATEGORIES}
    for row, news_article, excerpt, category in zip(rows, news_articles, excerpts, categories):
        # Skip articles with empty or invalid categories
        if not category or category.strip() == '' or category not in CATEGORIES:
            continue

        # Related URLs live in the 'Related' column; legacy CSVs stashed them in 'Type'.
        related = cell(row, 'Related')
        if not related and cell(row, 'Type').startswith('http'):
            related = cell(row, 'Type')

        articles_map[category].append({
            'url': row['URL'],
            'title': news_article['title'] if news_article and 'title' in news_article else row['Name'],
            'related_urls': related,
            'excerpt': excerpt,
            'category': category,
            'news_article': news_article
        })

    print('Populating content...')
    top_news_parts = []
    content_parts = []
    image_name = ''

    for category in tqdm(CATEGORIES):
        articles = articles_map[category]
        if articles:
            if category == 'Top News':
                top_news_content, image_name = build_top_news_section(articles, image_folder)
                top_news_parts.append(top_news_content)
            else:
                content_parts.append(build_other_category_section(category, articles))

    top_news = ''.join(top_news_parts)
    content = ''.join(content_parts).rstrip('\n')

    digest_excerpt = get_newsletter_excerpt(top_news if top_news.strip() else content)

    md = md_template.replace('$digest_number$', str(digest_number)) \
                    .replace('$digest_number_english$', digest_number_english) \
                    .replace('$top_news$', top_news) \
                    .replace('$content$', content) \
                    .replace('$im_name$', image_name) \
                    .replace('$digest_excerpt$', digest_excerpt)

    print('Saving digest markdown...')
    with open(output_md, 'wb') as output_file:
        output_file.write(md.encode('utf-8'))

    print('Done!')
