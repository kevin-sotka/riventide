"""
Character creation system for Riventide
"""

import os
from colorama import Fore, Back, Style

from game.utils.input_handler import get_input, get_choice, confirm
from game.characters.player import Player
from game.characters.character_classes import CLASSES
from game.characters.character_races import RACES

class CharacterCreation:
    """Character creation interface for the game."""
    
    def __init__(self, game_state):
        """Initialize the character creation interface."""
        self.game_state = game_state
        
    def create_character(self):
        """Guide the player through character creation."""
        self._clear_screen()
        print(Fore.CYAN + "\n" + "=" * 60)
        print(Fore.YELLOW + "CHARACTER CREATION" + Style.RESET_ALL)
        print(Fore.CYAN + "=" * 60 + "\n")
        
        print(Fore.WHITE + "Welcome, adventurer! Let's create your character for the journey ahead." + Style.RESET_ALL)
        print("Your choices will determine your strengths, weaknesses, and abilities in the world of Riventide.\n")
        
        # Get character name
        name = self._get_character_name()
        if name is None:  # User chose to go back
            return None
            
        # Choose race
        race_index = self._choose_race()
        if race_index == -1:  # User chose to go back
            return None
        race = list(RACES.keys())[race_index]
        
        # Choose class
        class_index = self._choose_class()
        if class_index == -1:  # User chose to go back
            return None
        character_class = list(CLASSES.keys())[class_index]
        
        # Allocate attribute points
        attributes = self._allocate_attributes(race)
        if attributes is None:  # User chose to go back
            return None
            
        # Review and confirm
        if not self._review_character(name, race, character_class, attributes):
            return self.create_character()  # Start over
            
        # Create the player character
        player = Player(
            name=name,
            race=race,
            character_class=character_class,
            attributes=attributes
        )
        
        return player
        
    def _clear_screen(self):
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def _get_character_name(self):
        """Get the character name from the player."""
        print(Fore.CYAN + "\nCHOOSE YOUR NAME" + Style.RESET_ALL)
        print("What shall you be known as in the realm of Riventide?")
        
        while True:
            name = get_input("\nEnter your character's name (or 'back' to return): ")
            
            if name.lower() == 'back':
                return None
                
            if len(name) < 2:
                print(Fore.RED + "Your name must be at least 2 characters long." + Style.RESET_ALL)
                continue
                
            if len(name) > 20:
                print(Fore.RED + "Your name must be no more than 20 characters long." + Style.RESET_ALL)
                continue
                
            return name
            
    def _choose_race(self):
        """Let the player choose a character race."""
        self._clear_screen()
        print(Fore.CYAN + "\nCHOOSE YOUR RACE" + Style.RESET_ALL)
        print("Each race has unique traits and bonuses that will affect your journey.")
        
        race_options = []
        for race, details in RACES.items():
            description = f"{race}: {details['description']}"
            bonuses = ", ".join([f"+{v} {k.capitalize()}" for k, v in details['bonuses'].items()])
            race_options.append(f"{description}\n   Bonuses: {bonuses}")
            
        return get_choice("Select your race:", race_options)
        
    def _choose_class(self):
        """Let the player choose a character class."""
        self._clear_screen()
        print(Fore.CYAN + "\nCHOOSE YOUR CLASS" + Style.RESET_ALL)
        print("Your class determines your abilities, combat style, and role in the world.")
        
        class_options = []
        for cls, details in CLASSES.items():
            description = f"{cls}: {details['description']}"
            abilities = ", ".join(details['abilities'])
            class_options.append(f"{description}\n   Abilities: {abilities}")
            
        return get_choice("Select your class:", class_options)
        
    def _allocate_attributes(self, race):
        """Let the player allocate attribute points."""
        self._clear_screen()
        print(Fore.CYAN + "\nALLOCATE ATTRIBUTES" + Style.RESET_ALL)
        print("Distribute points among your character's attributes.")
        print("These will determine your effectiveness in various situations.")
        
        # Base attributes
        attributes = {
            "strength": 8,
            "dexterity": 8,
            "intelligence": 8,
            "constitution": 8,
            "wisdom": 8,
            "charisma": 8
        }
        
        # Apply racial bonuses
        race_bonuses = RACES[race]["bonuses"]
        for attr, bonus in race_bonuses.items():
            attributes[attr] += bonus
            
        # Points to allocate
        points_remaining = 10
        
        while points_remaining > 0:
            self._clear_screen()
            print(Fore.CYAN + "\nALLOCATE ATTRIBUTES" + Style.RESET_ALL)
            print(f"Points remaining: {Fore.GREEN}{points_remaining}{Style.RESET_ALL}\n")
            
            print("Current attributes:")
            for attr, value in attributes.items():
                # Show racial bonuses
                bonus = race_bonuses.get(attr, 0)
                bonus_text = f" (+{bonus} from {race})" if bonus > 0 else ""
                print(f"{attr.capitalize()}: {Fore.YELLOW}{value}{Style.RESET_ALL}{bonus_text}")
                
            print("\nChoose an attribute to increase:")
            attr_options = list(attributes.keys())
            
            attr_index = get_choice("Select attribute to increase:", 
                                   [a.capitalize() for a in attr_options], 
                                   allow_back=points_remaining < 10)
                                   
            if attr_index == -1:
                if confirm("Return to character creation?"):
                    return None
                continue
                
            attr = attr_options[attr_index]
            attributes[attr] += 1
            points_remaining -= 1
            
        return attributes
        
    def _review_character(self, name, race, character_class, attributes):
        """Review and confirm the character."""
        self._clear_screen()
        print(Fore.CYAN + "\nREVIEW YOUR CHARACTER" + Style.RESET_ALL)
        print("Please review your character before finalizing.")
        
        print(f"\nName: {Fore.YELLOW}{name}{Style.RESET_ALL}")
        print(f"Race: {Fore.YELLOW}{race}{Style.RESET_ALL}")
        print(f"Class: {Fore.YELLOW}{character_class}{Style.RESET_ALL}")
        
        print("\nAttributes:")
        for attr, value in attributes.items():
            print(f"{attr.capitalize()}: {Fore.YELLOW}{value}{Style.RESET_ALL}")
            
        print("\nRacial traits:")
        print(RACES[race]["description"])
        
        print("\nClass abilities:")
        for ability in CLASSES[character_class]["abilities"]:
            print(f"- {ability}")
            
        return confirm("\nDo you want to proceed with this character?") 