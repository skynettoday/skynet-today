import os
import re
import requests
from PIL import Image
from io import BytesIO
from collections import defaultdict

def extract_top_news_and_images(content):
    top_news_pattern = r'### Top News\n\n(.*?)(\n### |\Z)'
    top_news_match = re.search(top_news_pattern, content, re.DOTALL)
    if top_news_match:
        top_news_section = top_news_match.group(1).strip()
        articles_and_images = re.findall(r'#### \[(.*?)\]\((.*?)\)\s*!\[.*?\]\((.*?)\)', top_news_section)
        return articles_and_images
    return []

def month_name(month_number):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return months[int(month_number) - 1]

def download_and_resize_images(image_urls, max_width, max_height):
    images = []
    for url in image_urls:
        try:
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img.thumbnail((max_width, max_height))
            images.append(img)
        except Exception as e:
            print(f"Error downloading or processing image {url}: {e}")
    return images

def create_collage(images, output_path):
    rows = (len(images) + 2) // 3  # Arrange up to 3 images per row
    cols = min(len(images), 3)

    # Correctly calculate the shortest height in each row
    heights_per_row = [min(img.size[1] for img in images[i * cols:(i + 1) * cols]) for i in range(rows)]
    total_height = sum(heights_per_row)
    max_width = max(img.size[0] for img in images) * cols

    collage = Image.new('RGB', (max_width, total_height), (255, 255, 255))  # RGB with white background

    y_offset = 0
    for row in range(rows):
        x_offset = (max_width - sum(img.size[0] * (heights_per_row[row] / img.size[1]) for img in images[row * cols:(row + 1) * cols])) // 2  # Centering each row
        for img in images[row * cols:(row + 1) * cols]:
            new_height = heights_per_row[row]
            new_width = int(img.size[0] * (new_height / img.size[1]))
            resized_img = img.resize((new_width, new_height), Image.LANCZOS)

            collage.paste(resized_img, (int(x_offset), int(y_offset)))
            x_offset += resized_img.size[0]
        y_offset += heights_per_row[row]

    collage.save(output_path, "JPEG")
    print(f"Collage image saved at {output_path}")


def parse_markdown_files(directory):
    news_by_month = defaultdict(list)
    images_by_month = defaultdict(list)
    for filename in os.listdir(directory):
        if filename.endswith('.md') and filename.startswith('2023'):
            file_path = os.path.join(directory, filename)
            with open(file_path, 'r') as file:
                content = file.read()
            date_match = re.match(r'2023-(\d{2})-\d{2}-(\d+).md', filename)
            if date_match:
                month = date_match.group(1)
                week_number = date_match.group(2)
                articles_and_images = extract_top_news_and_images(content)
                if articles_and_images:
                    news_by_month[month].append((week_number, [item[:2] for item in articles_and_images]))
                    images_by_month[month].extend([item[2] for item in articles_and_images])
    return news_by_month, images_by_month

def generate_summary_markdown(news_by_month, images_by_month, output_file_path, img_directory):
    with open(output_file_path, 'w') as file:        
        file.write("---\nlayout: post\ntitle: \"AI News in 2023: a Digest\"\n")
        file.write("excerpt: \"An overview of the big AI-related stories from 2023\"\n---\n")
        file.write("## Overview\n\nWith 2023 over, we reflect on what's happened in AI during this year.\n\n")

        for month, news_items in sorted(news_by_month.items()):
            month_name_str = month_name(month)
            print(month_name_str)
            print(news_items)
            image_urls = images_by_month[month]
            resized_images = download_and_resize_images(image_urls, 300, 300)  # Resize images to a max of 300x300
            collage_image_path = f"{img_directory}/collage_{month_name_str}.jpg"
            create_collage(resized_images, collage_image_path)

            file.write(f"## {month_name_str}\n\n")
            file.write("<figure>\n <img class=\"postimage_50\" src=\"{{ site.imgpath }}/"+collage_image_path+'"/>\n')
            file.write(" <figcaption>[Image Caption]</figcaption>\n</figure>\n\n")
            
            file.write("\n**Our Short Summary**: [Editorial text summarizing the main events of the month.]\n\n")
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


    return output_file_path

def main(directory, output_file_path, img_directory):
    news_by_month, images_by_month = parse_markdown_files(directory)
    summary_file_path = generate_summary_markdown(news_by_month, images_by_month, output_file_path, img_directory)
    print(f"Summary markdown file generated at: {summary_file_path}")


# To use this script, specify the directory of markdown files and the output path for the summary file.
# For example:
# main('/path/to/markdown/files', '/path/to/output/2023-summary.md')
main("_posts/digests","_posts/overviews/2023-12-23-2023-summary.md", "assets/img/overviews/2023-12-23-2023-summary")