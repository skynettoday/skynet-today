import os
import argparse
import requests
import re
from multiprocessing.dummy import Pool

import pandas as pd
import inflect
import json

from openai import OpenAI
with open('secrets/openai_api_key.txt', 'r') as f:
    _OPENAI_CLIENT = OpenAI(api_key=f.read().strip())

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from tenacity import retry, stop_after_attempt, wait_random_exponential
from content_retrieval import get_arxiv_paper_contents

CATEGORIES = [
    'Top News',
    'Tools',
    'Business',
    'Research',
    'Concerns',
    'Policy',
    'Analysis',
    'Expert Opinions',
    'Explainers',
    'Fun'
]


def apply_map_batch(func, args_list):
    pool = Pool(os.cpu_count())
    promises = [pool.apply_async(func, args) for args in args_list]

    results = [None] * len(promises)
    done_idxs = set()
    pbar = tqdm(total=len(promises))
    while len(done_idxs) < len(promises):
        for idx, promise in enumerate(promises):
            if idx not in done_idxs and promise.ready():
                done_idxs.add(idx)
                results[idx] = promise.get()
                pbar.update(1)
    return results


@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(10))
def query_openai(instructions, user_input, max_completion_tokens=100, model='gpt-5', debug_label=""):
    try:
        if instructions:
            result = _OPENAI_CLIENT.responses.create(
                model=model,
                instructions=instructions,
                input=user_input,
                reasoning={"effort": "minimal"},
            ).output_text
        else:
            result = _OPENAI_CLIENT.responses.create(
                model=model,
                input=user_input
            ).output_text

        return result
    except Exception as e:
        print(f"ERROR in query_openai ({debug_label}): {type(e).__name__}: {e}")
        if hasattr(e, 'response'):
            print(f"Response: {e.response}")
        if hasattr(e, 'body'):
            print(f"Body: {e.body}")
        raise


def get_article_category(row, article_text):
    if row['Type'] in CATEGORIES:
        return row['Type']

    title, url = row['Name'], row['URL']
    if 'arxiv' in url:
        return 'Research'

    # Use first 500 characters of article text if available, otherwise just title and URL
    text_preview = article_text[:500] if article_text else "No text available"
    
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
    return query_openai(
        system_prompt,
        prompt,
        model="gpt-5-mini-2025-08-07",
        max_completion_tokens=50,
        debug_label=f"CATEGORY for {title[:30]}"
    )


def get_news_article(url):
    try:
        if 'arxiv' in url:
            text = get_arxiv_paper_contents(url)
            return {
                'text': text,
                'top_image': None,
                'has_top_image': False
            }
        else:
            article = Article(url)
            article.download()
            article.parse()
            if not article.text:
                return None
            return {
                'title': article.title,
                'text': article.text,
                'top_image': article.top_image,
                'has_top_image': article.has_top_image()
            }
    except Exception as e:
        return None


def clip_text_words(text, max_words=10000):
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
    return query_openai(
        system_prompt,
        prompt,
        model="gpt-5-mini-2025-08-07",
        max_completion_tokens = 100,
        debug_label=f"EXCERPT for {row['Name'][:30]}"
    )


def get_article_type_manual(title, link, excerpt):
    print('To which category does this article belong?')
    print()
    print(row['Name'].encode('utf-8'))
    print()
    print(row['Excerpt'].encode('utf-8'))
    print()

    for i, c in enumerate(CATEGORIES):
        print(f'{i}) {c}')
    while True:
        try:
            print()
            c_idx = int(input('Category Number: '))
            c = CATEGORIES[c_idx]
            break
        except:
            print('Please enter a valid category!')
    print()

    return c


def get_output_file_name(n):
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

    return f'{formatted_date}-{n}.md'


def get_article_summary(title, news_article, related_articles=None):
    if not news_article:
        return ':/'
    
    # Determine if we have multiple articles to summarize
    has_related = related_articles and len(related_articles) > 0
    
    if has_related:
        system_prompt = '''
You are an expert writer and commentator hired to write summaries of articles for the newsletter Last Week in AI. 
I will give you a main article and related articles with their text, and you will write a concise summary that covers all the stories.
The summary should be at most two paragraphs long, with each paragraph having at least four sentences, contain key technical details, and be easy to understand. If it makes sense, you can also include a bullet point list.
The summary should highlight key words and concepts from all articles without abstracting them away. 
The reader should clearly understand the key points from all the stories after reading your summary.
Focus on the details of the concrete details of the stories rather than context or implications. 
When multiple articles are provided, synthesize the information to give a comprehensive overview of the topic.
The writing style should be succinct and direct.'''.strip()
        
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
The summary should be at most two paragraphs long, with each paragraph having at least four sentences, contain key technical details, and be easy to understand. If it makes sense, you can also include a bullet point list.
The summary should highlight key words and concepts from the article without abstracting them away. 
The reader should clearly understand the key points from the article after reading your summary.
Focus on the details of the concrete details of the story rather than context or implications. 
The writing style should be succinct and direct.'''.strip()
        
        user_prompt = f'''
Title: {title}
{clip_text_words(news_article["text"])}
'''.strip()

    try:
        result = query_openai(system_prompt, user_prompt, max_completion_tokens=4000, model='gpt-5', debug_label=f"SUMMARY for {title[:30]}")
        return result
    except Exception as e:
        print(f"Error generating summary for {title}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception message: {str(e)}")
        
        # For RetryError from tenacity, try to get the underlying error
        if hasattr(e, 'last_attempt') and e.last_attempt:
            try:
                underlying = e.last_attempt.exception()
                print(f"Underlying exception: {type(underlying).__name__}: {str(underlying)}")
                # For OpenAI errors, try to get more details
                if hasattr(underlying, 'response') and underlying.response:
                    print(f"HTTP Status: {underlying.response.status_code}")
                    if hasattr(underlying.response, 'text'):
                        print(f"Response text: {underlying.response.text}")
                if hasattr(underlying, 'body'):
                    print(f"Error body: {underlying.body}")
            except Exception as inner_e:
                print(f"Could not extract underlying error: {inner_e}")
        
        # Re-raise to let the caller handle it
        raise


def rank_articles(articles):
    system_prompt = '''
You are an expert writer and commentator in AI.
The user will give you a list of articles, and you will rank them in order of importance.
The most important article should be ranked first, and the least important article should be ranked last.
Article index, title, and excerpts are given.
Format your response as a valid JSON list of article indices, starting with the character '[' and ending with the character ']'.
'''.strip()
    
    user_prompt = '\n'.join([
        f'{i} | Title: {a["title"]} | Excerpt: {a["excerpt"]}\n' 
        for i, a in enumerate(articles)
    ])

    output = query_openai(system_prompt, user_prompt, max_completion_tokens=400, model='gpt-5', debug_label=f"RANKING {len(articles)} articles")
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
    
    user_prompt = top_news

    return query_openai(system_prompt, user_prompt, max_completion_tokens=256, model='gpt-5', debug_label="NEWSLETTER_EXCERPT")


def final_polish_newsletter(markdown_content):
    system_prompt = '''
You are an expert editor for the "Last Week in AI" newsletter. Your task is to polish the final newsletter content to ensure it's publication-ready.

Please review the entire newsletter and make the following improvements:

1. **Remove duplicate articles**: If the same article appears multiple times (same URL or very similar titles), keep only the best version and remove duplicates.

2. **Vary sentence starters**: Look at all the article excerpt sentences and ensure they don't start with repetitive words/phrases. Rewrite excerpts to have more varied and engaging openings while maintaining the same factual content.

3. **Overall polish**: 
   - Ensure consistent formatting
   - Fix any grammatical errors
   - Improve flow and readability
   - Make sure section transitions are smooth
   - Ensure the tone is consistent throughout

4. **Maintain accuracy**: Do not change any URLs, article titles, or factual content. Only improve the presentation and remove duplicates.

Return the polished markdown content. Keep all the original structure and formatting intact, just improve the quality and remove any issues.
Just output the polished markdown content, with no additional explanations or comments.
'''.strip()
    
    return query_openai(system_prompt, markdown_content, max_completion_tokens=8000, model='gpt-5', debug_label="FINAL_POLISH")


if __name__ == "__main__":    
    __spec__ = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=False, default='news.csv')
    parser.add_argument('--force_overwrite', '-f', action='store_true')
    args = parser.parse_args()

    n = args.digest_number
    p = inflect.engine()
    n_english = p.number_to_words(p.ordinal(n)).replace(' ', '-')
    print(f'Parsing for the {n_english} digest')

    im_folder = Path(f'../assets/img/digests/{n}')
    print(f'Making image folder {im_folder}')
    im_folder.mkdir(parents=True, exist_ok=True)

    output_md = Path('../_posts/digests') / get_output_file_name(n)

    print(f'Will save result to {output_md}')
    if os.path.isfile(output_md):
        if not args.force_overwrite:
            raise ValueError('Cannot overwrite existing output file!')

    print(f'Loading template from {args.template_file}')
    with open(args.template_file, 'r') as f:
        md_template = f.read()

    input_csv = args.input_csv
    if not input_csv:
        input_csv = f'Last Week in AI News Planning - Past - {n}.csv'

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

        if '?' in row['URL']:
            row['URL'] = row['URL'].split("?")[0]

        rows.append(row)

    print('Getting news articles...')
    news_articles = [get_news_article(row['URL']) for row in tqdm(rows)]

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

    articles_map = {c : [] for c in CATEGORIES}
    for row, news_article, excerpt, category in zip(rows, news_articles, excerpts, categories):
        # Skip articles with empty or invalid categories
        if not category or category.strip() == '' or category not in CATEGORIES:
            continue
            
        articles_map[category].append({
            'url': row['URL'],
            'title': news_article['title'] if news_article and 'title' in news_article else row['Name'],
            'Related Articles': row['Related'],
            'excerpt': excerpt,
            'category': category,
            'news_article': news_article
        })
    
    print('Populating content...')
    top_news = ''
    content = ''
    im_name = ''
    for c in tqdm(CATEGORIES):
        articles = articles_map[c]
        if articles:
            # Skip ranking if there's only one article
            if len(articles) == 1:
                rank = [0]
            else:
                # place the first article w/ an image first
                rank = rank_articles(articles)
                for idx, r in enumerate(rank):
                    try:
                        if articles[r]['news_article']['has_top_image']:
                            rank[0], rank[idx] = rank[idx], rank[0]
                            break
                    except:
                        continue
            
            if c == 'Top News':
                top_news += f'### {c}'
                top_news += '\n\n'

                # Process related articles first to get their content
                processed_articles = []
                for article_idx, article in enumerate(articles):
                    related_articles_data = []
                    
                    # Safely process related articles
                    try:
                        if article.get('Related Articles') and isinstance(article['Related Articles'], str):
                            related_urls = [url.strip() for url in article['Related Articles'].split(',') if url.strip()]
                            
                            for related_idx, related_url in enumerate(related_urls):
                                try: 
                                    if '?' in related_url:
                                        clean_url = related_url.split('?')[0]
                                    else:
                                        clean_url = related_url
                                    
                                    related_article = Article(clean_url.strip())
                                    related_article.download()
                                    related_article.parse()
                                    
                                    if related_article.text and related_article.title:
                                        related_articles_data.append({
                                            'title': related_article.title,
                                            'text': related_article.text,
                                            'url': clean_url.strip()
                                        })
                                except Exception as e:
                                    # Continue to next related article instead of failing completely
                                    continue
                    except Exception as e:
                        # Even if related articles fail completely, continue with main article
                        related_articles_data = []
                    
                    # Always append the article, even if related articles failed
                    processed_articles.append({
                        **article,
                        'related_articles_data': related_articles_data
                    })

                # Generate summaries with related articles - with error handling
                summaries = []
                for article in processed_articles:
                    try:
                        summary = get_article_summary(article['title'], article['news_article'], article['related_articles_data'])
                        summaries.append(summary)
                    except Exception as e:
                        summaries.append(None)  # Add None so indices still match

                for r in tqdm(rank, leave=False):
                    try:
                        article = processed_articles[r]
                        summary = summaries[r] if r < len(summaries) else None
                        if summary is None:
                            summary = ''

                        title, url, news_article = article['title'], article['url'], article['news_article']

                        top_news += f'#### [{title}]({url})'
                        top_news += '\n'
                        
                        # Add related articles section at the top
                        if article.get('related_articles_data') and len(article['related_articles_data']) > 0:
                            top_news += 'Related:'
                            for related in article['related_articles_data']:
                                if related.get('title') and related.get('url'):
                                    top_news += f'\n * [{related["title"]}]({related["url"]})'
                            top_news += '\n\n'
                        
                        if not news_article:
                            top_news += summary + '\n\n'
                            continue
                            
                        if news_article.get('has_top_image', False) and news_article.get('top_image'):
                            top_news += f'![]({news_article["top_image"]})'

                            if r == 0:
                                try:
                                    im_response = requests.get(news_article['top_image'])
                                    if im_response.status_code == 200:
                                        im_name = news_article['top_image'].split("/")[-1]

                                        with open(im_folder / im_name, "wb") as f:
                                            f.write(im_response.content)
                                except Exception as e:
                                    pass

                        top_news += '\n\n'
                        top_news += summary
                        top_news += '\n\n'
                        
                    except Exception as e:
                        # Continue with next article instead of failing completely
                        continue
                    
                print("Top News section completed")
            else:
                try:
                    content += f'#### {c}'
                    
                    if articles[rank[0]]['news_article']['has_top_image']:
                        content += '\n'
                        content += f'![]({articles[rank[0]]["news_article"]["top_image"]})'
                    content += '\n\n'
                    
                    for r in tqdm(rank, leave=False):
                        article = articles[r]
                        title, url, excerpt = article['title'], article['url'], article['excerpt']
                        content += f'[{title}]({url}). {excerpt}'
                        content += '\n\n'
                except:
                    pass

    # remove the last two empty lines
    content = content[:-2]

    digest_excerpt = get_newsletter_excerpt(top_news)

    md = md_template.replace('$digest_number$', str(n)) \
                    .replace('$digest_number_english$', n_english) \
                    .replace('$top_news$', top_news) \
                    .replace('$content$', content) \
                    .replace('$im_name$', im_name) \
                    .replace('$digest_excerpt$', digest_excerpt)

    print('Applying final polish to the newsletter...')
    
    # Split the markdown into header (YAML front matter) and content
    if md.startswith('---'):
        # Find the end of the YAML front matter
        parts = md.split('---', 2)
        if len(parts) >= 3:
            header = f"---{parts[1]}---"
            content_to_polish = parts[2]
            
            # Polish only the content portion
            polished_content = final_polish_newsletter(content_to_polish)
            
            # Recombine header and polished content
            md = header + polished_content
        else:
            # Fallback: polish everything if parsing fails
            md = final_polish_newsletter(md)
    else:
        # No YAML front matter, polish everything
        md = final_polish_newsletter(md)

    print('Saving digest markdown...')
    with open(output_md, 'wb') as f:
        f.write(md.encode('utf-8'))

    print('Done!')
