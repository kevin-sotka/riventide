#!/bin/bash
# Riventide Launcher Script

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if we're in a virtual environment
if [ -d ".venv" ]; then
    # Activate the virtual environment
    source .venv/bin/activate
    # Run the game
    python3 main.py
else
    # Run with system Python
    python3 main.py
fi 