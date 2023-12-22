import os
import re
from collections import defaultdict

def extract_top_news(content):
    """
    Extracts individual articles from the 'Top News' section in the markdown content.
    The format is:
        "#### [Title](link)"
    """
    top_news_pattern = r'### Top News\n\n(.*?)(\n### |\Z)'
    top_news_match = re.search(top_news_pattern, content, re.DOTALL)
    if top_news_match:
        top_news_section = top_news_match.group(1).strip()
        articles = re.findall(r'#### \[(.*?)\]\((.*?)\)', top_news_section)
        print(articles)
        return articles
    return []

def parse_markdown_files(directory):
    news_by_month = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith('.md') and filename.startswith('2023'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()
            
            date_match = re.match(r'2023-(\d{2})-\d{2}-(\d+).md', filename)
            if date_match:
                month = date_match.group(1)
                week_number = date_match.group(2)
                top_news = extract_top_news(content)
                if top_news:
                    news_by_month[month].append((week_number, top_news))

    return news_by_month

def month_name(month_number):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return months[int(month_number) - 1]

def generate_summary_markdown(news_by_month, output_file_path):
    with open(output_file_path, 'w') as file:
        # ... [initial content writing code] ...

        for month, news_items in sorted(news_by_month.items()):
            month_name_str = month_name(month)
            file.write(f"## {month_name_str}\n\n")
            # ... [image and caption writing code] ...

            file.write("**Newsletter links**: ")
            week_count = 1
            newsletter_links = []
            for week_number, _ in sorted(news_items, key=lambda x: int(x[0])):
                newsletter_links.append(f"[Week {week_count}](https://lastweekin.ai/p/{week_number})")
                week_count += 1
            file.write(" | ".join(newsletter_links) + " <br>\n**Highlights**:\n")
            for week_number, articles in sorted(news_items, key=lambda x: int(x[0])):
                for title, link in articles:
                    file.write(f"* [{title}]({link})\n")

            file.write("\n**Our Short Summary**: [Editorial text summarizing the main events of the month.]\n\n")

    return output_file_path

def main(directory, output_file_path):
    news_by_month = parse_markdown_files(directory)
    summary_file_path = generate_summary_markdown(news_by_month, output_file_path)
    print(f"Summary markdown file generated at: {summary_file_path}")


# To use this script, specify the directory of markdown files and the output path for the summary file.
# For example:
# main('/path/to/markdown/files', '/path/to/output/2023-summary.md')
main("_posts/digests","_posts/overviews/2023-summary.md")