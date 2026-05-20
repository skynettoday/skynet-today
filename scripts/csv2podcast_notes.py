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
        summary = summarize_article(row['URL'], title=row['Name'], lighting_round_story=not is_main_story, save_image=is_main_story)
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


FINAL_POLISH_MAX_TOKENS = 16000

def final_polish_podcast_notes(markdown_content):
    system_prompt = '''
You are an expert editor for the "Last Week in AI" podcast. Your task is to polish the final podcast show notes to ensure they're ready for the hosts to use.

Please review the entire document and make the following improvements:

1. **Remove duplicate stories**: If the same story appears multiple times (same URL or very similar content), keep only the best version and remove duplicates.

2. **Vary bullet point starters**: Look at all the bullet points and ensure they don't start with repetitive words/phrases. Rewrite to have more varied and engaging openings while maintaining the same factual content.

3. **Overall polish**:
   - Ensure consistent formatting across all summaries
   - Fix any grammatical errors
   - Improve clarity and readability for spoken delivery
   - Ensure bullet points are concise and easy to read aloud

4. **Maintain accuracy**: Do not change any URLs, article titles, or factual content. Only improve the presentation and remove duplicates.

Return the polished markdown content. Keep all the original structure and formatting intact, just improve the quality and remove any issues.
Just output the polished markdown content, with no additional explanations or comments.'''.strip()

    return query_llm([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': markdown_content}
    ], max_tokens=FINAL_POLISH_MAX_TOKENS)


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

    # Final polish pass (summaries only)
    print('\nApplying final polish to podcast notes...')
    polished_summaries = final_polish_podcast_notes(summaries)
    content = outline + polished_summaries

    # Output results
    print(content)
    with open(OUTPUT_FILE, 'wb') as output_file:
        output_file.write(content.encode('utf-8'))

    print(f'\nPodcast notes saved to {OUTPUT_FILE}')