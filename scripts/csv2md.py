import os
import logging
import argparse
from collections import Counter

import pandas as pd
import inflect


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

_CATEGRORIES = [
    'Mini Briefs',
    'Advances & Business',
    'Concerns & Hype',
    'Analysis & Policy',
    'Expert Opinions & Discussion within the field',
    'Explainers'
]


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('--template_file', '-tf', type=str, default='digest_template.md')
    parser.add_argument('--digest_number', '-n', type=int, required=True)
    parser.add_argument('--input_csv', '-i', type=str, required=True)
    parser.add_argument('--output_md', '-o', type=str, required=True)
    parser.add_argument('--force_overwrite', '-f', action='store_true')
    args = parser.parse_args()

    n = args.digest_number
    p = inflect.engine()
    n_english = p.number_to_words(p.ordinal(n))
    logging.info('Parsing for the {} digest'.format(n_english))

    logging.info('Will save result to {}'.format(args.output_md))
    if os.path.isfile(args.output_md):
        if not args.force_overwrite:
            raise ValueError('Cannot overwrite existing output file!')

    logging.info('Loading template from {}'.format(args.template_file))
    with open(args.template_file, 'r') as f:
        md_template = f.read()

    logging.info('Reading {}'.format(args.input_csv))
    articles_map = {c : [] for c in _CATEGRORIES}
    csv = pd.read_csv(args.input_csv)
    for row_num, row in csv.iterrows():
        if not row['Type']:
            print()
            print('To which category does this article belong?')
            print()
            print(row['Name'])
            print()
            
            for i, c in enumerate(_CATEGRORIES):
                print('{}) {}'.format(i, c))
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
    content = ''
    for c in _CATEGRORIES:
        items = articles_map[c]
        if len(items) > 0:
            content += '### {}\n'.format(c)
            content += '\n'

            for item in items:
                if c == 'Mini Briefs':
                    content += '#### [{}]({})\n'.format(item['Name'], item['URL'])
                    content += '\n'
                    content += '<one-two paragraph brief>\n'
                else:
                    content += '* [{}]({}) - {}\n'.format(item['Name'], item['URL'], item['Excerpt'])

                content += '\n'
    
    # remove the last two empty lines
    content = content[:-2]

    md = md_template.replace('$digest_number$', str(n)) \
                    .replace('$digest_number_english$', n_english) \
                    .replace('$content$', content)

    logging.info('Saving digest markdown...')
    with open(args.output_md, 'w') as f:
        f.write(md)

    logging.info('Done!')
