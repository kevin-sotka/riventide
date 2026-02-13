"""
Character races for Riventide
"""

RACES = {
    "Human": {
        "description": "Versatile and adaptable, humans are found throughout Riventide",
        "bonuses": {
            "strength": 1,
            "dexterity": 1,
            "intelligence": 1,
            "constitution": 1,
            "wisdom": 1,
            "charisma": 1
        },
        "traits": [
            "Adaptability: Gain experience 10% faster",
            "Versatility: Can use equipment from any race",
            "Diplomacy: +2 to persuasion checks with other humans"
        ],
        "regions": ["Kingdom of Eldoria", "Empire of Drakkar", "Barbarian Lands"]
    },
    "Elf": {
        "description": "Graceful and long-lived beings with a deep connection to nature and magic",
        "bonuses": {
            "dexterity": 2,
            "intelligence": 2,
            "wisdom": 1
        },
        "traits": [
            "Keen Senses: Can see in dim light",
            "Magic Affinity: +10% to spell effectiveness",
            "Longevity: Immune to aging effects",
            "Forest Stealth: +3 to stealth in wooded areas"
        ],
        "regions": ["Realm of Faerie", "Kingdom of Eldoria"]
    },
    "Dwarf": {
        "description": "Stout and sturdy folk with exceptional craftsmanship and resilience",
        "bonuses": {
            "strength": 2,
            "constitution": 3
        },
        "traits": [
            "Stonecunning: Can detect traps and secret doors in stone structures",
            "Resilience: +2 to saving throws against poison and magic",
            "Darkvision: Can see in complete darkness up to 60 feet",
            "Master Crafters: Crafted items are 15% more effective"
        ],
        "regions": ["Kingdom of Eldoria", "Barbarian Lands"]
    },
    "Orc": {
        "description": "Powerful and fierce warriors with a tribal culture and strong battle instincts",
        "bonuses": {
            "strength": 3,
            "constitution": 2,
            "charisma": -1
        },
        "traits": [
            "Battle Fury: +15% damage when below half health",
            "Intimidating Presence: +3 to intimidation checks",
            "Tribal Knowledge: Can identify dangerous creatures and plants",
            "Endurance: Can travel longer without rest"
        ],
        "regions": ["Barbarian Lands", "Empire of Drakkar"]
    },
    "Halfling": {
        "description": "Small but nimble folk known for their luck and stealth",
        "bonuses": {
            "dexterity": 3,
            "charisma": 1,
            "strength": -1
        },
        "traits": [
            "Lucky: Once per day, can reroll any failed check",
            "Nimbleness: +3 to dodge attacks",
            "Stealth: +2 to stealth checks due to small size",
            "Brave Heart: +2 to saving throws against fear"
        ],
        "regions": ["Kingdom of Eldoria", "Realm of Faerie"]
    }
} 