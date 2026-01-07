#!/bin/bash

# Nitro Swim Scraper - Local Setup Script
# For macOS/local development

set -e

echo "=========================================="
echo "Nitro Swim Scraper - Local Setup"
echo "=========================================="

# Check if Python3 is installed
echo "Checking Python3..."
if ! command -v python3 &> /dev/null; then
    echo "Python3 not found. Please install Python3 first."
    exit 1
fi

echo "Python3 found: $(python3 --version)"

# Install Python dependencies
echo ""
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create log directory
echo "Creating log directory..."
mkdir -p logs

# Install Playwright browsers
echo ""
echo "Installing Playwright browsers..."
python3 -m playwright install chromium

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "To run the scraper once:"
echo "  python3 scraper.py"
echo ""
echo "To run the scheduler (continuous):"
echo "  python3 scheduler.py"
echo ""
echo "To view logs:"
echo "  tail -f logs/nitro_swim_scraper.log"
echo ""
