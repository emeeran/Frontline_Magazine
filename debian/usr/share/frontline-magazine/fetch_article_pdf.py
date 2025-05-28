import os
import re
import pdfkit
from playwright.sync_api import sync_playwright, TimeoutError


def extract_article_content(url):
    # Specify the path to wkhtmltopdf executable
    # Use 'which wkhtmltopdf' to find the path, or None to use system PATH
    try:
        import subprocess
        wkhtmltopdf_path = subprocess.check_output(['which', 'wkhtmltopdf']).decode().strip()
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
    except:
        # Fall back to system PATH
        config = pdfkit.configuration()

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url)
            article_content_selector = (
                ".articlebodycontent.col-xl-9.col-lg-12.col-md-12.col-sm-12.col-12"
            )
            title = page.query_selector("h1.title").inner_text()
            publish_time = page.query_selector(".publish-time").inner_text()
            paragraph_tags = page.query_selector_all(f"{article_content_selector} p")

            # Filter out unwanted elements using list comprehension
            filtered_paragraphs = [
                tag.inner_text().strip()
                for tag in paragraph_tags
                if not any(
                    excluded_word in tag.inner_text().strip()
                    for excluded_word in ["Also Read", "COMMents", "Follow Us", "SHARE"]
                )
            ]

            browser.close()

            # Sanitize title for filename
            sanitized_title = re.sub(
                r'[<>:"/\\|?*]', "", title
            )  # Remove invalid characters

            # Create beautifully formatted HTML content for PDF
            html_content = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <title>{sanitized_title}</title>
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Georgia:ital,wght@0,400;0,700;1,400&display=swap');
                    
                    body {{
                        font-family: 'Georgia', 'Times New Roman', serif;
                        line-height: 1.8;
                        margin: 0;
                        padding: 40px;
                        color: #2c3e50;
                        background-color: #ffffff;
                        font-size: 12pt;
                    }}
                    
                    .header {{
                        border-bottom: 3px solid #3498db;
                        margin-bottom: 30px;
                        padding-bottom: 20px;
                    }}
                    
                    .article-title {{
                        font-size: 28pt;
                        font-weight: 700;
                        color: #2c3e50;
                        margin-bottom: 15px;
                        line-height: 1.3;
                    }}
                    
                    .publish-time {{
                        font-style: italic;
                        color: #7f8c8d;
                        font-size: 11pt;
                        margin-bottom: 10px;
                    }}
                    
                    .source {{
                        color: #3498db;
                        font-weight: 600;
                        font-size: 10pt;
                        text-transform: uppercase;
                        letter-spacing: 1px;
                    }}
                    
                    .article-content {{
                        margin-top: 30px;
                    }}
                    
                    .article-content p {{
                        margin-bottom: 18px;
                        text-align: justify;
                        text-indent: 1.5em;
                        orphans: 2;
                        widows: 2;
                    }}
                    
                    .article-content p:first-child {{
                        text-indent: 0;
                        font-weight: 500;
                        font-size: 13pt;
                    }}
                    
                    /* Print-specific styles */
                    @media print {{
                        body {{
                            margin: 0;
                            padding: 30px;
                        }}
                        
                        .header {{
                            page-break-after: avoid;
                        }}
                        
                        .article-content p {{
                            page-break-inside: avoid;
                        }}
                    }}
                    
                    /* Page footer for PDF */
                    .footer {{
                        position: fixed;
                        bottom: 20px;
                        right: 30px;
                        font-size: 9pt;
                        color: #bdc3c7;
                    }}
                </style>
            </head>
            <body>
                <div class="header">
                    <div class="source">Frontline Magazine</div>
                    <h1 class="article-title">{sanitized_title}</h1>
                    <div class="publish-time">{publish_time}</div>
                </div>
                
                <div class="article-content">
                    {''.join(f"<p>{paragraph}</p>" for paragraph in filtered_paragraphs)}
                </div>
                
                <div class="footer">
                    Extracted from Frontline Magazine
                </div>
            </body>
            </html>
            """

            # Save PDF file in the ./articles directory
            directory = "./articles/"
            os.makedirs(
                directory, exist_ok=True
            )  # Create directory if it doesn't exist
            pdf_filename = os.path.join(directory, f"{sanitized_title}.pdf")

            # Enhanced PDF generation options for professional formatting
            options = {
                "page-size": "A4",
                "margin-top": "2.5cm",
                "margin-right": "2cm", 
                "margin-bottom": "2.5cm",
                "margin-left": "2cm",
                "encoding": "UTF-8",
                "no-outline": None,
                "enable-local-file-access": None,
                "print-media-type": None,
                "disable-smart-shrinking": None,
                "dpi": 300,
                "image-quality": 100,
                "zoom": 1.0,
            }
            pdfkit.from_string(
                html_content, pdf_filename, options=options, configuration=config
            )

            print(f"PDF file '{pdf_filename}' created successfully.")

        except TimeoutError:
            print("Timeout occurred while waiting for selector.")
            browser.close()


# Example usage:
url = input("Enter the URL: ")
extract_article_content(url)
