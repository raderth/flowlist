#!/bin/bash

# Flowlist installation and systemd service generator script

INSTALL_DIR=$(pwd)
REPO_URL="https://github.com/raderth/flowlist.git"
REPO_NAME="flowlist"
PORT=8080 # You can change this if necessary

# Check if flowlist directory exists
if [ ! -d "$REPO_NAME" ]; then
    echo "'flowlist' directory not found. Cloning Flowlist..."
    git clone $REPO_URL
fi

cd $REPO_NAME

# Set up the virtual environment if not already set up
if [ ! -d "venv" ]; then
    echo "Setting up virtual environment..."
    python3 -m venv venv
fi

# Install dependencies if not already installed
VENV_PY="$INSTALL_DIR/$REPO_NAME/venv/bin/python"
if ! $VENV_PY -m pip show -q -f flask discord.py; then
    echo "Installing dependencies..."
    $VENV_PY -m pip install -r requirements.txt || $VENV_PY -m pip install flask discord.py
fi

# Get the absolute path to the main.py file
MAIN_PY="$INSTALL_DIR/$REPO_NAME/web/main.py"
if [ ! -f "$MAIN_PY" ]; then
    echo "'main.py' not found in 'flowlist/web'."
    exit 1
fi

# Define the service file location
SERVICE_FILE="$HOME/.config/systemd/user/flowlist.service"

# Create the directory for user systemd service if it doesn't exist
mkdir -p "$HOME/.config/systemd/user"

# Write the systemd service file
cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Flowlist Server
After=network.target

[Service]
ExecStart=$VENV_PY $MAIN_PY
WorkingDirectory=$INSTALL_DIR/$REPO_NAME
Restart=always
Environment=VIRTUAL_ENV=$INSTALL_DIR/$REPO_NAME/venv
Environment=PATH=$INSTALL_DIR/$REPO_NAME/venv/bin:$PATH
Environment=PORT=$PORT

[Install]
WantedBy=default.target
EOF

# Enable and start the service
systemctl --user enable flowlist
systemctl --user start flowlist

echo "Flowlist installed and systemd service created and started successfully."
