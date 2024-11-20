import os
import re
import logging
import argparse
import requests

import pandas as pd
import inflect
import openai

from newspaper import Article
from pathlib import Path
from datetime import date, timedelta
from tqdm.auto import tqdm

from tenacity import retry, stop_after_attempt, wait_random_exponential
from openai import OpenAI
with open('secrets/openai_api_key.txt', 'r') as f:
    _OPENAI_CLIENT = OpenAI(api_key=f.read().strip())
from content_retrieval import get_arxiv_paper_contents, get_reuters_article_content

_CATEGORIES = [
    'Tools & Apps',
    'Applications & Business',
    'Projects & Open Source',
    'Research & Advancements',
    'Policy & Safety',
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
def query_openai(messages, max_tokens=1000, model='gpt-4o'):
    return _OPENAI_CLIENT.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=max_tokens,
        temperature=0
    ).choices[0].message.content

def summarize_article(url, lighting_round_story=False, save_image=False):
    article = Article(url)
    article = Article(url)
    article.download()
    article.parse()
    text = article.text
    if 'arxiv' in url:
        text = get_arxiv_paper_contents(url)

    if save_image and article.has_top_image():
        im_response = requests.get(article.top_image)
        if im_response.status_code == 200:
            im_name = article.top_image.split("/")[-1]
            with open("images/"+im_name, "wb") as f:
                f.write(im_response.content)

    system_prompt = '''
Your task is to provide a bullet point summary of a news article or research paper about AI. Each bullet point should be no more than 2 sentences long. This summary will be used for the podcast Last Week in AI, in which the hosts summarize stories about AI in an accessible manner. We will provide the title and text contents of the article. Output the bullet points in markdown format.'''

    if lighting_round_story:
        system_prompt + " This story will be in a lighting round, so summarize it in no more than 10 bullet points, but still make sure to cover all the important details."
    else:
        system_prompt + " This will be covered as a main story, so produce a detailed summary covering all important details. Include at least 10 bullet points."
        
    system_prompt = system_prompt.strip()
    
    prompt = f'''
Title: {article.title}
Text: {text}
'''.strip()
    return query_openai([
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': prompt}
    ])

if __name__ == "__main__":
    with open('secrets/openai_api_key.txt', 'r') as f:
        openai.api_key = f.read().strip()

    articles_map = {c : ([],[]) for c in _CATEGORIES}
    related_articles_map = {}
    articles_map['other'] = ([],[])
    csv = pd.read_csv('news.csv', encoding='utf-8')
    num_picks = len(csv)
    pbar = tqdm(total=num_picks)

    for row_num, row in tqdm(csv.iterrows()):
        is_main_pick = row[STORY_TYPE_COL] == 'Main'
        category = SECTION_CATEGORY_MAPPINGS[row[STORY_SECTION_COL]]
        print('\nProcessing "%s"'%row['Name'])
        if is_main_pick:
            print("Type: Main story")
        else:
            print("Type: Lighting round story")
        print("Link: %s"%row['URL'])
        print("Category: %s"%category)
        try:
            summary = summarize_article(row['URL'],not is_main_pick, is_main_pick)
        except Exception as e:
            print(e)
            summary = "Error :("
        print('Summary:')
        print(summary)
        row['Name'] = row['Name'].replace("Title:","")
        if is_main_pick:
            articles_map[category][0].append([row['Name'],row['URL'],summary,row['Related Articles']])
        else:
            articles_map[category][1].append([row['Name'],row['URL'],summary,row['Related Articles']])
        print("")
        pbar.update(1)
    pbar.close()
        
    content = 'Outline:\n'
    
    for c in _CATEGORIES:
        content+="- "+c+"\n"
        items = articles_map[c]
        for item in items[0]:        
            name, url, summary, related_articles = item
            content += f'   - [{name}]({url})\n'
        content+="  - Lighting round\n"
        for item in items[1]: 
            name, url, summary, related_articles= item       
            content += f'       - [{name}]({url})\n'
            
    content +="\n\n#Summaries\n\n"
    for c in _CATEGORIES:
        items = articles_map[c]
        content += f'## {c}'
        if len(items[0]) > 0:
            content += '\n\n'
            for item in items[0]:
                name, url, summary, related_articles = item
                content += f'[{name}]({url})'
                content += '\n'
                content += summary
                content += "\n\n"
        content +="\n### Lighting Round\n\n"
        if len(items[1]) > 0:
            for item in items[1]:
                name, url, summary, related_articles = item
                content += f'[{name}]({url})'
                content += '\n'
                content += summary
                content += "\n\n"
                
    print(content)
    with open("summaries.md", 'wb') as f:
        f.write(content.encode('utf-8'))