#!/bin/bash

# Test script for Frontline Magazine .deb package

set -e

echo "Testing Frontline Magazine Package Installation..."
echo "================================================="

# Check if package is installed
if dpkg -l frontline-magazine >/dev/null 2>&1; then
    echo "✓ Package is installed"
else
    echo "✗ Package is not installed"
    echo "Please install with: sudo dpkg -i dist/frontline-magazine_1.0.0_all.deb"
    exit 1
fi

# Check if executable is available
if command -v frontline-magazine >/dev/null 2>&1; then
    echo "✓ Command line tool is available"
else
    echo "✗ Command line tool not found in PATH"
    exit 1
fi

# Test help command
echo ""
echo "Testing help command:"
echo "---------------------"
frontline-magazine --help

# Check if virtual environment exists
if [ -d "/usr/share/frontline-magazine/venv" ]; then
    echo "✓ Virtual environment exists"
else
    echo "✗ Virtual environment not found"
    exit 1
fi

# Check if Python dependencies are installed
echo ""
echo "Checking Python dependencies:"
echo "-----------------------------"
VENV_PYTHON="/usr/share/frontline-magazine/venv/bin/python"
if [ -f "$VENV_PYTHON" ]; then
    echo "✓ Python virtual environment is properly set up"
    
    # Check key dependencies
    if $VENV_PYTHON -c "import playwright" 2>/dev/null; then
        echo "✓ Playwright is installed"
    else
        echo "✗ Playwright not found"
    fi
    
    if $VENV_PYTHON -c "import bs4" 2>/dev/null; then
        echo "✓ BeautifulSoup4 is installed"
    else
        echo "✗ BeautifulSoup4 not found"
    fi
    
    if $VENV_PYTHON -c "import pdfkit" 2>/dev/null; then
        echo "✓ PDFKit is installed"
    else
        echo "✗ PDFKit not found"
    fi
else
    echo "✗ Python executable not found in virtual environment"
    exit 1
fi

# Check if desktop entry exists
if [ -f "/usr/share/applications/frontline-magazine.desktop" ]; then
    echo "✓ Desktop entry is installed"
else
    echo "✗ Desktop entry not found"
fi

# Check if wkhtmltopdf is available
if command -v wkhtmltopdf >/dev/null 2>&1; then
    echo "✓ wkhtmltopdf is available"
else
    echo "✗ wkhtmltopdf not found - PDF generation may not work"
fi

# Check if tkinter is available for GUI
echo ""
echo "Testing GUI dependencies:"
echo "------------------------"
if $VENV_PYTHON -c "import tkinter" 2>/dev/null; then
    echo "✓ tkinter is available for GUI"
else
    echo "✗ tkinter not found - GUI may not work"
    echo "  Install with: sudo apt install python3-tk"
fi

# Test CLI commands
echo ""
echo "Testing CLI commands:"
echo "--------------------"
echo "Testing help command:"
frontline-magazine --help | head -5

echo ""
echo "Installation test completed!"
echo ""
echo "To use the application:"
echo "  Command line: frontline-magazine [titles|article-html|article-pdf]"
echo "  GUI: frontline-magazine gui"
echo "  Desktop: Look for 'Frontline Magazine Scraper' in your applications menu"
echo ""
echo "Output files will be saved to: ~/FrontlineMagazine/"
