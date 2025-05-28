# Installation Guide for Frontline Magazine .deb Package

## Quick Installation

### Method 1: Using the .deb Package (Recommended)

1. **Download the package:**
   ```bash
   # The package is located at: dist/frontline-magazine_1.0.0_all.deb
   ```

2. **Install the package:**
   ```bash
   sudo dpkg -i dist/frontline-magazine_1.0.0_all.deb
   sudo apt-get install -f  # This will install any missing dependencies
   ```

3. **Verify installation:**
   ```bash
   frontline-magazine --help
   ```

### Method 2: Building from Source

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Frontline_Magazine
   ```

2. **Build the package:**
   ```bash
   ./build-deb.sh
   ```

3. **Install the built package:**
   ```bash
   sudo dpkg -i dist/frontline-magazine_1.0.0_all.deb
   sudo apt-get install -f
   ```

## Usage

After installation, you can use the application in several ways:

### Command Line Interface

```bash
# Extract magazine issue titles and generate HTML summary
frontline-magazine titles

# Extract individual article as HTML
frontline-magazine article-html

# Extract individual article as PDF
frontline-magazine article-pdf

# Show help
frontline-magazine --help
```

### Desktop Application

Look for "Frontline Magazine Scraper" in your applications menu under "Utilities" or search for it in your application launcher.

## Output Location

All generated files will be saved to: `~/FrontlineMagazine/articles/`

## System Requirements

- Ubuntu 18.04 LTS or later
- Python 3.8 or later
- Internet connection for downloading articles
- At least 500MB free disk space (including dependencies)

## Dependencies

The following packages will be automatically installed:

- `python3` (>= 3.8)
- `python3-pip`
- `python3-venv`
- `wkhtmltopdf`

Python packages installed in virtual environment:
- `playwright`
- `beautifulsoup4`
- `pdfkit`
- `requests`

## Uninstallation

To remove the application:

```bash
sudo apt remove frontline-magazine
```

This will remove the application and its virtual environment but keep your generated files in `~/FrontlineMagazine/`.

## Troubleshooting

### Common Issues

1. **Permission denied errors:**
   ```bash
   sudo apt-get install -f
   ```

2. **Missing dependencies:**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv wkhtmltopdf
   ```

3. **Playwright browser installation issues:**
   ```bash
   # The postinst script automatically installs Chromium
   # If manual installation is needed:
   /usr/share/frontline-magazine/venv/bin/playwright install chromium
   ```

### Getting Help

- Check the application help: `frontline-magazine --help`
- Review the log files in `~/FrontlineMagazine/`
- Report issues on the project repository

## Development

For developers who want to modify the code:

1. **Extract the installed files:**
   ```bash
   cp -r /usr/share/frontline-magazine/ ~/frontline-dev/
   ```

2. **Create development environment:**
   ```bash
   cd ~/frontline-dev/
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Rebuild package after changes:**
   ```bash
   ./build-deb.sh
   ```
