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
def query_openai(messages, max_tokens=10, model='gpt-4o'):
    return _OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    ).choices[0].message.content


def get_article_category(row, excerpt):
    if row['Type'] in CATEGORIES:
        print(row['Type'])
        return row['Type']

    title, url = row['Name'], row['URL']
    if 'arxiv' in url:
        return 'Research'

    prompt = f'''
Title: {title}
Summary: {excerpt}
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

The user will provide the article title, link, and description. 
After careful consideration, you will respond with ONLY the predicted article type, with no explanations, punctuation, formatting, or anything else.
Only respond with one of the above types (Business, Research, Tools, Concerns, Policy, Analysis, Expert Opinions, Explainers, Fun).
'''.strip()
    return query_openai([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt},
    ], model='gpt-4o')


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
            assert article.text
            return {
                'title': article.title,
                'text': article.text,
                'top_image': article.top_image,
                'has_top_image': article.has_top_image()
            }
    except Exception as e:
        print('ERROR: not able to get text for URL '+url)
        print(e)
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

Examples:
* 'Google is testing a vibe-coding app called Opal' -> 'The app allows users to create and share mini web apps using text prompts and a visual workflow, aiming to make app development accessible to non-technical users.'
* 'GitHub Goes After Vibe Coding Fans with the Public Preview of GitHub Spark' -> 'Spark allows users to create full-stack apps from natural language prompts, and is available to Copilot Pro+ subscribers for $39 a month.'
'''.strip()
    
    prompt = f'''
Title: {row['Name']}
Text: {clip_text_words(article["text"])}
'''.strip()
    return query_openai([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ],
    max_tokens = 100)


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

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    try:
        return query_openai(messages, max_tokens=4000, model='gpt-4')
    except:
        return None


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

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]
    output = query_openai(messages, max_tokens=400)
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

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    return query_openai(messages, max_tokens=256, model='gpt-4')


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
    
    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': markdown_content}
    ]

    return query_openai(messages, max_tokens=8000, model='gpt-4o')


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

    print('Getting article excerpts...')
    excerpts = apply_map_batch(
        get_article_excerpt,
        [
            (row, news_article)
            for row, news_article in zip(rows, news_articles)
        ]
    )

    print('Getting article categories...')
    categories = apply_map_batch(
        get_article_category,
        [
            (row, excerpt)
            for row, excerpt in zip(rows, excerpts)
        ]
    )

    articles_map = {c : [] for c in CATEGORIES}
    for row, news_article, excerpt, category in zip(rows, news_articles, excerpts, categories):
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
                for article in articles:
                    related_articles_data = []
                    if article['Related Articles'] and type(article['Related Articles']) == str:
                        for related_url in article['Related Articles'].split(','):
                            try: 
                                if '?' in related_url:
                                    related_url = related_url.split('?')[0]
                                related_article = Article(related_url.strip())
                                related_article.download()
                                related_article.parse()
                                related_articles_data.append({
                                    'title': related_article.title,
                                    'text': related_article.text,
                                    'url': related_url.strip()
                                })
                            except:
                                continue
                    
                    processed_articles.append({
                        **article,
                        'related_articles_data': related_articles_data
                    })

                # Generate summaries with related articles
                summaries = apply_map_batch(
                    get_article_summary,
                    [
                        (article['title'], article['news_article'], article['related_articles_data'])
                        for article in processed_articles
                    ]
                )

                for r in tqdm(rank, leave=False):
                    article = processed_articles[r]
                    summary = summaries[r]
                    if summary is None:
                        summary = ''

                    title, url, news_article = article['title'], article['url'], article['news_article']

                    top_news += f'#### [{title}]({url})'
                    top_news += '\n'
                    
                    # Add related articles section at the top
                    if article['related_articles_data']:
                        top_news += 'Related:'
                        for related in article['related_articles_data']:
                            top_news += f'\n * [{related["title"]}]({related["url"]})'
                        top_news += '\n\n'
                    
                    if not news_article:
                        continue
                    if news_article['has_top_image']:
                        top_news += f'![]({news_article["top_image"]})'

                        if r == 0:
                            im_response = requests.get(news_article['top_image'])
                            if im_response.status_code == 200:
                                im_name = news_article['top_image'].split("/")[-1]

                                with open(im_folder / im_name, "wb") as f:
                                    f.write(im_response.content)

                    top_news += '\n\n'
                    top_news += summary
                    top_news += '\n\n'
            else:
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
    md = final_polish_newsletter(md)

    print('Saving digest markdown...')
    with open(output_md, 'wb') as f:
        f.write(md.encode('utf-8'))

    print('Done!')
