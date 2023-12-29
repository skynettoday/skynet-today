import os
import re
import requests
from PIL import Image
from io import BytesIO
from collections import defaultdict
from newspaper import Article
from multiprocessing.dummy import Pool
from tqdm import tqdm


def apply_map_batch(func, args_list):
    pool = Pool(os.cpu_count())
    promises = [pool.apply_async(func, args) for args in args_list]

    results = [None] * len(promises)
    done_idxs = set()
    pbar = tqdm(total=len(promises))
    while len(done_idxs) < len(promises):
        for idx, promise in enumerate(promises):
            if idx not in done_idxs and promise.ready():
                done_idxs.add(idx)
                results[idx] = promise.get()
                pbar.update(1)
    return results


def extract_top_news_article_names_and_links(content):
    top_news_pattern = r'### Top News\n\n(.*?)(\n### |\Z)'
    top_news_match = re.search(top_news_pattern, content, re.DOTALL)
    if top_news_match:
        top_news_section = top_news_match.group(1).strip()
        articles_names_links = re.findall(r'#### \[(.*?)\]\((.*?)\)', top_news_section)
        return articles_names_links    
    return []


def month_name(month_number):
    months = ["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
    return months[int(month_number) - 1]


def download_and_resize_image(url, max_width, max_height):
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((max_width, max_height))
        return img
    except Exception as e:
        print(f"Error downloading or processing image {url}: {e}")


def create_collage(images, img_directory, month):
    month_name_str = month_name(month)
    collage_image_path = f"{img_directory}/collage_{month_name_str}.jpg"

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

    collage.save(collage_image_path, "JPEG")
    print(f"Collage image saved at {collage_image_path}")
    return collage_image_path


def parse_markdown_files(directory):
    news_by_month = defaultdict(list)
    for filename in os.listdir(directory):
        for month in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']:
            prefix = f'2023-{month}'
            if filename.endswith('.md') and filename.startswith(prefix):
                file_path = os.path.join(directory, filename)
                with open(file_path, 'r') as file:
                    content = file.read()
                date_match = re.search(r"-?\d+-(\d+)\..*", filename.removeprefix(prefix))
                if date_match:
                    week_number = date_match.group(1)
                    article_names_and_links = extract_top_news_article_names_and_links(content)
                    if article_names_and_links:
                        news_by_month[month].append((week_number, [item[:2] for item in article_names_and_links]))
    return news_by_month


def generate_summary_markdown(news_by_month, collage_image_path_by_month, output_file_path):
    with open(output_file_path, 'w') as file:
        file.write("---\nlayout: post\ntitle: \"AI News in 2023: a Digest\"\n")
        file.write("excerpt: \"An overview of the big AI-related stories from 2023\"\n---\n")
        file.write("## Overview\n\nWith 2023 over, we reflect on what's happened in AI during this year.\n\n")

        for month, news_items in sorted(news_by_month.items()):
            month_name_str = month_name(month)
            print(month_name_str)
            print(news_items)
            collage_image_path = collage_image_path_by_month[month]

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


def get_article_image(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        if article.has_top_image():
            return download_and_resize_image(article.top_image, 300, 300)
    except:
        pass
    return None


def main(directory, output_file_path, img_directory):
    news_by_month = parse_markdown_files(directory)
    images_by_month = defaultdict(list)
    for month, issues in news_by_month.items():
        urls = []
        for issue in issues:
            for article in issue[1]:
                urls.append(article[1])
        ims = apply_map_batch(get_article_image, [(url,) for url in urls])
        ims = [im for im in ims if im]
        images_by_month[month].extend(ims)

    collage_image_path_by_month = {}
    for month, ims in images_by_month.items():
        collage_image_path_by_month[month] = create_collage(ims, img_directory, month)

    summary_file_path = generate_summary_markdown(news_by_month, collage_image_path_by_month, output_file_path)
    print(f"Summary markdown file generated at: {summary_file_path}")


# To use this script, specify the directory of markdown files and the output path for the summary file.
# For example:
# main('/path/to/markdown/files', '/path/to/output/2023-summary.md')
main("_posts/digests","_posts/overviews/2023-12-30-2023-summary.md", "assets/img/overviews/2023-12-30-2023-summary")