#!/bin/bash

CONFIG_FILE="config.json"

# Step 1: check for requirments
echo "Checking python version"
if ! command -v python3 &>/dev/null; then
    echo "Python not installed. Aborting..."
    exit 1
fi

echo "Installing dependenices"
pip install -r requirements.txt

# Step 2: check if config.json is valid

# Step 3: create hashes from config

# Step 4: using hashes launch the app.py and keep it running

# Step 5: shred all these files