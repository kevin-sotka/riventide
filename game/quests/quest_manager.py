"""
Quest management for Riventide
"""

from game.quests.quest import Quest

class QuestManager:
    """Manages quests in the game."""
    
    def __init__(self):
        """Initialize the quest manager."""
        self.quests = {}
        self.quest_templates = self._initialize_quest_templates()
        
    def _initialize_quest_templates(self):
        """Initialize quest templates."""
        templates = {}
        
        # Defend the Realm quest
        templates["defend_the_realm"] = {
            "id": "defend_the_realm",
            "title": "Defend the Realm",
            "description": "King Alaric has tasked you with uncovering Lord Malgrim's spies who have infiltrated Eldoria. Find evidence of their activities and bring it to the King.",
            "objectives": [
                {
                    "id": "find_evidence",
                    "description": "Find evidence of Lord Malgrim's spies",
                    "target": 3
                },
                {
                    "id": "interrogate_suspect",
                    "description": "Interrogate a suspected spy",
                    "target": 1
                },
                {
                    "id": "report_to_king",
                    "description": "Report your findings to King Alaric",
                    "target": 1
                }
            ],
            "rewards": {
                "gold": 500,
                "experience": 200,
                "items": ["royal_signet_ring"],
                "reputation": {"eldoria": 10}
            },
            "giver": "king_alaric",
            "location": "royal_court"
        }
        
        # Royal Summons quest
        templates["royal_summons"] = {
            "id": "royal_summons",
            "title": "Royal Summons",
            "description": "You have received a summons from King Alaric. Travel to the Royal Court to meet with him.",
            "objectives": [
                {
                    "id": "visit_royal_court",
                    "description": "Visit the Royal Court",
                    "target": 1
                }
            ],
            "rewards": {
                "gold": 50,
                "experience": 20
            },
            "giver": "captain_roland",
            "location": "eldoria_capital"
        }
        
        # Add more quest templates as needed
        
        return templates
        
    def create_quest(self, quest_id):
        """
        Create a new quest from a template.
        
        Args:
            quest_id (str): The ID of the quest template to use
            
        Returns:
            Quest: The created quest, or None if the template doesn't exist
        """
        template = self.quest_templates.get(quest_id)
        if not template:
            print(f"Warning: Quest template {quest_id} not found")
            return None
            
        quest = Quest(
            template["id"],
            template["title"],
            template["description"],
            template["objectives"],
            template["rewards"],
            template.get("giver"),
            template.get("location")
        )
        
        self.quests[quest_id] = quest
        return quest
        
    def get_quest(self, quest_id):
        """
        Get a quest by ID.
        
        Args:
            quest_id (str): The ID of the quest
            
        Returns:
            Quest: The quest, or None if it doesn't exist
        """
        return self.quests.get(quest_id)
        
    def activate_quest(self, quest_id):
        """
        Activate a quest.
        
        Args:
            quest_id (str): The ID of the quest
            
        Returns:
            bool: True if the quest was activated, False otherwise
        """
        quest = self.get_quest(quest_id)
        if not quest:
            quest = self.create_quest(quest_id)
            if not quest:
                return False
                
        quest.activate()
        return True
        
    def complete_quest(self, quest_id):
        """
        Complete a quest.
        
        Args:
            quest_id (str): The ID of the quest
            
        Returns:
            bool: True if the quest was completed, False otherwise
        """
        quest = self.get_quest(quest_id)
        if not quest:
            return False
            
        quest.complete()
        return True
        
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
        quest = self.get_quest(quest_id)
        if not quest:
            return False
            
        return quest.update_progress(objective_id, amount)
        
    def get_active_quests(self):
        """
        Get all active quests.
        
        Returns:
            list: A list of active quests
        """
        return [quest for quest in self.quests.values() if quest.active]
        
    def get_completed_quests(self):
        """
        Get all completed quests.
        
        Returns:
            list: A list of completed quests
        """
        return [quest for quest in self.quests.values() if quest.completed]
        
    def get_quests_for_location(self, location_id):
        """
        Get quests available at a location.
        
        Args:
            location_id (str): The ID of the location
            
        Returns:
            list: A list of quests available at the location
        """
        available_quests = []
        
        # Check for quests in templates
        for quest_id, template in self.quest_templates.items():
            if template.get("location") == location_id and quest_id not in self.quests:
                available_quests.append(template)
                
        return available_quests
        
    def to_dict(self):
        """
        Convert the quest manager to a dictionary for saving.
        
        Returns:
            dict: A dictionary representation of the quest manager
        """
        return {
            "quests": {quest_id: quest.to_dict() for quest_id, quest in self.quests.items()}
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a quest manager from a dictionary.
        
        Args:
            data (dict): The dictionary containing quest manager data
            
        Returns:
            QuestManager: A new QuestManager instance
        """
        manager = cls()
        
        for quest_id, quest_data in data.get("quests", {}).items():
            manager.quests[quest_id] = Quest.from_dict(quest_data)
            
        return manager 