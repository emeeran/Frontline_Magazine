import os
import re
import pdfkit
from playwright.sync_api import sync_playwright, TimeoutError

def get_script_directory():
    return os.path.dirname(os.path.abspath(__file__))

def extract_article_content(url):
    script_dir = get_script_directory()
    
    if os.name == 'nt':  # Windows
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    else:
        wkhtmltopdf_path = "/usr/bin/wkhtmltopdf"  # Example path for Unix-based systems

    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        
        try:
            page.goto(url)
            article_content_selector = ".articlebodycontent.col-xl-9.col-lg-12.col-md-12.col-sm-12.col-12"
            title = page.query_selector("h1.title").inner_text()
            publish_time = page.query_selector(".publish-time").inner_text()
            paragraph_tags = page.query_selector_all(f"{article_content_selector} p")

            filtered_paragraphs = [
                tag.inner_text().strip()
                for tag in paragraph_tags
                if not any(
                    excluded_word in tag.inner_text().strip()
                    for excluded_word in ["Also Read", "COMMents", "Follow Us", "SHARE"]
                )
            ]

            browser.close()

            sanitized_title = re.sub(r'[<>:"/\|?*]', "_", title)  # Replace invalid characters with underscore

            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{sanitized_title}</title>
                <link rel="stylesheet" type="text/css" href="{os.path.join(script_dir, 'styles.css')}">
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

            directory = os.path.join(script_dir, "articles")
            os.makedirs(directory, exist_ok=True)

            pdf_filename = os.path.join(directory, f"{sanitized_title}.pdf")

            options = {
                "page-size": "A4",
                "margin-top": "2cm",
                "margin-right": "2cm",
                "margin-bottom": "2cm",
                "margin-left": "2cm",
            }
            
            pdfkit.from_string(html_content, pdf_filename, options=options, configuration=config)

            print(f"PDF file '{pdf_filename}' created successfully.")

        except TimeoutError:
            print("Timeout occurred while waiting for selector.")
            browser.close()

# Example usage:
url = input("Enter the URL: ")
extract_article_content(url)
