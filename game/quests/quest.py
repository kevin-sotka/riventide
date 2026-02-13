"""
Quest system for Riventide
"""

class Quest:
    """Represents a quest in the game."""
    
    def __init__(self, quest_id, title, description, objectives, rewards, giver=None, location=None):
        """
        Initialize a quest.
        
        Args:
            quest_id (str): Unique identifier for the quest
            title (str): The title of the quest
            description (str): A description of the quest
            objectives (list): A list of objectives to complete
            rewards (dict): The rewards for completing the quest
            giver (str, optional): The NPC who gives the quest
            location (str, optional): The location where the quest is given
        """
        self.id = quest_id
        self.title = title
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.giver = giver
        self.location = location
        self.active = False
        self.completed = False
        self.failed = False
        self.progress = {obj["id"]: 0 for obj in objectives}
        
    def activate(self):
        """Activate the quest."""
        self.active = True
        print(f"Quest activated: {self.title}")
        
    def complete(self):
        """Complete the quest."""
        self.completed = True
        self.active = False
        print(f"Quest completed: {self.title}")
        
    def fail(self):
        """Fail the quest."""
        self.failed = True
        self.active = False
        print(f"Quest failed: {self.title}")
        
    def update_progress(self, objective_id, amount=1):
        """
        Update progress on an objective.
        
        Args:
            objective_id (str): The ID of the objective to update
            amount (int, optional): The amount to increment progress
        
        Returns:
            bool: True if the objective is completed, False otherwise
        """
        if not self.active or self.completed or self.failed:
            return False
            
        # Find the objective
        objective = next((obj for obj in self.objectives if obj["id"] == objective_id), None)
        if not objective:
            print(f"Warning: Objective {objective_id} not found in quest {self.id}")
            return False
            
        # Update progress
        self.progress[objective_id] += amount
        
        # Check if the objective is completed
        if self.progress[objective_id] >= objective["target"]:
            print(f"Objective completed: {objective['description']}")
            
            # Check if all objectives are completed
            all_complete = all(self.progress[obj["id"]] >= obj["target"] for obj in self.objectives)
            if all_complete:
                self.complete()
                return True
                
        return False
        
    def get_progress_text(self):
        """
        Get text describing quest progress.
        
        Returns:
            str: A text description of quest progress
        """
        if not self.active:
            if self.completed:
                return f"{self.title} (Completed)"
            elif self.failed:
                return f"{self.title} (Failed)"
            else:
                return f"{self.title} (Inactive)"
                
        # For active quests, show objective progress
        progress_text = f"{self.title} (Active):\n"
        
        for obj in self.objectives:
            obj_id = obj["id"]
            current = self.progress[obj_id]
            target = obj["target"]
            
            progress_text += f"- {obj['description']}: {current}/{target}\n"
            
        return progress_text
        
    def to_dict(self):
        """
        Convert the quest to a dictionary for saving.
        
        Returns:
            dict: A dictionary representation of the quest
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "objectives": self.objectives,
            "rewards": self.rewards,
            "giver": self.giver,
            "location": self.location,
            "active": self.active,
            "completed": self.completed,
            "failed": self.failed,
            "progress": self.progress
        }
        
    @classmethod
    def from_dict(cls, data):
        """
        Create a quest from a dictionary.
        
        Args:
            data (dict): The dictionary containing quest data
            
        Returns:
            Quest: A new Quest instance
        """
        quest = cls(
            data["id"],
            data["title"],
            data["description"],
            data["objectives"],
            data["rewards"],
            data.get("giver"),
            data.get("location")
        )
        
        quest.active = data["active"]
        quest.completed = data["completed"]
        quest.failed = data["failed"]
        quest.progress = data["progress"]
        
        return quest 