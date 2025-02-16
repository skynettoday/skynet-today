import requests
from bs4 import BeautifulSoup
from collections import OrderedDict
import re

def arxiv_to_html(url: str) -> str:
    paper_id = url[url.find('abs/') + 4:].strip('/').strip()
    if paper_id:
        return f"https://arxiv.org/html/{paper_id}"
    else:
        return url

def arxiv_to_huggingface(url: str) -> str:
    match = re.search(r"https://arxiv.org/abs/(\d+\.\d+)(?:v\d+)?", url)
    if match:
        return f"https://huggingface.co/papers/{match.group(1)}"
    else:
        return url

def get_arxiv_paper_contents_html(url):
    def remove_unwanted_tags(content, tags_to_remove):
        """ Removes specified tags from the content but keeps their text. """
        for tag in tags_to_remove:
            for sub_tag in content.find_all(tag):
                sub_tag.replace_with(sub_tag.get_text())
        return content

    def extract_text_by_section_ordered(soup):
        extracted_text = OrderedDict()
        current_section = None

        for element in soup.descendants:
            if element.name == 'h2':
                current_section = element.get_text(strip=True)
                if current_section!="Abstract":
                    current_section = current_section[1:]
                extracted_text[current_section] = ''
            elif element.name == 'p' and current_section:
                cleaned_element = remove_unwanted_tags(element, ['cite', 'a', 'span'])
                extracted_text[current_section] += cleaned_element.get_text(separator='', strip=False) + '\n'
        return extracted_text
    html_url = arxiv_to_html(url)
    response = requests.get(html_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        title = soup.title.string
    except:
        title = ''
    section_texts = extract_text_by_section_ordered(soup)
    introduction = section_texts.get('Introduction')
    if not introduction:
        return None
    text = f"# Introduction:\n{introduction}"
    if 'Approach' in section_texts:
        text+=f"\n\n# Approach\n{section_texts.get('Approach')}"
    if 'Experiment' in section_texts:
        text+=f"\n\n# Experiment\n{section_texts.get('Experiment')}"
    if 'Discussion' in section_texts:
        text+=f"\n\n# Discussion\n{section_texts.get('Discussion')}"
    return text


def get_arxiv_paper_contents_huggingface(url):
    hf_url = arxiv_to_huggingface(url)
    response = requests.get(hf_url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.h1.text
    abstract = soup.p.text
    return f'Title: {title}\n\nAbstract:\n{abstract}'


def get_arxiv_paper_contents(url):
    text = None
    try:
        text = get_arxiv_paper_contents_html(url)
    except Exception as e:
        print(e)
    if text is None:
        text = get_arxiv_paper_contents_huggingface(url)
    return text        


def get_reuters_article_content(url):
    """
    Extracts the content of a Reuters article from its URL.

    :param url: URL of the Reuters article.
    :return: Plain text string of the article contents, without HTML tags.
    """
    # Fetch the HTML content from the URL
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the div with a class that starts with "article-body__container"
    article_body = soup.find('div', class_=lambda value: value and value.startswith('article-body__container'))

    # Extract and return the text content, if the div is found
    if article_body:
        return article_body.get_text(strip=True)
    else:
        return "Article content not found."


if __name__ == '__main__':
    url = "https://browse.arxiv.org/html/2401.02117v1"
    result = extract_title_abstract_introduction(url)

    print(result)

