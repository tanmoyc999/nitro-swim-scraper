#!/bin/bash

# Nitro Swim Scraper - EC2 Setup Script
# This script automates the setup on EC2 instance

set -e

echo "=========================================="
echo "Nitro Swim Scraper - EC2 Setup"
echo "=========================================="

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and pip
echo "Installing Python3 and pip..."
sudo apt-get install -y python3 python3-pip

# Install system dependencies for Playwright
echo "Installing system dependencies for Playwright..."
sudo apt-get install -y \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2t64

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Install Playwright browsers
echo "Installing Playwright browsers..."
python3 -m playwright install

# Create log directory
echo "Creating log directory..."
sudo mkdir -p /var/log/nitro_swim
sudo chown $USER:$USER /var/log/nitro_swim

# Copy systemd service file
echo "Setting up systemd service..."
sudo cp nitro-swim.service /etc/systemd/system/
sudo systemctl daemon-reload

# Enable service
echo "Enabling service..."
sudo systemctl enable nitro-swim.service

# Start service
echo "Starting service..."
sudo systemctl start nitro-swim.service

# Check status
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Service Status:"
sudo systemctl status nitro-swim.service

echo ""
echo "To view logs:"
echo "  tail -f /var/log/nitro_swim_scraper.log"
echo ""
echo "To check service status:"
echo "  sudo systemctl status nitro-swim.service"
echo ""
echo "To stop the service:"
echo "  sudo systemctl stop nitro-swim.service"
echo ""
