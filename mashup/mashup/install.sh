#!/bin/bash

# Installation script for YouTube Mashup Creator
# This script installs all required dependencies

echo "============================================================"
echo "     YouTube Mashup Creator - Installation Script"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if FFmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg is not installed."
    echo ""
    echo "Please install FFmpeg:"
    echo "  - Ubuntu/Debian: sudo apt install ffmpeg"
    echo "  - macOS: brew install ffmpeg"
    echo "  - Windows: Download from https://ffmpeg.org/download.html"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✓ FFmpeg found: $(ffmpeg -version | head -n 1)"
fi

echo ""
echo "Installing Python dependencies..."
echo ""

# Install Python packages
pip3 install yt-dlp pydub flask flask-mail --break-system-packages

if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "✓ Installation completed successfully!"
    echo "============================================================"
    echo ""
    echo "Next steps:"
    echo ""
    echo "1. For Command Line Program:"
    echo "   python3 101556.py \"Singer Name\" 15 25 output.mp3"
    echo ""
    echo "2. For Web Service:"
    echo "   - Update email settings in app.py"
    echo "   - Run: python3 app.py"
    echo "   - Visit: http://localhost:5000"
    echo ""
    echo "See README.md for detailed instructions."
    echo "============================================================"
else
    echo ""
    echo "❌ Installation failed. Please check the errors above."
    exit 1
fi
