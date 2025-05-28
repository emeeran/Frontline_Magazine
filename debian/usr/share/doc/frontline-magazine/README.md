# Frontline Magazine Scraper

A Python-based web scraping application for extracting articles and generating HTML/PDF files from Frontline Magazine's current issues.

## Features

- **Article Extraction**: Scrape individual articles and save them as HTML files
- **Issue Overview**: Generate comprehensive HTML files with all articles from the current issue
- **PDF Generation**: Convert articles to PDF format for offline reading
- **Clean Output**: Filtered content without ads, comments, or unnecessary elements

## Project Structure

```
Frontline_Magazine/
├── src/
│   ├── fetch_article_html.py    # Extract individual articles as HTML
│   ├── fetch_article_pdf.py     # Extract individual articles as PDF
│   ├── fetch_titles_html.py     # Generate issue overview HTML
│   └── styles.css              # CSS styling for HTML output
├── articles/                   # Generated HTML and PDF files
├── requirements.txt           # Python dependencies
└── README.md                 # Project documentation
```

## Prerequisites

### System Dependencies
- Python 3.8+
- wkhtmltopdf (for PDF generation)

### Installing System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y wkhtmltopdf
```

**macOS:**
```bash
brew install wkhtmltopdf
```

**Windows:**
Download and install from: https://wkhtmltopdf.org/downloads.html

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Frontline_Magazine
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Usage

### Generate Issue Overview HTML
Creates an HTML file with all articles from the current issue:

```bash
cd src
python fetch_titles_html.py
```

Output: `articles/Frontline_<date>.html`

### Extract Individual Article as HTML
Extracts a specific article and saves it as HTML:

```bash
cd src
python fetch_article_html.py
# Enter the article URL when prompted
```

Output: `articles/<article-title>.html`

### Extract Individual Article as PDF
Extracts a specific article and saves it as PDF:

```bash
cd src
python fetch_article_pdf.py
# Enter the article URL when prompted
```

Output: `articles/<article-title>.pdf`

## Key Dependencies

- **playwright**: Web automation and scraping
- **beautifulsoup4**: HTML parsing
- **pdfkit**: PDF generation from HTML
- **requests**: HTTP requests

## Configuration

The application works out-of-the-box with Frontline Magazine's current website structure. No additional configuration is required.

## Platform Compatibility

- ✅ Linux (Ubuntu, Debian, etc.)
- ✅ macOS
- ✅ Windows (with appropriate system dependencies)

## Troubleshooting

### Common Issues

1. **wkhtmltopdf not found**:
   - Ensure wkhtmltopdf is installed and in your system PATH
   - On Linux, install with: `sudo apt install -y wkhtmltopdf`

2. **Playwright browser not found**:
   - Run: `playwright install`

3. **Permission errors**:
   - Ensure the `articles/` directory is writable
   - Check file permissions in the project directory

### Error Handling

The application includes error handling for:
- Network timeouts
- Missing elements on web pages
- File system permissions
- Invalid URLs

## Output Files

### HTML Files
- Clean, styled HTML with embedded CSS
- Proper encoding (UTF-8) for international characters
- Responsive design for different screen sizes

### PDF Files
- A4 page format with appropriate margins
- Styled text with proper formatting
- Embedded fonts for consistent rendering

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for educational and personal use. Please respect Frontline Magazine's terms of service and copyright policies.

## Disclaimer

This tool is designed for personal use and educational purposes. Users are responsible for complying with the website's terms of service and applicable copyright laws.

## Version History

- **v1.0**: Initial release with basic scraping functionality
- **v1.1**: Added PDF generation support
- **v1.2**: Fixed cross-platform compatibility issues
- **v1.3**: Improved error handling and date display formatting
