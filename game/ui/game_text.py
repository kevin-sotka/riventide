"""
Game text display utilities for Riventide
"""

import time
import os
from colorama import Fore, Back, Style

class GameText:
    """Handles the display of game text and narration."""
    
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    @staticmethod
    def print_slow(text, delay=0.03, color=None):
        """Print text slowly, character by character."""
        if color:
            text = color + text + Style.RESET_ALL
            
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
        
    @staticmethod
    def print_header(text, width=60):
        """Print a header with decorative borders."""
        print(Fore.CYAN + "=" * width)
        print(Fore.YELLOW + text.center(width) + Style.RESET_ALL)
        print(Fore.CYAN + "=" * width + Style.RESET_ALL)
        
    @staticmethod
    def print_box(text, width=60, color=Fore.WHITE):
        """Print text in a decorative box."""
        print(Fore.CYAN + "+" + "-" * (width - 2) + "+")
        
        # Split text into lines that fit within the box
        words = text.split()
        lines = []
        current_line = ""
        
        for word in words:
            if len(current_line) + len(word) + 1 <= width - 4:  # -4 for margins
                current_line += " " + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
                
        if current_line:
            lines.append(current_line)
            
        # Print each line centered in the box
        for line in lines:
            padding = (width - 4 - len(line)) // 2
            print(Fore.CYAN + "| " + " " * padding + color + line + 
                  " " * (width - 4 - len(line) - padding) + Fore.CYAN + " |")
                  
        print(Fore.CYAN + "+" + "-" * (width - 2) + "+" + Style.RESET_ALL)
        
    @staticmethod
    def print_options(options, prompt="What will you do?"):
        """Print a list of options for the player to choose from."""
        print("\n" + Fore.CYAN + prompt + Style.RESET_ALL + "\n")
        
        for i, option in enumerate(options, 1):
            print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {option}")
            
    @staticmethod
    def narrate(text, delay=0.03):
        """Display narrative text with a typewriter effect."""
        GameText.print_slow(text, delay, Fore.WHITE)
        
    @staticmethod
    def describe_location(name, description):
        """Display a location description."""
        GameText.print_header(name)
        GameText.print_slow(description, 0.02, Fore.WHITE)
        print()
        
    @staticmethod
    def describe_character(name, description):
        """Display a character description."""
        print(f"\n{Fore.YELLOW}{name}{Style.RESET_ALL}")
        GameText.print_slow(description, 0.02, Fore.WHITE)
        
    @staticmethod
    def display_dialog(speaker, text):
        """Display character dialog."""
        print(f"\n{Fore.YELLOW}{speaker}:{Style.RESET_ALL}", end=" ")
        GameText.print_slow(f'"{text}"', 0.02, Fore.CYAN)
        
    @staticmethod
    def display_combat_action(actor, action, target, result):
        """Display a combat action."""
        print(f"{Fore.YELLOW}{actor}{Style.RESET_ALL} {action} {Fore.YELLOW}{target}{Style.RESET_ALL}. {result}")
        
    @staticmethod
    def display_item_found(item_name, description):
        """Display information about an item that was found."""
        print(f"\n{Fore.GREEN}You found: {item_name}!{Style.RESET_ALL}")
        print(description)
        
    @staticmethod
    def display_quest(title, description):
        """Display quest information."""
        GameText.print_box(f"NEW QUEST: {title}", color=Fore.YELLOW)
        GameText.print_slow(description, 0.02, Fore.WHITE)
        
    @staticmethod
    def display_level_up(level, stat_increases):
        """Display level up information."""
        GameText.print_box(f"LEVEL UP! You are now level {level}", color=Fore.YELLOW)
        
        for stat, increase in stat_increases.items():
            print(f"{stat.capitalize()}: +{increase}")
            
        print()
        
    @staticmethod
    def wait_for_input(prompt="Press Enter to continue..."):
        """Wait for the player to press Enter."""
        input(Fore.CYAN + prompt + Style.RESET_ALL) 