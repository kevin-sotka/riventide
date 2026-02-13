"""
Character classes for Riventide
"""

CLASSES = {
    "Warrior": {
        "description": "A skilled fighter trained in combat and warfare",
        "abilities": [
            "Weapon Mastery", 
            "Heavy Armor Proficiency", 
            "Battle Stance", 
            "Intimidate"
        ],
        "starting_equipment": [
            "Iron Sword",
            "Wooden Shield",
            "Leather Armor",
            "Health Potion (2)"
        ],
        "primary_attributes": ["strength", "constitution"],
        "hit_points_per_level": 10,
        "mana_points_per_level": 2
    },
    "Mage": {
        "description": "A practitioner of arcane arts and magical spells",
        "abilities": [
            "Spellcasting", 
            "Arcane Knowledge", 
            "Mana Regeneration", 
            "Elemental Affinity"
        ],
        "starting_equipment": [
            "Wooden Staff",
            "Spellbook",
            "Cloth Robes",
            "Mana Potion (3)"
        ],
        "primary_attributes": ["intelligence", "wisdom"],
        "hit_points_per_level": 4,
        "mana_points_per_level": 10
    },
    "Rogue": {
        "description": "A stealthy thief skilled in deception and precision strikes",
        "abilities": [
            "Sneak Attack", 
            "Lockpicking", 
            "Evasion", 
            "Pickpocket"
        ],
        "starting_equipment": [
            "Dagger (2)",
            "Thieves' Tools",
            "Leather Armor",
            "Smoke Bomb (2)"
        ],
        "primary_attributes": ["dexterity", "charisma"],
        "hit_points_per_level": 6,
        "mana_points_per_level": 4
    },
    "Healer": {
        "description": "A divine spellcaster focused on healing and protection",
        "abilities": [
            "Healing Magic", 
            "Divine Protection", 
            "Bless", 
            "Turn Undead"
        ],
        "starting_equipment": [
            "Mace",
            "Holy Symbol",
            "Chain Mail",
            "Healing Potion (3)"
        ],
        "primary_attributes": ["wisdom", "charisma"],
        "hit_points_per_level": 6,
        "mana_points_per_level": 8
    },
    "Archer": {
        "description": "A ranged specialist with deadly accuracy from a distance",
        "abilities": [
            "Precise Shot", 
            "Quick Draw", 
            "Eagle Eye", 
            "Trap Setting"
        ],
        "starting_equipment": [
            "Shortbow",
            "Quiver (30 arrows)",
            "Hunting Knife",
            "Leather Armor"
        ],
        "primary_attributes": ["dexterity", "wisdom"],
        "hit_points_per_level": 7,
        "mana_points_per_level": 3
    }
} 