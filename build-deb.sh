#!/bin/bash

# Build script for Frontline Magazine .deb package

set -e

PACKAGE_NAME="frontline-magazine"
VERSION="1.0.0"
ARCH="all"
BUILD_DIR="$(pwd)"

echo "Building ${PACKAGE_NAME} v${VERSION} for ${ARCH}..."

# Check if we're in the right directory
if [ ! -d "debian" ]; then
    echo "Error: debian directory not found. Please run this script from the project root."
    exit 1
fi

# Check dependencies
echo "Checking build dependencies..."
if ! command -v dpkg-deb &> /dev/null; then
    echo "Error: dpkg-deb not found. Please install dpkg-dev:"
    echo "sudo apt install dpkg-dev"
    exit 1
fi

# Create output directory
mkdir -p dist

# Set proper permissions
echo "Setting file permissions..."
find debian/usr -type f -exec chmod 644 {} \;
find debian/usr/bin -type f -exec chmod 755 {} \;
chmod 755 debian/DEBIAN/postinst debian/DEBIAN/prerm

# Build the package
echo "Building .deb package..."
dpkg-deb --build debian "dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

# Check package
echo "Checking package integrity..."
dpkg-deb --info "dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
dpkg-deb --contents "dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"

echo ""
echo "Package built successfully!"
echo "Location: dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo ""
echo "To install:"
echo "sudo dpkg -i dist/${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
echo "sudo apt-get install -f  # Fix any missing dependencies"
echo ""
echo "To remove:"
echo "sudo apt remove ${PACKAGE_NAME}"
