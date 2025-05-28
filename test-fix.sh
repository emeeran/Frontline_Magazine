#!/bin/bash

# Quick test of the fixed package structure
echo "Testing fixed package structure..."

# Test the main executable script
echo ""
echo "Testing main executable paths:"
echo "=============================="

INSTALL_DIR="/home/em/code/wip/Frontline_Magazine/debian/usr/share/frontline-magazine"
VENV_DIR="$INSTALL_DIR/venv"

echo "Install directory: $INSTALL_DIR"
echo "Files in install directory:"
ls -la "$INSTALL_DIR"

echo ""
echo "Testing script paths:"
for script in "fetch_titles_html.py" "fetch_article_html.py" "fetch_article_pdf.py" "frontline_gui.py"; do
    if [ -f "$INSTALL_DIR/$script" ]; then
        echo "✓ $script found"
    else
        echo "✗ $script missing"
    fi
done

echo ""
echo "Testing main executable:"
cat "/home/em/code/wip/Frontline_Magazine/debian/usr/bin/frontline-magazine" | grep -A 10 "case.*in"
