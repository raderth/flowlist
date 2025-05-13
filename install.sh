#!/bin/bash

# Flowlist installer

set -e

echo "Installing Flowlist (standalone version)..."

# Install Python and pip if missing (Debian-based systems only)
if ! command -v python3 &> /dev/null; then
  echo "Installing Python..."
  sudo apt-get update
  sudo apt-get install -y python3 python3-pip python3-venv
fi

# Clone the repo
git clone https://github.com/raderth/flowlist.git
cd flowlist

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
if [ -f requirements.txt ]; then
  pip install -r requirements.txt
else
  pip install flask discord.py
fi

# Run the server
echo "Starting Flowlist..."
python web/main.py
