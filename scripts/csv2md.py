import os
import argparse

import pandas as pd
import inflect
import openai

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from tenacity import retry, stop_after_attempt, wait_random_exponential

_CATEGORIES = [
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


@retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(10))
def query_openai(messages, max_tokens=10):
    return openai.ChatCompletion.create(
        model='gpt-3.5-turbo', 
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    ).choices[0]['message']['content']


def classify_article_type(row):
    prompt = f'''
Title: {row['Name']}
Description: {row['Excerpt']}
Link: {row['URL']}
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

def summarize_article(row):
    article = Article(row['URL'])
    try: 
        article.download()
        article.parse()
        authors = article.authors
        text = article.text
        words = text.split(" ")
        if len(words) > 2000:
            text = " ".join(words[:2000])
    except:
        return ":("

    system_prompt = '''
Given the title, subtitle, and text of an article about AI, write a short (one or two sentence) summary of its content.
DO NOT start with "The article" or "This article".
'''.strip()
    
    prompt = f'''
Title: {row['Name']}
Subtitle: {row['Excerpt']}
Text: {text}
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

    for i, c in enumerate(_CATEGORIES):
        print(f'{i}) {c}')
    while True:
        try:
            print()
            c_idx = int(input('Category Number: '))
            c = _CATEGORIES[c_idx]
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template_website.md')
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
    articles_map = {c : [] for c in _CATEGORIES}
    csv = pd.read_csv(input_csv, encoding='utf-8')
    url_to_summary_map = {}

    rows_to_classify = {}
    for row_num, row in csv.iterrows():
        if 'arxiv' in row['URL']:
            continue
        has_type = 'Type' not in row or not row['Type'] or row['Type'] not in articles_map
        has_content = row['Name'] and row['Excerpt']
        if has_type and has_content:
            rows_to_classify[row_num] = row
    
    print('Classifying articles...')
    article_types = [classify_article_type(row) for row in tqdm(rows_to_classify.values())]
    article_types_map = {row_num: article_type for row_num, article_type in zip(rows_to_classify.keys(), article_types)}
    
    for row_num, row in csv.iterrows():
        if 'arxiv' in row['URL']:
            continue
        if row_num in article_types_map:
            c = article_types_map[row_num]
            if c not in _CATEGORIES:
                print(f'Row {row_num} classified as:', c, 'which is not a valid category!')
                c = get_article_type_manual(row['Name'], row['URL'], row['Excerpt'])
        else:
            c = row['Type']
        articles_map[c].append(row)
            
    
    print('Summarizing articles...')
    for row_num, row in tqdm(rows_to_classify.items()):
        summary = summarize_article(row)
        url_to_summary_map[row['URL']] = summary
        
        print()
        print(row['Name'])
        print(summary)

    print('Populating content...')
    top_news = ''
    content = ''
    for c in _CATEGORIES:
        items = articles_map[c]
        if len(items) > 0:
            if c == 'Top News':
                top_news += f'### {c}'
                top_news += '\n\n'

                for item in items:
                    name, url = item['Name'], item['URL']
                    top_news += f'#### [{name}]({url})'
                    top_news += '\n\n'
                    top_news += 'one paragraph summary'
                    top_news += '\n\n'
            else:
                content += f'#### {c}'
                content += '\n\n'
                for item in items:
                    name, url, summary = item['Name'], item['URL'], url_to_summary_map[item['URL']]
                    content += f'[{name}]({url}) - "{summary}"'
                    content += '\n\n'

    # remove the last two empty lines
    content = content[:-2]

    md = md_template.replace('$digest_number$', str(n)) \
                    .replace('$digest_number_english$', n_english) \
                    .replace('$top_news$', top_news) \
                    .replace('$content$', content)

    print('Saving digest markdown...')
    with open(output_md, 'wb') as f:
        f.write(md.encode('utf-8'))

    print('Done!')
