import os
import re
import base64
import argparse
import requests

import pandas as pd
import inflect

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from llm_utils import query_llm, web_fetch_summarize, MODEL_SONNET
from content_retrieval import get_arxiv_paper_contents, get_arxiv_pdf_bytes, get_reuters_article_content

# Constants
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

def summarize_article(url, title=None, lighting_round_story=False, save_image=False):
    """Generate a bullet point summary of a news article or research paper."""
    download_failed = False
    text = None
    pdf_bytes = None

    article = Article(url)
    try:
        article.download()
        article.parse()
        text = article.text
    except Exception as e:
        print(f'  newspaper download error: {e}')
        download_failed = True

    if 'arxiv' in url:
        text = get_arxiv_paper_contents(url)
        if text is None:
            print('  HTML/HuggingFace extraction failed, falling back to PDF...')
            pdf_bytes = get_arxiv_pdf_bytes(url)
        download_failed = False  # arxiv has its own extraction chain

    if not download_failed and save_image and article.has_top_image():
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

    if download_failed:
        return web_fetch_summarize(url, system_prompt, title=title)

    if pdf_bytes is not None:
        # Send the PDF directly to Claude
        user_content = [
            {
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": base64.standard_b64encode(pdf_bytes).decode("utf-8"),
                },
                "title": article.title,
            },
            {"type": "text", "text": f"Title: {article.title}\nPlease summarize this paper."},
        ]
    else:
        user_content = f"Title: {article.title}\nText: {text}"

    return query_llm([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_content}
    ])


def indent_lines(text, spaces=4):
    """Indent every non-empty line of text by the given number of spaces."""
    pad = ' ' * spaces
    return '\n'.join(pad + line if line.strip() else line for line in text.split('\n'))


def process_related_articles(related_articles_str):
    """Fetch and summarize related (sub-)stories from a comma-separated URL string.

    Returns a list of {'title', 'url', 'summary'} dicts (empty if none).
    """
    related_data = []

    if not related_articles_str or not isinstance(related_articles_str, str):
        return related_data

    related_urls = [url.strip() for url in related_articles_str.split(',') if url.strip()]

    for related_url in related_urls:
        # Try to recover a readable title for the outline; fall back to the URL.
        title = related_url
        try:
            related_article = Article(related_url)
            related_article.download()
            related_article.parse()
            if related_article.title:
                title = related_article.title
        except Exception as e:
            print(f'  newspaper failed for related article {related_url}: {e}')

        try:
            summary = summarize_article(related_url, title=title, lighting_round_story=True)
        except Exception as e:
            print(f'  failed to summarize related article {related_url}: {e}')
            summary = "Error :("

        related_data.append({'title': title, 'url': related_url, 'summary': summary})

    return related_data


def build_outline(articles_map, categories):
    """Build the outline section of the podcast notes."""
    parts = ['Outline:\n']

    def story_line(indent, name, url, related_articles):
        line = f'{indent}- [{name}]({url})'
        for related in related_articles:
            line += f' + [{related["title"]}]({related["url"]})'
        return line + '\n'

    for category in categories:
        parts.append(f'- {category}\n')
        main_stories, lighting_stories = articles_map[category]

        for name, url, summary, related_articles in main_stories:
            parts.append(story_line('   ', name, url, related_articles))

        parts.append('  - Lighting round\n')

        for name, url, summary, related_articles in lighting_stories:
            parts.append(story_line('       ', name, url, related_articles))

    return ''.join(parts)


def build_summaries(articles_map, categories):
    """Build the summaries section of the podcast notes."""
    parts = ['\n\n#Summaries\n\n']

    def append_story(name, url, summary, related_articles):
        parts.append(f'[{name}]({url})\n')
        parts.append(summary)
        parts.append('\n\n')
        # Nest each related story as an indented substory of the main story.
        for related in related_articles:
            parts.append(f'  - Related substory: [{related["title"]}]({related["url"]})\n')
            parts.append(indent_lines(related['summary'], spaces=4))
            parts.append('\n\n')

    for category in categories:
        main_stories, lighting_stories = articles_map[category]
        parts.append(f'## {category}')

        if len(main_stories) > 0:
            parts.append('\n\n')
            for name, url, summary, related_articles in main_stories:
                append_story(name, url, summary, related_articles)

        parts.append('\n### Lighting Round\n\n')

        if len(lighting_stories) > 0:
            for name, url, summary, related_articles in lighting_stories:
                append_story(name, url, summary, related_articles)

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
        summary = summarize_article(row['URL'], title=row['Name'], lighting_round_story=not is_main_story, save_image=is_main_story)
    except Exception as e:
        print(e)
        summary = "Error :("

    print('Summary:')
    print(summary)

    # Clean up title
    cleaned_name = row['Name'].replace("Title:", "")

    # Fetch and summarize any related stories so they can be nested under this one.
    related_articles = process_related_articles(row['Related Articles'])
    if related_articles:
        print(f'Found {len(related_articles)} related substor{"y" if len(related_articles) == 1 else "ies"}')

    return {
        'is_main': is_main_story,
        'category': category,
        'name': cleaned_name,
        'url': row['URL'],
        'summary': summary,
        'related_articles': related_articles
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