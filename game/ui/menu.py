"""
Menu system for Riventide
"""

import os
import sys
from colorama import Fore, Back, Style

from game.ui.character_creation import CharacterCreation
from game.utils.input_handler import get_input

class MainMenu:
    """Main menu for the game."""
    
    def __init__(self, game_state):
        """Initialize the main menu."""
        self.game_state = game_state
        self.options = [
            "New Game",
            "Gameplay",
            "Credits",
            "Exit"
        ]
        
    def display(self):
        """Display the main menu and handle user input."""
        while True:
            self._clear_screen()
            print(Fore.CYAN + "\n" + "=" * 40)
            print(Fore.YELLOW + "RIVENTIDE" + Style.RESET_ALL)
            print(Fore.CYAN + "=" * 40 + "\n")
            
            for i, option in enumerate(self.options, 1):
                print(f"{Fore.GREEN}{i}.{Style.RESET_ALL} {option}")
                
            print("\n" + Fore.CYAN + "=" * 40 + Style.RESET_ALL)
            
            choice = get_input("\nEnter your choice (1-4): ", 
                              validator=lambda x: x.isdigit() and 1 <= int(x) <= 4)
            
            if choice == "1":
                self._new_game()
            elif choice == "2":
                self._gameplay()
            elif choice == "3":
                self._credits()
            elif choice == "4":
                self._exit_game()
                
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def _new_game(self):
        """Start a new game."""
        character_creation = CharacterCreation(self.game_state)
        player = character_creation.create_character()
        
        if player:
            self.game_state.start_new_game(player)
            # TODO: Start the actual game
            print(Fore.GREEN + "Starting new game..." + Style.RESET_ALL)
            input("Press Enter to continue...")
    
    def _gameplay(self):
        """Display gameplay instructions."""
        self._clear_screen()
        print(Fore.CYAN + "\n" + "=" * 40)
        print(Fore.YELLOW + "GAMEPLAY" + Style.RESET_ALL)
        print(Fore.CYAN + "=" * 40 + "\n")
        
        print(Fore.WHITE + "Riventide is a choose-your-own-adventure story game." + Style.RESET_ALL)
        print("\nHow to play:")
        print("- Use the arrow keys (↑/↓) to navigate between choices")
        print("- Press Enter to select your choice")
        print("- Press Escape to exit the game")
        print("\nNote: This game does not have save points. Each choice you make will")
        print("permanently affect your journey through the story.")
        
        input("\nPress Enter to return to the main menu...")
        
    def _credits(self):
        """Display game credits."""
        self._clear_screen()
        print(Fore.CYAN + "\n" + "=" * 40)
        print(Fore.YELLOW + "CREDITS" + Style.RESET_ALL)
        print(Fore.CYAN + "=" * 40 + "\n")
        
        print(Fore.WHITE + "Riventide" + Style.RESET_ALL)
        print("An Epic Fantasy Adventure\n")
        print("Written and designed by: Kevin Sotka, 2025\n")
        print("Story elements drawn from the Tanis podcast,")
        print("by Terry Miles and Nic Silver\n")
        
        input("\nPress Enter to return to the main menu...")
        
    def _exit_game(self):
        """Exit the game."""
        self._clear_screen()
        print(Fore.YELLOW + "\nThank you for playing Riventide!" + Style.RESET_ALL)
        print("May your adventures continue in other realms...\n")
        sys.exit(0) 