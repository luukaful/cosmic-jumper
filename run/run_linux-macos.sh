#!/bin/bash
# This script is used to run the Linux/macOS version of the game.

# Navigate to the parent directory
cd ..

# Activate the virtual environment
source .venv/bin/activate

# Run the game
python3 main.py

# Deactivate the virtual environment
deactivate