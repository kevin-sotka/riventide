#!/usr/bin/env python3
"""
Riventide - An immersive text-based role-playing adventure game
"""

import os
import sys
import time
import random
import argparse
from colorama import init, Fore, Back, Style
import pyfiglet

# Initialize colorama
init(autoreset=True)

# Import game modules
from game.engine import GameEngine

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_title():
    """Display the game title."""
    clear_screen()
    title = pyfiglet.figlet_format("RIVENTIDE", font="big")
    print(Fore.CYAN + title)
    print(Fore.YELLOW + "An Epic Fantasy Adventure" + Style.RESET_ALL)
    print("\n" + Fore.WHITE + "Written and designed by: Kevin Sotka, 2025" + Style.RESET_ALL)
    print("\n" + "-" * 80 + "\n")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Riventide - An Epic Fantasy Adventure")
    parser.add_argument("--text-only", action="store_true", help="Run in text-only mode (no graphics or sound)")
    parser.add_argument("--width", type=int, default=800, help="Window width (default: 800)")
    parser.add_argument("--height", type=int, default=600, help="Window height (default: 600)")
    parser.add_argument("--no-music", action="store_true", help="Disable music")
    parser.add_argument("--no-sound", action="store_true", help="Disable sound effects")
    return parser.parse_args()

def main():
    """Main game function."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Display title in text mode
    if args.text_only:
        display_title()
        print(Fore.GREEN + "Welcome to the world of Riventide!" + Style.RESET_ALL)
        print("A land of magic, mystery, and adventure awaits you.\n")
        input(Fore.CYAN + "Press Enter to continue..." + Style.RESET_ALL)
    
    # Initialize game engine
    engine = GameEngine(
        width=args.width,
        height=args.height,
        text_only=args.text_only
    )
    
    # Apply audio settings
    if args.no_music and engine.audio:
        engine.audio.music_enabled = False
    if args.no_sound and engine.audio:
        engine.audio.sound_enabled = False
    
    # Start the game
    try:
        engine.start()
    except KeyboardInterrupt:
        print("\n\nGame terminated by user. Farewell, adventurer!")
    except Exception as e:
        print(f"\n\nAn error occurred: {e}")
    finally:
        engine.cleanup()

if __name__ == "__main__":
    main() 