"""
Graphical character creation screen for Riventide
"""

import pygame
from enum import Enum

from game.characters.player import Player
from game.characters.character_classes import CLASSES
from game.characters.character_races import RACES

class CreationStage(Enum):
    """Stages of character creation."""
    NAME = "name"
    RACE = "race"
    CLASS = "class"
    ATTRIBUTES = "attributes"
    REVIEW = "review"
    COMPLETE = "complete"

class CharacterCreationScreen:
    """Graphical character creation screen."""
    
    def __init__(self, game_engine):
        """Initialize the character creation screen."""
        self.game_engine = game_engine
        self.graphics = game_engine.graphics
        self.audio = game_engine.audio
        self.width = game_engine.width
        self.height = game_engine.height
        
        # Character creation state
        self.stage = CreationStage.NAME
        self.name = ""
        self.race = None
        self.character_class = None
        self.attributes = {
            "strength": 8,
            "dexterity": 8,
            "intelligence": 8,
            "constitution": 8,
            "wisdom": 8,
            "charisma": 8
        }
        self.points_remaining = 10
        self.selected_option = 0
        self.typing_active = False
        self.name_cursor_visible = True
        self.cursor_blink_timer = 0
        
        # For attribute allocation
        self.selected_attribute = 0
        
        # For scrolling text
        self.scroll_offset = 0
        self.max_scroll = 0
        
        # Load portraits
        self.race_portraits = {}
        self.class_portraits = {}
        
    def handle_event(self, event):
        """Handle pygame events."""
        if event.type == pygame.KEYDOWN:
            if self.stage == CreationStage.NAME:
                self._handle_name_input(event)
            elif self.stage == CreationStage.RACE:
                self._handle_race_selection(event)
            elif self.stage == CreationStage.CLASS:
                self._handle_class_selection(event)
            elif self.stage == CreationStage.ATTRIBUTES:
                self._handle_attribute_allocation(event)
            elif self.stage == CreationStage.REVIEW:
                self._handle_review(event)
                
    def _handle_name_input(self, event):
        """Handle name input events."""
        if event.key == pygame.K_RETURN:
            if len(self.name) >= 2:
                self.stage = CreationStage.RACE
                self.selected_option = 0
                if self.audio:
                    self.audio.play_sound("menu_select")
        elif event.key == pygame.K_BACKSPACE:
            self.name = self.name[:-1]
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_ESCAPE:
            # Return to main menu
            self.game_engine.mode = self.game_engine.GameMode.MENU
            if self.audio:
                self.audio.play_sound("menu_select")
        elif len(self.name) < 20 and event.unicode.isprintable():
            self.name += event.unicode
            if self.audio:
                self.audio.play_sound("menu_select")
                
    def _handle_race_selection(self, event):
        """Handle race selection events."""
        if event.key == pygame.K_RETURN:
            self.race = list(RACES.keys())[self.selected_option]
            self.stage = CreationStage.CLASS
            self.selected_option = 0
            self.scroll_offset = 0
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_UP:
            self.selected_option = max(0, self.selected_option - 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_DOWN:
            self.selected_option = min(len(RACES) - 1, self.selected_option + 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_ESCAPE:
            self.stage = CreationStage.NAME
            if self.audio:
                self.audio.play_sound("menu_select")
                
    def _handle_class_selection(self, event):
        """Handle class selection events."""
        if event.key == pygame.K_RETURN:
            self.character_class = list(CLASSES.keys())[self.selected_option]
            
            # Reset attributes and apply racial bonuses
            self.attributes = {
                "strength": 8,
                "dexterity": 8,
                "intelligence": 8,
                "constitution": 8,
                "wisdom": 8,
                "charisma": 8
            }
            
            race_bonuses = RACES[self.race]["bonuses"]
            for attr, bonus in race_bonuses.items():
                self.attributes[attr] += bonus
                
            self.points_remaining = 10
            self.stage = CreationStage.ATTRIBUTES
            self.selected_attribute = 0
            self.scroll_offset = 0
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_UP:
            self.selected_option = max(0, self.selected_option - 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_DOWN:
            self.selected_option = min(len(CLASSES) - 1, self.selected_option + 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_ESCAPE:
            self.stage = CreationStage.RACE
            if self.audio:
                self.audio.play_sound("menu_select")
                
    def _handle_attribute_allocation(self, event):
        """Handle attribute allocation events."""
        attr_keys = list(self.attributes.keys())
        
        if event.key == pygame.K_RETURN:
            if self.points_remaining == 0:
                self.stage = CreationStage.REVIEW
                if self.audio:
                    self.audio.play_sound("menu_select")
        elif event.key == pygame.K_UP:
            self.selected_attribute = max(0, self.selected_attribute - 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_DOWN:
            self.selected_attribute = min(len(attr_keys) - 1, self.selected_attribute + 1)
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_RIGHT and self.points_remaining > 0:
            # Increase selected attribute
            attr = attr_keys[self.selected_attribute]
            self.attributes[attr] += 1
            self.points_remaining -= 1
            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_LEFT:
            # Decrease selected attribute (but not below base + racial bonus)
            attr = attr_keys[self.selected_attribute]
            base_value = 8
            racial_bonus = RACES[self.race]["bonuses"].get(attr, 0)
            min_value = base_value + racial_bonus
            
            if self.attributes[attr] > min_value:
                self.attributes[attr] -= 1
                self.points_remaining += 1
                if self.audio:
                    self.audio.play_sound("menu_select")
        elif event.key == pygame.K_ESCAPE:
            if self.points_remaining < 10:
                # Reset attributes if points have been spent
                self.attributes = {
                    "strength": 8,
                    "dexterity": 8,
                    "intelligence": 8,
                    "constitution": 8,
                    "wisdom": 8,
                    "charisma": 8
                }
                
                race_bonuses = RACES[self.race]["bonuses"]
                for attr, bonus in race_bonuses.items():
                    self.attributes[attr] += bonus
                    
                self.points_remaining = 10
            else:
                self.stage = CreationStage.CLASS
                
            if self.audio:
                self.audio.play_sound("menu_select")
                
    def _handle_review(self, event):
        """Handle review events."""
        if event.key == pygame.K_RETURN:
            # Create the player character
            player = Player(
                name=self.name,
                race=self.race,
                character_class=self.character_class,
                attributes=self.attributes
            )

            # Start the game FIRST. _start_new_game() calls game_state.reset(),
            # which wipes both game_state.player and player_modifiers back to
            # their defaults - so anything we set before this call would be
            # discarded. Everything below must happen AFTER this line.
            self.game_engine._start_new_game()

            # Set the player in the game state
            self.game_engine.game_state.player = player

            # Record the race/class choice as modifiers for the choice-gating
            # system (game.engine.available_choices). Fires exactly once,
            # right here, before the first story location's choices are ever
            # evaluated. Modifier names must match the "race_<id>"/"class_<id>"
            # entries declared in GameState.player_modifiers.
            race_modifier = f"race_{self.race.lower()}"
            class_modifier = f"class_{self.character_class.lower()}"
            if not self.game_engine.game_state.set_modifier(race_modifier):
                print(f"Warning: unknown race modifier '{race_modifier}' - not registered in GameState.player_modifiers")
            if not self.game_engine.game_state.set_modifier(class_modifier):
                print(f"Warning: unknown class modifier '{class_modifier}' - not registered in GameState.player_modifiers")

            if self.audio:
                self.audio.play_sound("menu_select")
        elif event.key == pygame.K_ESCAPE:
            self.stage = CreationStage.ATTRIBUTES
            if self.audio:
                self.audio.play_sound("menu_select")
                
    def update(self, dt):
        """Update the character creation screen."""
        # Update cursor blink timer for name input
        if self.stage == CreationStage.NAME:
            self.cursor_blink_timer += dt
            if self.cursor_blink_timer >= 0.5:  # Blink every half second
                self.name_cursor_visible = not self.name_cursor_visible
                self.cursor_blink_timer = 0
                
    def render(self):
        """Render the character creation screen."""
        # Clear the screen
        self.graphics.clear((0, 0, 50))  # Dark blue background
        
        # Draw title
        title_text = "CHARACTER CREATION"
        self.graphics.draw_text_box(
            title_text, 
            (self.width // 4, 20), 
            (self.width // 2, 50), 
            font_size=36, 
            text_color=(255, 255, 100),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Render the current stage
        if self.stage == CreationStage.NAME:
            self._render_name_stage()
        elif self.stage == CreationStage.RACE:
            self._render_race_stage()
        elif self.stage == CreationStage.CLASS:
            self._render_class_stage()
        elif self.stage == CreationStage.ATTRIBUTES:
            self._render_attributes_stage()
        elif self.stage == CreationStage.REVIEW:
            self._render_review_stage()
            
        # Draw navigation help
        help_text = ""
        if self.stage == CreationStage.NAME:
            help_text = "Type your name and press Enter to continue. Press Esc to return to menu."
        elif self.stage == CreationStage.RACE:
            help_text = "Use Up/Down to select a race. Press Enter to confirm or Esc to go back."
        elif self.stage == CreationStage.CLASS:
            help_text = "Use Up/Down to select a class. Press Enter to confirm or Esc to go back."
        elif self.stage == CreationStage.ATTRIBUTES:
            help_text = "Use Up/Down to select attribute, Left/Right to adjust. Press Enter when done or Esc to go back."
        elif self.stage == CreationStage.REVIEW:
            help_text = "Press Enter to create character and start game, or Esc to go back."
            
        self.graphics.draw_text_box(
            help_text, 
            (50, self.height - 50), 
            (self.width - 100, 40), 
            font_size=16, 
            text_color=(200, 200, 200),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
    def _render_name_stage(self):
        """Render the name input stage."""
        prompt_text = "What is your name, adventurer?"
        self.graphics.draw_text_box(
            prompt_text, 
            (self.width // 4, 100), 
            (self.width // 2, 40), 
            font_size=24, 
            text_color=(255, 255, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw name input box
        name_display = self.name
        if self.name_cursor_visible:
            name_display += "|"
            
        self.graphics.draw_text_box(
            name_display, 
            (self.width // 4, 160), 
            (self.width // 2, 50), 
            font_size=28, 
            text_color=(255, 255, 255),
            bg_color=(20, 20, 70),
            border_color=(100, 100, 200)
        )
        
    def _render_race_stage(self):
        """Render the race selection stage."""
        prompt_text = "Choose your race:"
        self.graphics.draw_text_box(
            prompt_text, 
            (self.width // 4, 80), 
            (self.width // 2, 40), 
            font_size=24, 
            text_color=(255, 255, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw race options
        y_pos = 130
        visible_races = list(RACES.keys())
        
        # Handle scrolling if needed
        max_visible = 4  # Maximum number of races visible at once
        if len(visible_races) > max_visible:
            # Adjust selected option to ensure it's visible
            if self.selected_option < self.scroll_offset:
                self.scroll_offset = self.selected_option
            elif self.selected_option >= self.scroll_offset + max_visible:
                self.scroll_offset = self.selected_option - max_visible + 1
                
            # Limit scroll offset
            self.scroll_offset = min(max(0, self.scroll_offset), len(visible_races) - max_visible)
            
            # Only show visible races
            visible_races = visible_races[self.scroll_offset:self.scroll_offset + max_visible]
            
        for i, race_name in enumerate(visible_races):
            actual_index = i + self.scroll_offset
            race_info = RACES[race_name]
            
            # Determine colors based on selection
            if actual_index == self.selected_option:
                text_color = (255, 255, 100)  # Yellow for selected option
                bg_color = (50, 50, 100)      # Lighter blue background
                border_color = (200, 200, 100)  # Yellow border
            else:
                text_color = (255, 255, 255)  # White for unselected options
                bg_color = (20, 20, 70)       # Dark blue background
                border_color = (100, 100, 200)  # Blue border
                
            # Draw race name and description
            race_text = f"{race_name}: {race_info['description']}"
            self.graphics.draw_text_box(
                race_text, 
                (100, y_pos), 
                (self.width - 200, 60), 
                font_size=20,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
            # Draw racial bonuses
            bonuses_text = "Bonuses: " + ", ".join([f"+{v} {k.capitalize()}" for k, v in race_info['bonuses'].items()])
            self.graphics.draw_text_box(
                bonuses_text, 
                (120, y_pos + 60), 
                (self.width - 240, 30), 
                font_size=16,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
            y_pos += 100
            
        # Draw scroll indicators if needed
        if len(RACES) > max_visible:
            if self.scroll_offset > 0:
                # Draw up arrow
                self.graphics.draw_text_box(
                    "▲ More races above", 
                    (self.width // 2 - 100, 130 - 30), 
                    (200, 25), 
                    font_size=16,
                    text_color=(200, 200, 200),
                    bg_color=(0, 0, 50),
                    border_color=(0, 0, 50)
                )
                
            if self.scroll_offset + max_visible < len(RACES):
                # Draw down arrow
                self.graphics.draw_text_box(
                    "▼ More races below", 
                    (self.width // 2 - 100, y_pos + 10), 
                    (200, 25), 
                    font_size=16,
                    text_color=(200, 200, 200),
                    bg_color=(0, 0, 50),
                    border_color=(0, 0, 50)
                )
                
    def _render_class_stage(self):
        """Render the class selection stage."""
        prompt_text = "Choose your class:"
        self.graphics.draw_text_box(
            prompt_text, 
            (self.width // 4, 80), 
            (self.width // 2, 40), 
            font_size=24, 
            text_color=(255, 255, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw class options
        y_pos = 130
        visible_classes = list(CLASSES.keys())
        
        # Handle scrolling if needed
        max_visible = 4  # Maximum number of classes visible at once
        if len(visible_classes) > max_visible:
            # Adjust selected option to ensure it's visible
            if self.selected_option < self.scroll_offset:
                self.scroll_offset = self.selected_option
            elif self.selected_option >= self.scroll_offset + max_visible:
                self.scroll_offset = self.selected_option - max_visible + 1
                
            # Limit scroll offset
            self.scroll_offset = min(max(0, self.scroll_offset), len(visible_classes) - max_visible)
            
            # Only show visible classes
            visible_classes = visible_classes[self.scroll_offset:self.scroll_offset + max_visible]
            
        for i, class_name in enumerate(visible_classes):
            actual_index = i + self.scroll_offset
            class_info = CLASSES[class_name]
            
            # Determine colors based on selection
            if actual_index == self.selected_option:
                text_color = (255, 255, 100)  # Yellow for selected option
                bg_color = (50, 50, 100)      # Lighter blue background
                border_color = (200, 200, 100)  # Yellow border
            else:
                text_color = (255, 255, 255)  # White for unselected options
                bg_color = (20, 20, 70)       # Dark blue background
                border_color = (100, 100, 200)  # Blue border
                
            # Draw class name and description
            class_text = f"{class_name}: {class_info['description']}"
            self.graphics.draw_text_box(
                class_text, 
                (100, y_pos), 
                (self.width - 200, 60), 
                font_size=20,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
            # Draw class abilities
            abilities_text = "Abilities: " + ", ".join(class_info['abilities'])
            self.graphics.draw_text_box(
                abilities_text, 
                (120, y_pos + 60), 
                (self.width - 240, 30), 
                font_size=16,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
            y_pos += 100
            
        # Draw scroll indicators if needed
        if len(CLASSES) > max_visible:
            if self.scroll_offset > 0:
                # Draw up arrow
                self.graphics.draw_text_box(
                    "▲ More classes above", 
                    (self.width // 2 - 100, 130 - 30), 
                    (200, 25), 
                    font_size=16,
                    text_color=(200, 200, 200),
                    bg_color=(0, 0, 50),
                    border_color=(0, 0, 50)
                )
                
            if self.scroll_offset + max_visible < len(CLASSES):
                # Draw down arrow
                self.graphics.draw_text_box(
                    "▼ More classes below", 
                    (self.width // 2 - 100, y_pos + 10), 
                    (200, 25), 
                    font_size=16,
                    text_color=(200, 200, 200),
                    bg_color=(0, 0, 50),
                    border_color=(0, 0, 50)
                )
                
    def _render_attributes_stage(self):
        """Render the attribute allocation stage."""
        prompt_text = f"Allocate Attributes - Points Remaining: {self.points_remaining}"
        self.graphics.draw_text_box(
            prompt_text, 
            (self.width // 4, 80), 
            (self.width // 2, 40), 
            font_size=24, 
            text_color=(255, 255, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw attributes
        y_pos = 130
        attr_keys = list(self.attributes.keys())
        for i, attr in enumerate(attr_keys):
            value = self.attributes[attr]
            
            # Determine colors based on selection
            if i == self.selected_attribute:
                text_color = (255, 255, 100)  # Yellow for selected option
                bg_color = (50, 50, 100)      # Lighter blue background
                border_color = (200, 200, 100)  # Yellow border
            else:
                text_color = (255, 255, 255)  # White for unselected options
                bg_color = (20, 20, 70)       # Dark blue background
                border_color = (100, 100, 200)  # Blue border
                
            # Show racial bonus if any
            racial_bonus = RACES[self.race]["bonuses"].get(attr, 0)
            bonus_text = f" (+{racial_bonus} from {self.race})" if racial_bonus > 0 else ""
            
            # Draw attribute name and value
            attr_text = f"{attr.capitalize()}: {value}{bonus_text}"
            self.graphics.draw_text_box(
                attr_text, 
                (self.width // 4, y_pos), 
                (self.width // 2, 40), 
                font_size=20,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
            y_pos += 50
            
        # Draw class recommendation
        if self.character_class:
            class_info = CLASSES[self.character_class]
            primary_attrs = class_info["primary_attributes"]
            
            recommendation_text = f"Recommended for {self.character_class}: {', '.join(a.capitalize() for a in primary_attrs)}"
            self.graphics.draw_text_box(
                recommendation_text, 
                (self.width // 4, y_pos + 20), 
                (self.width // 2, 40), 
                font_size=18,
                text_color=(200, 200, 255),
                bg_color=(0, 0, 50),
                border_color=(0, 0, 50)
            )
            
    def _render_review_stage(self):
        """Render the character review stage."""
        prompt_text = "Review Your Character"
        self.graphics.draw_text_box(
            prompt_text, 
            (self.width // 4, 80), 
            (self.width // 2, 40), 
            font_size=24, 
            text_color=(255, 255, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw character summary with proper line breaks
        summary_text = f"Name: {self.name}\nRace: {self.race}\nClass: {self.character_class}"
        self.graphics.draw_text_box(
            summary_text, 
            (100, 130), 
            (self.width - 200, 80), 
            font_size=20,
            text_color=(255, 255, 255),
            bg_color=(20, 20, 70),
            border_color=(100, 100, 200)
        )
        
        # Draw attributes with proper line breaks
        attr_lines = []
        for attr, value in self.attributes.items():
            attr_lines.append(f"{attr.capitalize()}: {value}")
        attr_text = "Attributes:\n" + "\n".join(attr_lines)
        
        self.graphics.draw_text_box(
            attr_text, 
            (100, 220), 
            (self.width // 2 - 120, 200), 
            font_size=18,
            text_color=(255, 255, 255),
            bg_color=(20, 20, 70),
            border_color=(100, 100, 200)
        )
        
        # Draw racial traits with proper line breaks
        race_info = RACES[self.race]
        trait_lines = []
        for trait in race_info["traits"]:
            trait_lines.append(f"• {trait}")
        traits_text = f"Racial Traits:\n" + "\n".join(trait_lines)
        
        self.graphics.draw_text_box(
            traits_text, 
            (self.width // 2 + 20, 220), 
            (self.width // 2 - 120, 200), 
            font_size=16,
            text_color=(255, 255, 255),
            bg_color=(20, 20, 70),
            border_color=(100, 100, 200)
        )
        
        # Draw confirmation prompt
        confirm_text = "Press Enter to create this character and begin your adventure!"
        self.graphics.draw_text_box(
            confirm_text, 
            (self.width // 4, 430), 
            (self.width // 2, 40), 
            font_size=18,
            text_color=(255, 255, 100),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        ) 