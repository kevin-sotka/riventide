#!/usr/bin/env python3
"""
Riventide Launcher
Double-click this file to start the game
"""

import os
import sys
import subprocess

def main():
    """Launch Riventide."""
    print("Starting Riventide...")
    
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the script directory
    os.chdir(script_dir)
    
    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    
    # Determine the Python executable to use
    if in_venv:
        # Use the virtual environment's Python
        python_exe = sys.executable
    else:
        # Use the system Python
        python_exe = "python3" if os.name != "nt" else "python"
    
    # Launch the game
    try:
        subprocess.run([python_exe, "main.py"])
    except Exception as e:
        print(f"Error launching Riventide: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 