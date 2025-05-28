import os
import re
from playwright.sync_api import sync_playwright, TimeoutError

def extract_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            page.goto(url)
            
            # Try multiple possible selectors for title
            title_selectors = ["h1.title", "h1", ".article-title", ".headline", ".story-title"]
            title = None
            for selector in title_selectors:
                title_element = page.query_selector(selector)
                if title_element:
                    title = title_element.inner_text()
                    break
            
            if not title:
                title = "Untitled Article"
            
            # Try multiple possible selectors for publish time
            time_selectors = [".publish-time", ".published-date", ".date", ".timestamp"]
            publish_time = None
            for selector in time_selectors:
                time_element = page.query_selector(selector)
                if time_element:
                    publish_time = time_element.inner_text()
                    break
            
            if not publish_time:
                from datetime import datetime
                publish_time = f"Extracted on {datetime.now().strftime('%B %d, %Y')}"
            
            # Try multiple possible selectors for article content
            content_selectors = [
                ".articlebodycontent.col-xl-9.col-lg-12.col-md-12.col-sm-12.col-12 p",
                ".article-content p",
                ".story-content p",
                ".content p",
                ".entry-content p",
                "article p"
            ]
            
            paragraph_tags = []
            for selector in content_selectors:
                paragraph_tags = page.query_selector_all(selector)
                if paragraph_tags:
                    break

            # Filter out unwanted elements using list comprehension
            excluded_words = ["Also Read", "COMMents", "Follow Us", "SHARE"]
            filtered_paragraphs = [tag.inner_text().strip() for tag in paragraph_tags if all(excluded_word not in tag.inner_text().strip() for excluded_word in excluded_words)]

            browser.close()

            sanitized_title = re.sub(r'[<>:"/\|?*]', "_", title)  # Sanitize title for filename

            # Create Markdown content
            markdown_content = f"""# {title}

**Published:** {publish_time}

---

{chr(10).join(paragraph for paragraph in filtered_paragraphs)}

---

*Source: {url}*
"""

            directory = "./articles/"
            os.makedirs(directory, exist_ok=True)

            filename = os.path.join(directory, f"{sanitized_title}.md")
            with open(filename, "w", encoding="utf-8") as file:
                file.write(markdown_content)

            print(f"Markdown file '{filename}' created successfully.")

        except TimeoutError:
            print("Timeout occurred while waiting for selector.")
            browser.close()

# Example usage:
url = input("Enter the URL: ")
extract_article_content(url)
