import pdfkit
from playwright.sync_api import sync_playwright

def extract_article_content(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        page.wait_for_load_state('networkidle')

        # Exclude unwanted elements
        unwanted_selectors = ['Also Read', 'COMMents', 'Follow Us', 'SHARE']
        for selector in unwanted_selectors:
            element = page.query_selector(selector)
            if element:
                element.remove()

        # Extract all paragraph elements
        paragraph_elements = page.query_selector_all('p')

        # Concatenate text from all paragraph elements
        article_content = '\n'.join([p.inner_text() for p in paragraph_elements])

        # Output to PDF
        filename = url.split('/')[-2] + '.pdf'
        # Replace 'path_to_wkhtmltopdf' with the actual path to wkhtmltopdf executable
        pdfkit.from_string(article_content, filename, configuration=pdfkit.configuration(wkhtmltopdf='C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'))

        browser.close()

if __name__ == "__main__":
    url = input("Enter the URL: ")
    extract_article_content(url)
