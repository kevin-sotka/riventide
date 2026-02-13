"""
Player character class for Riventide
"""

from game.characters.character_classes import CLASSES
from game.characters.character_races import RACES

class Player:
    """Represents the player character in the game."""
    
    def __init__(self, name, race, character_class, attributes):
        """Initialize a new player character."""
        self.name = name
        self.race = race
        self.character_class = character_class
        self.attributes = attributes
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100  # Base XP needed for level 2
        
        # Calculate derived stats
        self._calculate_stats()
        
        # Initialize equipment and inventory
        self.equipment = {
            "weapon": None,
            "armor": None,
            "shield": None,
            "accessory": None
        }
        
        # Add starting equipment
        self.inventory = []
        self._add_starting_equipment()
        
        # Initialize skills based on class and attributes
        self.skills = self._initialize_skills()
        
        # Initialize spells/abilities
        self.abilities = []
        self._add_class_abilities()
        
        # Status effects
        self.status_effects = []
        
    def _calculate_stats(self):
        """Calculate derived stats based on attributes and class."""
        # Get class info
        class_info = CLASSES[self.character_class]
        
        # Base hit points and mana
        base_hp = class_info["hit_points_per_level"]
        base_mp = class_info["mana_points_per_level"]
        
        # Constitution bonus to HP (each point above 10 gives +5% HP)
        con_bonus = 1 + max(0, (self.attributes["constitution"] - 10) * 0.05)
        
        # Intelligence/Wisdom bonus to MP (each point above 10 gives +5% MP)
        if "intelligence" in class_info["primary_attributes"]:
            mp_attr = "intelligence"
        else:
            mp_attr = "wisdom"
            
        mp_bonus = 1 + max(0, (self.attributes[mp_attr] - 10) * 0.05)
        
        # Calculate final values
        self.max_hit_points = int(base_hp * con_bonus)
        self.hit_points = self.max_hit_points
        
        self.max_mana_points = int(base_mp * mp_bonus)
        self.mana_points = self.max_mana_points
        
        # Combat stats
        self.attack_power = self._calculate_attack_power()
        self.defense = self._calculate_defense()
        self.magic_power = self._calculate_magic_power()
        self.speed = self._calculate_speed()
        
    def _calculate_attack_power(self):
        """Calculate attack power based on attributes and class."""
        if self.character_class in ["Warrior", "Archer"]:
            primary_attr = "strength" if self.character_class == "Warrior" else "dexterity"
            return 5 + self.attributes[primary_attr] // 2
        else:
            return 3 + max(self.attributes["strength"], self.attributes["dexterity"]) // 3
            
    def _calculate_defense(self):
        """Calculate defense based on attributes."""
        return 2 + self.attributes["constitution"] // 4
        
    def _calculate_magic_power(self):
        """Calculate magic power based on attributes and class."""
        if self.character_class in ["Mage", "Healer"]:
            primary_attr = "intelligence" if self.character_class == "Mage" else "wisdom"
            return 5 + self.attributes[primary_attr] // 2
        else:
            return 1 + max(self.attributes["intelligence"], self.attributes["wisdom"]) // 5
            
    def _calculate_speed(self):
        """Calculate speed based on attributes."""
        return 5 + self.attributes["dexterity"] // 3
        
    def _add_starting_equipment(self):
        """Add starting equipment based on character class."""
        starting_items = CLASSES[self.character_class]["starting_equipment"]
        
        for item in starting_items:
            self.inventory.append(item)
            
    def _initialize_skills(self):
        """Initialize skills based on class and attributes."""
        skills = {
            "melee": 0,
            "ranged": 0,
            "magic": 0,
            "stealth": 0,
            "persuasion": 0,
            "perception": 0,
            "survival": 0,
            "crafting": 0
        }
        
        # Set base skills based on class
        if self.character_class == "Warrior":
            skills["melee"] = 3
            skills["survival"] = 2
        elif self.character_class == "Mage":
            skills["magic"] = 3
            skills["persuasion"] = 1
        elif self.character_class == "Rogue":
            skills["stealth"] = 3
            skills["ranged"] = 1
            skills["perception"] = 2
        elif self.character_class == "Healer":
            skills["magic"] = 2
            skills["persuasion"] = 2
            skills["perception"] = 1
        elif self.character_class == "Archer":
            skills["ranged"] = 3
            skills["perception"] = 2
            skills["survival"] = 1
            
        # Attribute bonuses to skills
        skills["melee"] += self.attributes["strength"] // 5
        skills["ranged"] += self.attributes["dexterity"] // 5
        skills["magic"] += max(self.attributes["intelligence"], self.attributes["wisdom"]) // 5
        skills["stealth"] += self.attributes["dexterity"] // 5
        skills["persuasion"] += self.attributes["charisma"] // 5
        skills["perception"] += self.attributes["wisdom"] // 5
        skills["survival"] += self.attributes["constitution"] // 5
        skills["crafting"] += self.attributes["intelligence"] // 5
        
        return skills
        
    def _add_class_abilities(self):
        """Add starting abilities based on character class."""
        class_abilities = CLASSES[self.character_class]["abilities"]
        
        # For now, just add the ability names
        # In a full implementation, these would be actual ability objects
        for ability in class_abilities:
            self.abilities.append(ability)
            
    def gain_experience(self, amount):
        """Gain experience points and level up if necessary."""
        self.experience += amount
        
        if self.experience >= self.experience_to_level:
            self.level_up()
            
    def level_up(self):
        """Level up the character."""
        self.level += 1
        
        # Reset experience and calculate new threshold (increases by 50% each level)
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)
        
        # Increase stats
        class_info = CLASSES[self.character_class]
        
        # Increase HP and MP
        base_hp_increase = class_info["hit_points_per_level"]
        base_mp_increase = class_info["mana_points_per_level"]
        
        con_bonus = 1 + max(0, (self.attributes["constitution"] - 10) * 0.05)
        
        if "intelligence" in class_info["primary_attributes"]:
            mp_attr = "intelligence"
        else:
            mp_attr = "wisdom"
            
        mp_bonus = 1 + max(0, (self.attributes[mp_attr] - 10) * 0.05)
        
        hp_increase = int(base_hp_increase * con_bonus)
        mp_increase = int(base_mp_increase * mp_bonus)
        
        self.max_hit_points += hp_increase
        self.hit_points = self.max_hit_points
        
        self.max_mana_points += mp_increase
        self.mana_points = self.max_mana_points
        
        # Recalculate combat stats
        self.attack_power = self._calculate_attack_power()
        self.defense = self._calculate_defense()
        self.magic_power = self._calculate_magic_power()
        self.speed = self._calculate_speed()
        
        # TODO: Add new abilities at certain levels
        
    def to_dict(self):
        """Convert the player to a dictionary for saving."""
        return {
            "name": self.name,
            "race": self.race,
            "character_class": self.character_class,
            "attributes": self.attributes,
            "level": self.level,
            "experience": self.experience,
            "experience_to_level": self.experience_to_level,
            "max_hit_points": self.max_hit_points,
            "hit_points": self.hit_points,
            "max_mana_points": self.max_mana_points,
            "mana_points": self.mana_points,
            "attack_power": self.attack_power,
            "defense": self.defense,
            "magic_power": self.magic_power,
            "speed": self.speed,
            "equipment": self.equipment,
            "inventory": self.inventory,
            "skills": self.skills,
            "abilities": self.abilities,
            "status_effects": self.status_effects
        }
        
    @classmethod
    def from_dict(cls, data):
        """Create a player from a dictionary."""
        player = cls(
            name=data["name"],
            race=data["race"],
            character_class=data["character_class"],
            attributes=data["attributes"]
        )
        
        # Override calculated values with saved values
        player.level = data["level"]
        player.experience = data["experience"]
        player.experience_to_level = data["experience_to_level"]
        player.max_hit_points = data["max_hit_points"]
        player.hit_points = data["hit_points"]
        player.max_mana_points = data["max_mana_points"]
        player.mana_points = data["mana_points"]
        player.attack_power = data["attack_power"]
        player.defense = data["defense"]
        player.magic_power = data["magic_power"]
        player.speed = data["speed"]
        player.equipment = data["equipment"]
        player.inventory = data["inventory"]
        player.skills = data["skills"]
        player.abilities = data["abilities"]
        player.status_effects = data["status_effects"]
        
        return player 