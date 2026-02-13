"""
Game state management for Riventide
"""

import json
import os
from datetime import datetime
from game.world.world import World
from game.quests.quest_manager import QuestManager

class GameState:
    """Manages the state of the game."""
    
    def __init__(self):
        """Initialize the game state."""
        self.world = World()
        self.quest_manager = QuestManager()
        self.player = None
        self.current_location = None
        self.inventory = []
        self.game_time = 360  # Minutes (6:00 AM)
        self.day = 1
        self.day_night_cycle = "day"  # "day" or "night"
        self.story_flags = {
            "met_king": False,
            "found_ancient_artifact": False,
            "defeated_dragon": False
        }
        # Add player modifiers for the new storyline
        self.player_modifiers = {
            "artifact_knowledge": False,
            "protective_rune": False,
            "humming_crystal": False,
            "tech_fragment": False,
            "no_aid": False
        }
        self.current_storyline = "royal_court"  # Track where player is in the story
        
    def reset(self):
        """Reset the game state."""
        # Keep the world reference
        self.player = None
        self.current_location = None
        self.inventory = []
        self.game_time = 360  # Minutes (6:00 AM)
        self.day = 1
        self.day_night_cycle = "day"
        self.story_flags = {
            "met_king": False,
            "found_ancient_artifact": False,
            "defeated_dragon": False
        }
        
        # Reset player modifiers
        self.player_modifiers = {
            "artifact_knowledge": False,
            "protective_rune": False,
            "humming_crystal": False,
            "tech_fragment": False,
            "no_aid": False
        }
        self.current_storyline = "royal_court"
        
        # Reset quest manager
        self.quest_manager = QuestManager()
        
        print("Game state reset for new game")
        
    def set_modifier(self, modifier_name):
        """
        Set a player modifier to True.
        
        Args:
            modifier_name (str): The name of the modifier to set
            
        Returns:
            bool: True if successful, False if modifier doesn't exist
        """
        if modifier_name in self.player_modifiers:
            self.player_modifiers[modifier_name] = True
            print(f"Player modifier set: {modifier_name}")
            return True
        return False
        
    def has_modifier(self, modifier_name):
        """
        Check if the player has a specific modifier.
        
        Args:
            modifier_name (str): The name of the modifier to check
            
        Returns:
            bool: True if the player has the modifier, False otherwise
        """
        return self.player_modifiers.get(modifier_name, False)
        
    def advance_storyline(self, new_storyline):
        """
        Advance the storyline to a new stage.
        
        Args:
            new_storyline (str): The new storyline stage
        """
        self.current_storyline = new_storyline
        print(f"Storyline advanced to: {new_storyline}")
        
    def update_time(self, minutes):
        """
        Update the game time.
        
        Args:
            minutes (int): The number of minutes to advance the time
        """
        self.game_time += minutes
        
        # Check for day change
        if self.game_time >= 1440:  # 24 hours
            self.game_time %= 1440
            self.day += 1
            
        # Update day/night cycle
        if 360 <= self.game_time < 1080:  # 6:00 AM to 6:00 PM
            self.day_night_cycle = "day"
        else:
            self.day_night_cycle = "night"
            
    def get_time_str(self):
        """
        Get a string representation of the game time.
        
        Returns:
            str: The formatted time string (e.g., "6:00 AM")
        """
        hours = self.game_time // 60
        minutes = self.game_time % 60
        
        if hours == 0:
            return f"12:{minutes:02d} AM"
        elif hours < 12:
            return f"{hours}:{minutes:02d} AM"
        elif hours == 12:
            return f"12:{minutes:02d} PM"
        else:
            return f"{hours - 12}:{minutes:02d} PM"
            
    def save_game(self, save_name="save"):
        """
        Save the game state.
        
        Args:
            save_name (str, optional): The name of the save file
            
        Returns:
            bool: True if the save was successful, False otherwise
        """
        # Create save directory if it doesn't exist
        save_dir = os.path.join(os.getcwd(), "saves")
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
            
        # Build the save data
        save_data = {
            "timestamp": datetime.now().isoformat(),
            "player": self.player.to_dict() if self.player else None,
            "current_location": self.current_location["id"] if self.current_location else None,
            "inventory": self.inventory,
            "game_time": self.game_time,
            "day": self.day,
            "day_night_cycle": self.day_night_cycle,
            "story_flags": self.story_flags,
            "player_modifiers": self.player_modifiers,
            "current_storyline": self.current_storyline,
            "quest_manager": self.quest_manager.to_dict()
        }
        
        # Save the game
        save_path = os.path.join(save_dir, f"{save_name}.json")
        try:
            with open(save_path, "w") as f:
                json.dump(save_data, f, indent=2)
            print(f"Game saved to {save_path}")
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
            
    def load_game(self, save_name="save"):
        """
        Load a saved game.
        
        Args:
            save_name (str, optional): The name of the save file
            
        Returns:
            bool: True if the load was successful, False otherwise
        """
        save_path = os.path.join(os.getcwd(), "saves", f"{save_name}.json")
        
        if not os.path.exists(save_path):
            print(f"Save file not found: {save_path}")
            return False
            
        try:
            with open(save_path, "r") as f:
                save_data = json.load(f)
                
            # Load player data
            if save_data.get("player"):
                from game.characters.player import Player
                self.player = Player.from_dict(save_data["player"])
                
            # Load location
            location_id = save_data.get("current_location")
            if location_id:
                self.current_location = self.world.get_location(location_id)
                
            # Load other data
            self.inventory = save_data.get("inventory", [])
            self.game_time = save_data.get("game_time", 360)
            self.day = save_data.get("day", 1)
            self.day_night_cycle = save_data.get("day_night_cycle", "day")
            self.story_flags = save_data.get("story_flags", {})
            self.player_modifiers = save_data.get("player_modifiers", {
                "artifact_knowledge": False,
                "protective_rune": False,
                "humming_crystal": False,
                "tech_fragment": False,
                "no_aid": False
            })
            self.current_storyline = save_data.get("current_storyline", "royal_court")
            
            # Load quest manager
            quest_data = save_data.get("quest_manager", {"quests": {}})
            self.quest_manager = QuestManager.from_dict(quest_data)
            
            print(f"Game loaded from {save_path}")
            return True
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
            
    def add_quest(self, quest_id):
        """
        Add a quest to the player's quest log.
        
        Args:
            quest_id (str): The ID of the quest to add
            
        Returns:
            bool: True if the quest was added, False otherwise
        """
        return self.quest_manager.activate_quest(quest_id)
        
    def complete_quest(self, quest_id):
        """
        Complete a quest in the player's quest log.
        
        Args:
            quest_id (str): The ID of the quest to complete
            
        Returns:
            bool: True if the quest was completed, False otherwise
        """
        return self.quest_manager.complete_quest(quest_id)
        
    def update_quest_progress(self, quest_id, objective_id, amount=1):
        """
        Update progress on a quest objective.
        
        Args:
            quest_id (str): The ID of the quest
            objective_id (str): The ID of the objective
            amount (int, optional): The amount to increment progress
            
        Returns:
            bool: True if the objective was updated, False otherwise
        """
        return self.quest_manager.update_quest_progress(quest_id, objective_id, amount)
        
    def get_active_quests(self):
        """
        Get all active quests.
        
        Returns:
            list: A list of active quests
        """
        return self.quest_manager.get_active_quests()
        
    def get_completed_quests(self):
        """
        Get all completed quests.
        
        Returns:
            list: A list of completed quests
        """
        return self.quest_manager.get_completed_quests()
        
    def get_quests_for_location(self, location_id):
        """
        Get quests available at a location.
        
        Args:
            location_id (str): The ID of the location
            
        Returns:
            list: A list of quests available at the location
        """
        return self.quest_manager.get_quests_for_location(location_id) 