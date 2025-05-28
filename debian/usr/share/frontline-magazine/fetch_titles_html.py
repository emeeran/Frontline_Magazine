from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


# Function to scrape data from the webpage
def scrape_data(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)

        # Extract magazine issue date
        issue_date_element = page.query_selector("span.date")
        issue_date = (
            issue_date_element.inner_text() if issue_date_element else "Unknown"
        )

        articles = page.query_selector_all(
            "div.section-magazine.current-issue-in-this-issue div.content"
        )

        data = []
        for article in articles:
            title = article.query_selector("h3.title").inner_text()
            sub_text = article.query_selector("div.sub-text").inner_text()
            author = article.query_selector("div.author").inner_text()
            link = article.query_selector("a").get_attribute("href")
            data.append(
                {
                    "title": title,
                    "sub_text": sub_text,
                    "author": author,
                    "link": link,
                    "issue_date": issue_date,
                }
            )

        browser.close()
        return data


# Function to generate HTML file with extracted data
def generate_html(data):
    issue_date = data[0]['issue_date'] if data else 'Unknown'
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Frontline Issue</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
            }}
            .article {{
                margin-bottom: 20px;
                padding: 10px;
                border: 1px solid #ccc;
            }}
            .title {{
                font-size: 18px;
                font-weight: bold;
            }}
            .sub-text {{
                font-style: italic;
            }}
            .author {{
                font-size: 14px;
            }}
            .link {{
                color: blue;
            }}
        </style>
    </head>
    <body>
        <h1>Frontline Issue - {issue_date}</h1>
    """

    for article in data:
        html_content += f"""
        <div class="article">
            <div class="title">{article['title']}</div>
            <div class="sub-text">{article['sub_text']}</div>
            <div class="author">Author: {article['author']}</div>
            <div class="link"><a href="{article['link']}" target="_blank">Read More</a></div>
        </div>
        """

    html_content += """
    </body>
    </html>
    """

    return html_content


# Main function
def main():
    url = "https://frontline.thehindu.com/current-issue/"
    data = scrape_data(url)
    html_content = generate_html(data)

    import os
    # Create articles directory in current working directory (user's home/FrontlineMagazine)
    os.makedirs("articles", exist_ok=True)
    
    with open(
        f'./articles/Frontline_{data[0]["issue_date"]}.html', "w", encoding="utf-8"
    ) as f:
        f.write(html_content)

        print("HTML file created successfully.")


if __name__ == "__main__":
    main()
# works fine!
