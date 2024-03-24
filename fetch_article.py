from playwright.sync_api import sync_playwright, TimeoutError
from datetime import datetime
import re

def extract_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url)
            article_content_selector = '.articlebodycontent.col-xl-9.col-lg-12.col-md-12.col-sm-12.col-12'
            page.wait_for_selector(article_content_selector, timeout=10000)  # Increased timeout value to 10 seconds
            title = page.query_selector('h1.title').inner_text()
            publish_time = page.query_selector('.publish-time').inner_text()
            paragraph_tags = page.query_selector_all(f"{article_content_selector} p")
            
            # Filter out unwanted elements
            filtered_paragraphs = []
            for tag in paragraph_tags:
                text = tag.inner_text().strip()
                if text and not any(excluded_word in text for excluded_word in ['Also Read', 'COMMents', 'Follow Us', 'SHARE']):
                    filtered_paragraphs.append(text)
            
            browser.close()
            
            # Sanitize title for filename
            sanitized_title = re.sub(r'[<>:"/\\|?*]', '', title)  # Remove invalid characters
            
            # Create HTML content
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>{sanitized_title}</title>
                <style>
                    /* Add your CSS styles here */
                    body {{
                        font-family: Arial, sans-serif;
                        line-height: 1.6;
                        margin: 20px;
                    }}
                    .article-title {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }}
                    .publish-time {{
                        font-style: italic;
                        color: #888;
                    }}
                    .article-content {{
                        margin-top: 20px;
                    }}
                    .article-content p {{
                        margin-bottom: 10px;
                    }}
                </style>
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
            
            # Save HTML content to a file
            filename = f"{sanitized_title}.html"
            with open(filename, "w", encoding="utf-8") as file:
                file.write(html_content)
                
            print(f"HTML file '{filename}' created successfully.")
            
        except TimeoutError:
            print("Timeout occurred while waiting for selector.")
            browser.close()

# Example usage:
url = input("Enter the URL: ")
extract_article_content(url)
