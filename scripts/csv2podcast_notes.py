import os
import re
import argparse
import requests

import pandas as pd
import inflect

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from tenacity import retry, stop_after_attempt, wait_random_exponential
from openai import OpenAI
with open('secrets/openai_api_key.txt', 'r') as f:
    _OPENAI_CLIENT = OpenAI(api_key=f.read().strip())
from content_retrieval import get_arxiv_paper_contents, get_reuters_article_content

# Constants
DEFAULT_MAX_TOKENS = 4000
DEFAULT_MODEL = 'gpt-4o'
IMAGE_FOLDER = 'images'
OUTPUT_FILE = 'summaries.md'
INPUT_CSV = 'news.csv'

_CATEGORIES = [
    'Tools & Apps',
    'Applications & Business',
    'Projects & Open Source',
    'Policy & Safety',
    'Research & Advancements',
    'Synthetic Media & Art',
    'Fun!'
]

SECTION_CATEGORY_MAPPINGS = {
    "Tools/Apps": 'Tools & Apps',
    "Business/Applications":'Applications & Business',
    "OSS/Projects": 'Projects & Open Source',
    "Research/Advancements": 'Research & Advancements',
    "Policy/Safety": 'Policy & Safety',
    "Synthetic Media/Art": 'Synthetic Media & Art',
    "Fun!": 'Fun!'}
STORY_TYPE_COL = "Main Story or Lighting Round?"
STORY_SECTION_COL = "Section"

@retry(wait=wait_random_exponential(min=1, max=10), stop=stop_after_attempt(10))
def query_openai(messages, max_tokens=DEFAULT_MAX_TOKENS, model=DEFAULT_MODEL):
    """Query OpenAI API with retry logic."""
    return _OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    ).choices[0].message.content

def summarize_article(url, lighting_round_story=False, save_image=False):
    """Generate a bullet point summary of a news article or research paper."""
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    if 'arxiv' in url:
        text = get_arxiv_paper_contents(url)

    if save_image and article.has_top_image():
        image_response = requests.get(article.top_image)
        if image_response.status_code == 200:
            image_name = article.top_image.split("/")[-1]
            image_folder_path = Path(IMAGE_FOLDER)
            image_folder_path.mkdir(parents=True, exist_ok=True)
            image_path = image_folder_path / image_name
            with open(image_path, "wb") as image_file:
                image_file.write(image_response.content)

    system_prompt = '''
Your task is to provide a bullet point summary of a news article or research paper about AI. Each bullet point should be no more than 2 sentences long. This summary will be used for the podcast Last Week in AI, in which the hosts summarize stories about AI in an accessible manner. We will provide the title and text contents of the article. Output in markdown format.'''

    if lighting_round_story:
        system_prompt += " This story will be in a lighting round, so summarize it in no more than 10 bullet points, but still make sure to cover all the important details. Don't cover background or implications, just the details of the news."
    else:
        system_prompt += " This will be covered as a main story, so produce a detailed summary covering all important details. Don't cover background or implications, just the details of the news. Don't use sections like '##', just use bullet points. Do not use bold text. Be concise but thorough. If summarizing a paper, be sure to explain the key findings and results, don't be afraid to get detailed."

    system_prompt = system_prompt.strip()
    
    prompt = f'''
Title: {article.title}
Text: {text}
'''.strip()
    return query_openai([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ])


def build_outline(articles_map, categories):
    """Build the outline section of the podcast notes."""
    parts = ['Outline:\n']

    for category in categories:
        parts.append(f'- {category}\n')
        main_stories, lighting_stories = articles_map[category]

        for name, url, summary, related_articles in main_stories:
            parts.append(f'   - [{name}]({url})\n')

        parts.append('  - Lighting round\n')

        for name, url, summary, related_articles in lighting_stories:
            parts.append(f'       - [{name}]({url})\n')

    return ''.join(parts)


def build_summaries(articles_map, categories):
    """Build the summaries section of the podcast notes."""
    parts = ['\n\n#Summaries\n\n']

    for category in categories:
        main_stories, lighting_stories = articles_map[category]
        parts.append(f'## {category}')

        if len(main_stories) > 0:
            parts.append('\n\n')
            for name, url, summary, related_articles in main_stories:
                parts.append(f'[{name}]({url})\n')
                parts.append(summary)
                parts.append('\n\n')

        parts.append('\n### Lighting Round\n\n')

        if len(lighting_stories) > 0:
            for name, url, summary, related_articles in lighting_stories:
                parts.append(f'[{name}]({url})\n')
                parts.append(summary)
                parts.append('\n\n')

    return ''.join(parts)


def process_csv_row(row):
    """Process a single CSV row and return article data."""
    is_main_story = row[STORY_TYPE_COL] == 'Main'
    category = SECTION_CATEGORY_MAPPINGS[row[STORY_SECTION_COL]]

    print(f'\nProcessing "{row["Name"]}"')
    print(f'Type: {"Main story" if is_main_story else "Lighting round story"}')
    print(f'Link: {row["URL"]}')
    print(f'Category: {category}')

    try:
        summary = summarize_article(row['URL'], not is_main_story, is_main_story)
    except Exception as e:
        print(e)
        summary = "Error :("

    print('Summary:')
    print(summary)

    # Clean up title
    cleaned_name = row['Name'].replace("Title:", "")

    return {
        'is_main': is_main_story,
        'category': category,
        'name': cleaned_name,
        'url': row['URL'],
        'summary': summary,
        'related_articles': row['Related Articles']
    }


if __name__ == "__main__":
    # Initialize articles map: {category: ([main_stories], [lighting_stories])}
    articles_map = {category: ([], []) for category in _CATEGORIES}
    articles_map['other'] = ([], [])

    # Read and process CSV
    csv_data = pd.read_csv(INPUT_CSV, encoding='utf-8')

    print(f'Processing {len(csv_data)} articles...')
    for row_num, row in tqdm(csv_data.iterrows(), total=len(csv_data)):
        article_data = process_csv_row(row)

        # Add to appropriate category and story type
        category = article_data['category']
        article_info = [
            article_data['name'],
            article_data['url'],
            article_data['summary'],
            article_data['related_articles']
        ]

        if article_data['is_main']:
            articles_map[category][0].append(article_info)
        else:
            articles_map[category][1].append(article_info)

        print("")

    # Build content using helper functions
    outline = build_outline(articles_map, _CATEGORIES)
    summaries = build_summaries(articles_map, _CATEGORIES)
    content = outline + summaries

    # Output results
    print(content)
    with open(OUTPUT_FILE, 'wb') as output_file:
        output_file.write(content.encode('utf-8'))

    print(f'\nPodcast notes saved to {OUTPUT_FILE}')