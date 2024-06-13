#!/bin/bash

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Inform the user
echo "Setup complete. To activate the virtual environment, run 'source venv/bin/activate'."
