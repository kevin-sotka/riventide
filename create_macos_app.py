#!/usr/bin/env python3
"""
Create a macOS application bundle for Riventide
"""

import os
import sys
import shutil
import subprocess

def create_app_bundle():
    """Create a macOS application bundle for Riventide."""
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Define the app bundle structure
    app_name = "Riventide.app"
    app_path = os.path.join(current_dir, app_name)
    contents_path = os.path.join(app_path, "Contents")
    macos_path = os.path.join(contents_path, "MacOS")
    resources_path = os.path.join(contents_path, "Resources")
    
    # Create the directory structure
    os.makedirs(macos_path, exist_ok=True)
    os.makedirs(resources_path, exist_ok=True)
    
    # Create the Info.plist file
    info_plist = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Riventide</string>
    <key>CFBundleIdentifier</key>
    <string>com.example.riventide</string>
    <key>CFBundleName</key>
    <string>Riventide</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
"""
    
    with open(os.path.join(contents_path, "Info.plist"), "w") as f:
        f.write(info_plist)
    
    # Create the launcher script
    launcher_script = """#!/bin/bash
# Riventide Launcher

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Change to the Resources directory
cd "$SCRIPT_DIR/../Resources"

# Run the game
./venv/bin/python main.py
"""
    
    with open(os.path.join(macos_path, "Riventide"), "w") as f:
        f.write(launcher_script)
    
    # Make the launcher script executable
    os.chmod(os.path.join(macos_path, "Riventide"), 0o755)
    
    # Copy the game files to the Resources directory
    for item in os.listdir(current_dir):
        if item != app_name and not item.startswith("."):
            src = os.path.join(current_dir, item)
            dst = os.path.join(resources_path, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst)
            else:
                shutil.copy2(src, dst)
    
    # Create a virtual environment in the Resources directory
    subprocess.run([sys.executable, "-m", "venv", os.path.join(resources_path, "venv")])
    
    # Install the required packages
    subprocess.run([
        os.path.join(resources_path, "venv/bin/pip"),
        "install", "-r", os.path.join(resources_path, "requirements.txt")
    ])
    
    print(f"Created macOS application bundle: {app_name}")
    print(f"You can now run the game by double-clicking on {app_name}")

if __name__ == "__main__":
    create_app_bundle() 