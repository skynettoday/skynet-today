import requests
from bs4 import BeautifulSoup
from collections import OrderedDict

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

def extract_title_abstract_introduction(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    title = soup.title.string if soup.title else "Title not found"
    section_texts = extract_text_by_section_ordered(soup)
    abstract = section_texts.get('Abstract', 'Abstract not found')
    introduction = section_texts.get('Introduction', 'Introduction not found')

    return f"Title: {title}\n\nAbstract:\n{abstract}\n\nIntroduction:\n{introduction}"

if __name__ == '__main__':
    url = "https://browse.arxiv.org/html/2401.02117v1"
    result = extract_title_abstract_introduction(url)

    print(result)

