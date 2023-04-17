import os
import logging
import argparse

import pandas as pd
import inflect
import openai

from pathlib import Path
from datetime import date, timedelta

try:
    import sys
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    print('Was not able to change sys encoding to utf-8, probably b/c you\'re on Python 3.')
    pass


_CATEGRORIES = [
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


def classify_article_type(title, link, excerpt):
    prompt = f'''
Title: {title}
Description: {excerpt}
Link: {link}
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


def get_article_type_manual(title, link, excerpt):
    print('To which category does this article belong?')
    print()
    print(row['Name'].encode('utf-8'))
    print()
    print(row['Excerpt'].encode('utf-8'))
    print()

    for i, c in enumerate(_CATEGRORIES):
        print(f'{i}) {c}')
    while True:
        try:
            print()
            c_idx = int(input('Category Number: '))
            c = _CATEGRORIES[c_idx]
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
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template_website.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=False, default='')
    parser.add_argument('--force_overwrite', '-f', action='store_true')
    parser.add_argument('--manual_article_type', '-m', action='store_true')
    args = parser.parse_args()

    n = args.digest_number
    p = inflect.engine()
    n_english = p.number_to_words(p.ordinal(n)).replace(' ', '-')
    logging.info(f'Parsing for the {n_english} digest')

    im_folder = Path(f'../assets/img/digests/{n}')
    logging.info(f'Making image folder {im_folder}')
    im_folder.mkdir(parents=True, exist_ok=True)

    output_md = Path('../_posts/digests') / get_output_file_name(n)

    logging.info(f'Will save result to {output_md}')
    if os.path.isfile(output_md):
        if not args.force_overwrite:
            raise ValueError('Cannot overwrite existing output file!')

    logging.info(f'Loading template from {args.template_file}')
    with open(args.template_file, 'r') as f:
        md_template = f.read()

    input_csv = args.input_csv
    if not input_csv:
        input_csv = f'Last Week in AI News Planning - Past - {n}.csv'

    set_openai_key = False

    logging.info(f'Reading {input_csv}')
    articles_map = {c : [] for c in _CATEGRORIES}
    csv = pd.read_csv(input_csv, encoding='utf-8')
    for row_num, row in csv.iterrows():
        has_type = 'Type' not in row or not row['Type'] or row['Type'] not in articles_map
        has_content = row['Name'] and row['Excerpt']
        if has_type and has_content:
            print()
            print(row_num + 1, '/', len(csv))
            
            if args.manual_article_type:
                c = get_article_type_manual(row['Name'], row['URL'], row['Excerpt'])
            else:
                if not set_openai_key:
                    with open('secrets/openai_api_key.txt', 'r') as f:
                        openai.api_key = f.read().strip()
                    with open('secrets/openai_org.txt', 'r') as f:
                        openai.organization = f.read().strip()
                    set_openai_key = True
                
                c = classify_article_type(row['Name'], row['URL'], row['Excerpt'])
                if c not in _CATEGRORIES:
                    print('Classified as:', c, 'which is not a valid category!')
                    c = get_article_type_manual(row['Name'], row['URL'], row['Excerpt'])
                
        else:
            c = row['Type']

        articles_map[c].append(row)

    logging.info('Populating content...')
    top_news = ''
    content = ''
    for c in _CATEGRORIES:
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
                    name, url, excerpt = item['Name'], item['URL'], item['Excerpt']
                    content += f'[{name}]({url}) - "{excerpt}"'
                    content += '\n\n'

    # remove the last two empty lines
    content = content[:-2]

    md = md_template.replace('$digest_number$', str(n)) \
                    .replace('$digest_number_english$', n_english) \
                    .replace('$top_news$', top_news) \
                    .replace('$content$', content)

    logging.info('Saving digest markdown...')
    with open(output_md, 'wb') as f:
        f.write(md.encode('utf-8'))

    logging.info('Done!')
