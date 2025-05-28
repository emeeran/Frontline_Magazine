import os
import re
from playwright.sync_api import sync_playwright, TimeoutError

def extract_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(url)
            article_content_selector = ".articlebodycontent.col-xl-9.col-lg-12.col-md-12.col-sm-12.col-12"
            title = page.query_selector("h1.title").inner_text()
            publish_time = page.query_selector(".publish-time").inner_text()
            paragraph_tags = page.query_selector_all(f"{article_content_selector} p")

            # Filter out unwanted elements using list comprehension
            excluded_words = ["Also Read", "COMMents", "Follow Us", "SHARE"]
            filtered_paragraphs = [tag.inner_text().strip() for tag in paragraph_tags if all(excluded_word not in tag.inner_text().strip() for excluded_word in excluded_words)]

            browser.close()

            sanitized_title = re.sub(r'[<>:"/\|?*]', "_", title)  # Sanitize title for filename

            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{sanitized_title}</title>
                <link rel="stylesheet" type="text/css" href="styles.css">
            </head>
            <body>
                <div class="article-title">{sanitized_title}</div>
                <div class="publish-time">{publish_time}</div>
                <div class="article-content">
                    {''.join(f"<p>{paragraph}</p>" for paragraph in filtered_paragraphs)}
                </div>
            </body>
            </html>
            """

            directory = "./articles/"
            os.makedirs(directory, exist_ok=True)

            filename = os.path.join(directory, f"{sanitized_title}.html")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_content)

            print(f"HTML file '{filename}' created successfully.")

        except TimeoutError:
            print("Timeout occurred while waiting for selector.")
            browser.close()

# Example usage:
url = input("Enter the URL: ")
extract_article_content(url)
