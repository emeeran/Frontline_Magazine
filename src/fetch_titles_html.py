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


# Function to generate Markdown file with extracted data
def generate_markdown(data):
    issue_date = data[0]['issue_date'] if data else 'Unknown'
    markdown_content = f"""# Frontline Issue - {issue_date}

"""

    for article in data:
        markdown_content += f"""## {article['title']}

*{article['sub_text']}*

**Author:** {article['author']}

**Link:** [{article['title']}]({article['link']})

---

"""

    return markdown_content


# Main function
def main():
    url = "https://frontline.thehindu.com/current-issue/"
    data = scrape_data(url)
    markdown_content = generate_markdown(data)

    with open(
        f'./articles/Frontline_{data[0]["issue_date"]}.md', "w", encoding="utf-8"
    ) as f:
        f.write(markdown_content)

        print("Markdown file created successfully.")


if __name__ == "__main__":
    main()
# works fine!
