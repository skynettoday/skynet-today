import os
import argparse
import requests

import pandas as pd
import inflect
import openai
import json

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from tenacity import retry, stop_after_attempt, wait_random_exponential


CATEGORIES = [
    'Top News',
    'Research',
    'Applications',
    'Business',
    'Concerns',
    'Analysis',
    'Policy',
    'Expert Opinions',
    'Explainers',
    'Fun'
]


def classify_article_type_ft(row):
    prompt = f'''
Title: {row['Name']}
Description: {row['Excerpt']}
Link: {row['URL']}
Type:
'''.strip()
    
    response = openai.Completion.create(
        prompt=prompt, 
        stop=['.', '\n'],
        engine='curie:ft-jacky:article-type-2023-01-18-07-53-32',
        max_tokens=10,
        temperature=0,
    )['choices'][0]['text'].strip()

    return response


@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(10))
def query_openai(messages, max_tokens=10):
    return openai.ChatCompletion.create(
        model='gpt-3.5-turbo-16k', 
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    ).choices[0]['message']['content']


def get_article_category(row, excerpt):
    if row['Type'] in CATEGORIES:
        return row['Type']

    title, url = row['Name'], row['URL']

    prompt = f'''
Title: {title}
Summary: {excerpt}
Link: {url}
'''.strip()

    system_prompt = '''
Your task is to classify articles about AI into one of the following types:
Business: Anything related to product announcements, investments, funding, VCs, company updates, or market trends.
Research: Scientific studies, research in AI, or applying AI to do science in various fields.
Applications: Applying AI to do something.
Concerns: Discussions and news about problems, harms, and any alarming things about AI, including govermnet investigations about AI.
Policy: News, analysis, and opinions related to government policies.
Analysis: Analyzes an existing topic about AI that's not the above topics (not news).
Expert Opinions: Opinion pieces from experts and not factual reporting. If it's not clear the opinion piece is from a domain expert, then it should be in Analysis.
Explainers: Explains a given topic in AI with the goal to educate the reader; tutorials, guides.
Fun: Anything silly, fun, and doesn't belong to the other types.

The user will provide the article title, link, and description. 
After careful consideration, you will respond with ONLY the predicted article type, with no explanations, punctuation, formatting, or anything else.
Please only respond with one of the above types (Business, Resesarch, Applications, Concerns, Policy, Analysis, Expert Opinions, Explainers, Fun).
'''.strip()
    return query_openai([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ])


def get_news_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        assert article.text
        return article
    except:
        return None
    

def clip_text_words(text, max_words=10000):
    words = text.split(" ")
    if len(words) > max_words:
        text = " ".join(words[:max_words])
    return text


def get_article_excerpt(row, article):
    system_prompt = '''
Given the title, subtitle, and text of an article about AI, write a short one sentence summary of its content.
The summary should NOT start with or contain phrases like "The article", "This article", or anything similar.
The summary should be exactly one sentence long.
'''.strip()
    
    prompt = f'''
Title: {row['Name']}
Subtitle: {row['Excerpt']}
Text: {clip_text_words(article.text)}
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
    days_to_monday = (today.weekday() - 0) % 7
    closest_monday = today - timedelta(days=days_to_monday)

    # Format the date as YYYY-MM-DD
    formatted_date = closest_monday.strftime("%Y-%m-%d")

    return f'{formatted_date}-{n}.md'


def get_article_summary(title, news_article):
    system_prompt = '''
You are an expert writer and commentator. 
The user will give you an article, and you will write a short summary.
The summary should be a paragraph long, contain key technical details, and be easy to understand. 
The summary should highlight key words and concepts from the article without abstracting them away. 
It should end with the key takeaway from the article.
'''.strip()
    
    user_prompt = f'''
Title: {title}
{clip_text_words(news_article.text)}
'''.strip()

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_prompt}
    ]

    return query_openai(messages, max_tokens=500)


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

    return json.loads(query_openai(messages, max_tokens=200))


if __name__ == "__main__":
    __spec__ = None
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=False, default='')
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

    with open('secrets/openai_api_key.txt', 'r') as f:
        openai.api_key = f.read().strip()

    print(f'Reading {input_csv}')
    csv = pd.read_csv(input_csv, encoding='utf-8')
    rows_news_articles = []
    for row_num, row in tqdm(csv.iterrows(), total=len(csv)):
        if 'arxiv' in row['URL'] or 'youtube' in row['URL']:
            continue

        news_article = get_news_article(row['URL'])
        if not news_article:
            continue

        rows_news_articles.append((row, news_article))

    print('Getting article excerpts...')
    excerpts = [
        get_article_excerpt(row, news_article) 
        for row, news_article in tqdm(rows_news_articles)
    ]

    print('Getting article categories...')
    categories = [
        get_article_category(row, excerpt)
        for (row, _), excerpt in tqdm(zip(rows_news_articles, excerpts), total=len(rows_news_articles))
    ]

    articles_map = {c : [] for c in CATEGORIES}
    for (row, news_article), excerpt, category in zip(rows_news_articles, excerpts, categories):
        articles_map[category].append({
            'url': row['URL'],
            'title': row['Name'],
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
                if articles[r]['news_article'].has_top_image():
                    rank[0], rank[idx] = rank[idx], rank[0]
                    break
            
            if c == 'Top News':
                top_news += f'### {c}'
                top_news += '\n\n'

                for r in tqdm(rank, leave=False):
                    article = articles[r]
                    title, url, news_article = article['title'], article['url'], article['news_article']
                    summary = get_article_summary(title, news_article)
                    
                    top_news += f'#### [{title}]({url})'
                    top_news += '\n'

                    if news_article.has_top_image():
                        top_news += f'![]({news_article.top_image})'

                        if r == 0:
                            im_response = requests.get(news_article.top_image)
                            if im_response.status_code == 200:
                                im_name = news_article.top_image.split("/")[-1]

                                with open(im_folder / im_name, "wb") as f:
                                    f.write(im_response.content)

                    top_news += '\n\n'
                    top_news += summary
                    top_news += '\n\n'
            else:
                content += f'#### {c}'
                
                if articles[rank[0]]['news_article'].has_top_image():
                    content += '\n'
                    content += f'![]({articles[rank[0]]["news_article"].top_image})'
                content += '\n\n'
                
                for r in tqdm(rank, leave=False):
                    article = articles[r]
                    title, url, excerpt = article['title'], article['url'], article['excerpt']
                    content += f'[{title}]({url}) - {excerpt}'
                    content += '\n\n'

    # remove the last two empty lines
    content = content[:-2]

    md = md_template.replace('$digest_number$', str(n)) \
                    .replace('$digest_number_english$', n_english) \
                    .replace('$top_news$', top_news) \
                    .replace('$content$', content) \
                    .replace('$im_name$', im_name)

    print('Saving digest markdown...')
    with open(output_md, 'wb') as f:
        f.write(md.encode('utf-8'))

    print('Done!')
