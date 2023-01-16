import os
import logging
import argparse

import pandas as pd
import inflect

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


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template_website.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=False, default='')
    parser.add_argument('--output_md', '-o', type=str, required=False)
    parser.add_argument('--force_overwrite', '-f', action='store_true')
    args = parser.parse_args()

    n = args.digest_number
    p = inflect.engine()
    n_english = p.number_to_words(p.ordinal(n)).replace(' ', '-')
    logging.info(f'Parsing for the {n_english} digest')

    output_md = args.output_md
    if output_md is None:
        output_md = f'{n}.md'

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

    logging.info(f'Reading {input_csv}')
    articles_map = {c : [] for c in _CATEGRORIES}
    csv = pd.read_csv(input_csv, encoding='utf-8')
    for row_num, row in csv.iterrows():
        has_type = 'Type' not in row or not row['Type'] or row['Type'] not in articles_map
        has_content = row['Name'] and row['Excerpt']
        if has_type and has_content:
            print()
            print(row_num + 1, '/', len(csv))
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
