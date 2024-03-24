from playwright.sync_api import sync_playwright


# def extract_article_content(url):
# 	with sync_playwright() as p:
# 		browser = p.chromium.launch()
# 		page = browser.new_page()
# 		page.goto(url)
# 		title = page.query_selector('h1.title').inner_text()
# 		publish_time = page.query_selector('.publish-time').inner_text()
# 		article_content = page.query_selector('#content-body-67945963').inner_text()
# 		browser.close()
#
# 	return {
# 		"title": title,
# 		"publish_time": publish_time,
# 		"article_content": article_content
# 	}
def extract_article_content(url):
	with sync_playwright() as p:
		browser = p.chromium.launch()
		page = browser.new_page()
		page.goto(url)
		article_content_selector = '#content-body-67945963'
		page.wait_for_selector(article_content_selector)
		title = page.query_selector('h1.title').inner_text()
		publish_time = page.query_selector('.publish-time').inner_text()
		article_content = page.query_selector(article_content_selector).inner_text()
		browser.close()

	return {
		"title": title,
		"publish_time": publish_time,
		"article_content": article_content
	}


def export_to_html(title, publish_time, article_content):
	html_content = f"""
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 20px;
            }}
            h1 {{
                font-size: 24px;
            }}
            p.publish-time {{
                font-size: 14px;
                color: gray;
            }}
            .content {{
                margin-top: 20px;
                font-size: 16px;
                line-height: 1.6;
            }}
        </style>
    </head>
    <body>
        <h1>{title}</h1>
        <p class="publish-time">{publish_time}</p>
        <div class="content">{article_content}</div>
    </body>
    </html>
    """

	with open(f'{title}.html', 'w', encoding='utf-8') as file:
		file.write(html_content)
	print(f"Data exported to {title}.html file.")


url = input("Enter the URL of the article: ")
article_data = extract_article_content(url)
export_to_html(article_data['title'], article_data['publish_time'], article_data['article_content'])
