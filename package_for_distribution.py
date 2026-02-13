#!/usr/bin/env python3
"""
Package Riventide for distribution on different platforms
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def check_dependencies():
    """Check if required tools are installed."""
    print("Checking dependencies...")
    
    # Check PyInstaller
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check if assets exist
    if not os.path.exists("assets"):
        print("✗ Assets directory not found!")
        return False
    
    print("✓ All dependencies ready")
    return True

def create_executable():
    """Create a standalone executable using PyInstaller."""
    print("Creating executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=Riventide",
        "--add-data=assets;assets",
        "--icon=assets/graphics/icons/quest.png",
        "main.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✓ Executable created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create executable: {e}")
        return False

def create_installer_windows():
    """Create Windows installer using NSIS."""
    print("Creating Windows installer...")
    
    # Check if NSIS is available
    nsis_path = shutil.which("makensis")
    if not nsis_path:
        print("✗ NSIS not found. Install NSIS to create Windows installer.")
        return False
    
    # Create NSIS script
    nsis_script = """
!include "MUI2.nsh"

Name "Riventide"
OutFile "Riventide-Setup.exe"
InstallDir "$PROGRAMFILES\\Riventide"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File "dist\\Riventide.exe"
    File /r "assets"
    
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
    
    CreateDirectory "$SMPROGRAMS\\Riventide"
    CreateShortCut "$SMPROGRAMS\\Riventide\\Riventide.lnk" "$INSTDIR\\Riventide.exe"
    CreateShortCut "$DESKTOP\\Riventide.lnk" "$INSTDIR\\Riventide.exe"
    
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riventide" \\
                     "DisplayName" "Riventide"
    WriteRegStr HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riventide" \\
                     "UninstallString" "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\Riventide.exe"
    RMDir /r "$INSTDIR\\assets"
    Delete "$INSTDIR\\Uninstall.exe"
    RMDir "$INSTDIR"
    
    Delete "$SMPROGRAMS\\Riventide\\Riventide.lnk"
    RMDir "$SMPROGRAMS\\Riventide"
    Delete "$DESKTOP\\Riventide.lnk"
    
    DeleteRegKey HKLM "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Riventide"
SectionEnd
"""
    
    with open("installer.nsi", "w") as f:
        f.write(nsis_script)
    
    try:
        subprocess.run(["makensis", "installer.nsi"], check=True)
        print("✓ Windows installer created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create installer: {e}")
        return False

def create_dmg_macos():
    """Create macOS DMG file."""
    print("Creating macOS DMG...")
    
    # Check if create-dmg is available
    create_dmg_path = shutil.which("create-dmg")
    if not create_dmg_path:
        print("✗ create-dmg not found. Install with: brew install create-dmg")
        return False
    
    try:
        # Create DMG
        subprocess.run([
            "create-dmg",
            "--volname", "Riventide",
            "--window-pos", "200", "120",
            "--window-size", "600", "400",
            "--icon-size", "100",
            "--icon", "Riventide.app", "175", "120",
            "--hide-extension", "Riventide.app",
            "--app-drop-link", "425", "120",
            "Riventide.dmg",
            "dist/"
        ], check=True)
        print("✓ macOS DMG created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create DMG: {e}")
        return False

def create_linux_package():
    """Create Linux package."""
    print("Creating Linux package...")
    
    # Create AppImage
    try:
        # Create AppDir structure
        appdir = "Riventide.AppDir"
        os.makedirs(f"{appdir}/usr/bin", exist_ok=True)
        os.makedirs(f"{appdir}/usr/share/applications", exist_ok=True)
        os.makedirs(f"{appdir}/usr/share/icons/hicolor/256x256/apps", exist_ok=True)
        
        # Copy executable
        shutil.copy("dist/Riventide", f"{appdir}/usr/bin/")
        
        # Create desktop file
        desktop_content = """[Desktop Entry]
Name=Riventide
Comment=An immersive text-based role-playing adventure game
Exec=riventide
Icon=riventide
Terminal=false
Type=Application
Categories=Game;AdventureGame;RolePlaying;
"""
        with open(f"{appdir}/usr/share/applications/riventide.desktop", "w") as f:
            f.write(desktop_content)
        
        # Copy icon
        shutil.copy("assets/graphics/icons/quest.png", 
                   f"{appdir}/usr/share/icons/hicolor/256x256/apps/riventide.png")
        
        # Create AppRun
        apprun_content = """#!/bin/bash
cd "$(dirname "$0")"
exec ./usr/bin/Riventide "$@"
"""
        with open(f"{appdir}/AppRun", "w") as f:
            f.write(apprun_content)
        os.chmod(f"{appdir}/AppRun", 0o755)
        
        # Create AppImage
        subprocess.run([
            "appimagetool", appdir, "Riventide-x86_64.AppImage"
        ], check=True)
        
        print("✓ Linux AppImage created")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to create AppImage: {e}")
        return False

def create_itch_io_package():
    """Create package for Itch.io."""
    print("Creating Itch.io package...")
    
    itch_dir = "itch-package"
    if os.path.exists(itch_dir):
        shutil.rmtree(itch_dir)
    os.makedirs(itch_dir)
    
    # Copy executable
    if platform.system() == "Windows":
        shutil.copy("dist/Riventide.exe", f"{itch_dir}/Riventide.exe")
    elif platform.system() == "Darwin":
        shutil.copy("dist/Riventide", f"{itch_dir}/Riventide")
    else:
        shutil.copy("dist/Riventide", f"{itch_dir}/Riventide")
    
    # Copy assets
    shutil.copytree("assets", f"{itch_dir}/assets")
    
    # Create README
    readme_content = """# Riventide

An immersive text-based role-playing adventure game.

## Installation
1. Extract all files to a folder
2. Run the executable (Riventide.exe on Windows, Riventide on Mac/Linux)
3. Enjoy your adventure!

## Controls
- Arrow keys to navigate
- Enter/Space to select
- Escape to go back
- I for inventory, M for map, C for character, Q for quests

## System Requirements
- Windows 7+, macOS 10.12+, or Linux
- 2 GB RAM
- 500 MB storage space
"""
    with open(f"{itch_dir}/README.txt", "w") as f:
        f.write(readme_content)
    
    print("✓ Itch.io package created")
    return True

def main():
    """Main packaging function."""
    print("Riventide Packaging Tool")
    print("=" * 40)
    
    if not check_dependencies():
        return
    
    # Create executable first
    if not create_executable():
        return
    
    # Create platform-specific packages
    system = platform.system()
    
    if system == "Windows":
        create_installer_windows()
    elif system == "Darwin":
        create_dmg_macos()
    elif system == "Linux":
        create_linux_package()
    
    # Create Itch.io package
    create_itch_io_package()
    
    print("\nPackaging complete!")
    print("Files created:")
    print("- dist/Riventide (executable)")
    if system == "Windows":
        print("- Riventide-Setup.exe (installer)")
    elif system == "Darwin":
        print("- Riventide.dmg (macOS package)")
    elif system == "Linux":
        print("- Riventide-x86_64.AppImage (Linux package)")
    print("- itch-package/ (Itch.io ready)")

if __name__ == "__main__":
    main() 