"""
Game engine for Riventide
"""

import os
import sys
import time
import asyncio
import pygame
from enum import Enum

from game.audio.audio_manager import AudioManager
from game.ui.graphics_manager import GraphicsManager
from game.ui.game_text import GameText
from game.utils.game_state import GameState
from game.world.world import World
from game.ui.character_creation_screen import CharacterCreationScreen, CreationStage

# ---------------------------------------------------------------------------
# Data-driven music and SFX assignments for every location
# ---------------------------------------------------------------------------

LOCATION_MUSIC = {
    # Eldoria
    "eldoria_introduction": "intro_music",
    "royal_court": "royal_court",
    "royal_court_segue_artifact": "royal_court",
    "royal_court_segue_rune": "royal_court",
    "royal_court_segue_alchemist": "royal_court",
    "eldoria_gate": "whisperwood",

    # Whisperwood
    "whisperwood_start": "whisperwood",
    "alien_tech_discovery": "alien_tech",
    "synthetic_clearing": "synthetic",
    "mushroom_path": "whisperwood",
    "faerie_vision": "faerie_realm",
    "bioengineered_creatures": "whisperwood",
    "tech_ambush_risk": "combat",
    "device_activation": "alien_tech",
    "tech_fragment_path": "alien_tech",
    "device_destruction_path": "alien_tech",
    "continue_journey_path": "whisperwood",
    "continue_to_faerie": "faerie",
    "combat_tech_soldiers": "death_music",
    "combat_tech_soldiers_weakened": "combat",
    "tech_soldiers_parley": "combat",
    "flee_ambush_attempt": "whisperwood",
    "ambush_negotiation_fail": "combat",
    "crystal_disruption_attempt": "combat",
    "rune_defense_attempt": "combat",
    "ambush_victory": "whisperwood",

    # Faerie Border
    "faerie_border": "faerie_realm",
    "faerie_realm_entrance": "faerie_realm",
    "faerie_scouts": "faerie_scouts",
    "faerie_escort": "faerie_scouts",
    "faerie_tech_reaction": "faerie_scouts",
    "faerie_invasion_reaction": "faerie_scouts",
    "faerie_city_approach": "faerie_scouts",

    # Faerie Realm Core
    "faerie_realm_entry": "faerie_realm",
    "test_of_loyalty": "crystal_grove",
    "drone_aftermath": "crystal_grove",
    "crash_site_retrieval": "crash_site",
    "heartstone_retrieval": "crash_site",
    "heartstone_secured": "crash_site",
    "crash_site_collapse": "crash_site",
    "crystal_interface": "knowledge_interface",
    "knowledge_repository": "knowledge_interface",
    "overloaded_connection": "knowledge_interface",
    "safe_disconnect": "knowledge_interface",
    "faerie_favor": "knowledge_interface",
    "faerie_alliance": "faerie_realm",
    "faerie_defense_preparations": "faerie_realm",

    # Grackle Encounters
    "grackle_encounter": "grackle_encounter",
    "grackle_deception": "grackle_encounter",
    "forest_escape": "grackle_encounter",
    "scout_ship_battle": "combat",
    "grackle_alliance_offer": "grackle_encounter",
    "grackle_tracking": "grackle_encounter",
    "data_core_escape": "grackle_encounter",
    "larger_vessel_threat": "death_music",
    "sensor_probe": "grackle_encounter",
    "faerie_rescue": "faerie_scouts",
    "map_escape": "combat",
    "void_transport": "captured_by_grackles",

    # Grackle Ship / Sneaking
    "grackle_ship_mission": "grackle_scout",
    "mission_preparation": "grackle_scout",
    "sneak_aboard": "grackle_scout",

    # Faerie Realm War
    "grackle_incursion": "combat",
    "vision_of_tanis": "alien_tech",
    "void_exile": "tragic",
    "spire_shielded": "combat",
    "warship_focus": "combat",
    "larger_grackle_force": "death_music",
    "outpost_destruction": "combat",
    "tanis_portal": "boss_battle",

    # Prison
    "captured_by_grackles": "captured_by_grackles",
    "vanlander_prison_capture": "vanlander_prison",
    "vent_escape": "vanlander_prison",
    "alarm_escape": "combat",
    "panel_escape": "vanlander_prison",
    "outer_pursuit": "combat",
    "delayed_escape": "vanlander_prison",
    "hidden_exit": "vanlander_prison",
    "lockdown": "combat",
    "alternate_route": "vanlander_prison",
    "power_core": "alien_tech",
    "maintenance_shaft": "vanlander_prison",
    "safe_exit": "vanlander_prison",
    "recapture": "defeat",

    # Void / Space
    "shuttle_chase": "combat",
    "void_survival": "tragic",
    "safe_haven_search": "tragic",
    "crash_landing": "crash_site",
    "cave_shelter": "tragic",
    "injured_retreat": "combat",
    "miracle_ship": "faerie_realm",
    "recovered_ally": "tragic",
    "crystal_signal": "faerie",

    # Confrontation & Endings
    "final_showdown": "boss_battle",
    "story_end": "tavern",
    "malgrim_showdown": "boss_battle",
    "magic_tavern": "tavern",
    "title_screen": "intro_music",

    # Route A -- Faerie Alliance path
    "faerie_war_council": "faerie_realm",
    "shadowlands_approach": "shadowlands",
    "malgrim_fortress_gate": "boss_battle",
    "malgrim_fortress_infiltration": "combat",
    "malgrim_throne_room": "boss_battle",
    "ending_heros_victory": "victory",

    # Route B -- Prison Break path
    "ending_pyrrhic_victory": "tragic",
    "ending_forgotten_prisoner": "defeat",

    # Route C -- Rogue Agent path
    "grackle_infiltrator": "grackle_scout",
    "grackle_sabotage": "alien_tech",
    "malgrim_audience": "boss_battle",
    "ending_double_agent": "synthetic",
}

LOCATION_SFX = {
    "whisperwood_start": ["forest_ambience"],
    "alien_tech_discovery": ["tech_hum"],
    "synthetic_clearing": ["static_whispers"],
    "faerie_realm_entry": ["faerie_chimes"],
    "faerie_realm_entrance": ["faerie_chimes"],
    "test_of_loyalty": ["holographic_arena"],
    "drone_aftermath": ["tech_hum"],
    "crash_site_retrieval": ["grackle_drone"],
    "heartstone_retrieval": ["heartstone_buzz"],
    "heartstone_secured": ["heartstone_buzz", "ship_scanning"],
    "knowledge_repository": ["data_transmission"],
    "overloaded_connection": ["crystal_overload"],
    "crystal_interface": ["crystal_resonance"],
    "grackle_encounter": ["scanner_beam"],
    "grackle_deception": ["alien_communication"],
    "scout_ship_battle": ["energy_weapon", "ship_weapons"],
    "grackle_incursion": ["grackle_alarm", "energy_weapon"],
    "captured_by_grackles": ["grackle_alarm"],
    "alarm_escape": ["grackle_alarm"],
    "shuttle_chase": ["ship_weapons"],
    "crash_landing": ["energy_weapon"],
    "miracle_ship": ["faerie_chimes", "tech_activation"],
    "tanis_portal": ["ship_scanning"],
    "final_showdown": ["energy_weapon"],
    "malgrim_showdown": ["energy_weapon", "tech_activation"],
    "malgrim_throne_room": ["energy_weapon", "tech_corruption"],
    "ending_heros_victory": ["faerie_chimes"],
    "ending_double_agent": ["alien_communication"],
    "grackle_sabotage": ["tech_corruption", "energy_weapon"],
    "malgrim_audience": ["tech_activation"],
    "malgrim_fortress_gate": ["energy_weapon"],
    "shadowlands_approach": ["static_whispers"],
}

# SFX that should be played as looping ambient sounds
LOOPING_SFX = {"forest_ambience"}

# Locations where forest ambience should play
WHISPERWOOD_AREAS = {
    "whisperwood_start", "eldoria_gate", "mushroom_path",
    "alien_tech_discovery", "synthetic_clearing", "tech_ambush_risk",
    "continue_to_faerie", "bioengineered_creatures", "faerie_vision",
    "device_activation", "tech_fragment_path", "device_destruction_path",
    "continue_journey_path", "flee_ambush_attempt", "ambush_victory",
    "combat_tech_soldiers", "combat_tech_soldiers_weakened",
    "tech_soldiers_parley", "ambush_negotiation_fail",
    "crystal_disruption_attempt", "rune_defense_attempt",
}

class GameMode(Enum):
    """Game modes."""
    MENU = "menu"
    CHARACTER_CREATION = "character_creation"
    EXPLORATION = "exploration"
    DIALOGUE = "dialogue"
    COMBAT = "combat"
    INVENTORY = "inventory"
    MAP = "map"
    CHARACTER = "character"
    QUEST = "quest"

class GameEngine:
    """Main game engine that integrates all components."""
    
    def __init__(self, width=800, height=600, text_only=False):
        """Initialize the game engine."""
        self.running = False
        self.text_only = text_only
        self.width = width
        self.height = height
        
        # Initialize components
        self.game_state = GameState()
        self.world = World()
        self.game_state.world = self.world
        
        # Initialize audio and graphics if not in text-only mode
        if not text_only:
            try:
                self.audio = AudioManager()
                self.graphics = GraphicsManager(width, height)
            except Exception as e:
                print(f"Error initializing audio or graphics: {e}")
                self.audio = None
                self.graphics = None
                self.text_only = True
        else:
            self.audio = None
            self.graphics = None
            
        # Game mode and state
        self.mode = GameMode.MENU
        self.current_text = ""
        self.current_options = []
        self.current_background = None
        
        # Menu state
        self.menu_options = ["New Game", "Gameplay", "Credits", "Exit"]
        self.selected_menu_option = 0
        
        # Exploration state
        self.selected_exploration_option = 0
        
        # Character creation screen
        self.character_creation = CharacterCreationScreen(self)
        
        # Event handlers
        self.event_handlers = {
            GameMode.MENU: self._handle_menu_events,
            GameMode.CHARACTER_CREATION: self._handle_character_creation_events,
            GameMode.EXPLORATION: self._handle_exploration_events,
            GameMode.DIALOGUE: self._handle_dialogue_events,
            GameMode.COMBAT: self._handle_combat_events,
            GameMode.INVENTORY: self._handle_inventory_events,
            GameMode.MAP: self._handle_map_events,
            GameMode.CHARACTER: self._handle_character_events,
            GameMode.QUEST: self._handle_quest_events
        }
        
        # Rendering functions
        self.render_functions = {
            GameMode.MENU: self._render_menu,
            GameMode.CHARACTER_CREATION: self._render_character_creation,
            GameMode.EXPLORATION: self._render_exploration,
            GameMode.DIALOGUE: self._render_dialogue,
            GameMode.COMBAT: self._render_combat,
            GameMode.INVENTORY: self._render_inventory,
            GameMode.MAP: self._render_map,
            GameMode.CHARACTER: self._render_character,
            GameMode.QUEST: self._render_quest
        }
        
        # Game clock for timing
        self.clock = pygame.time.Clock()
        self.dt = 0  # Delta time between frames
        
        # Text box visibility
        self.text_box_visible = True
        
    def start(self):
        """Start the game engine."""
        self.running = True
        
        # Play intro music
        if self.audio:
            self.audio.play_music("intro_music")
            
        # Main game loop
        if not self.text_only:
            self._graphical_game_loop()
        else:
            self._text_game_loop()
            
    def _graphical_game_loop(self):
        """Main game loop for graphical mode."""
        frame_count = 0
        last_mode = None
        
        print("Starting graphical game loop...")
        
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            frame_count += 1
            
            # Print debug info every 100 frames or when mode changes
            if frame_count % 100 == 0 or self.mode != last_mode:
                print(f"Frame: {frame_count}, Mode: {self.mode}")
                # Print custom screen status if in menu mode
                if self.mode == GameMode.MENU and hasattr(self, 'custom_screen_active'):
                    print(f"Custom screen active: {self.custom_screen_active}, Type: {getattr(self, 'custom_screen_type', 'None')}")
                last_mode = self.mode
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    if self.graphics:
                        self.graphics.handle_resize(event)
                else:
                    # Call the appropriate event handler based on game mode
                    handler = self.event_handlers.get(self.mode)
                    if handler:
                        handler(event)
                        
            # Update game state
            self._update(self.dt)
                        
            # Clear the screen
            self.graphics.clear()
            
            # Render the current mode
            render_func = self.render_functions.get(self.mode)
            if render_func:
                render_func()
            else:
                print(f"No render function for mode: {self.mode}")
                
            # Update the display
            self.graphics.update_display()
            
        # Clean up
        if self.audio:
            try:
                self.audio.cleanup()
            except Exception as e:
                print(f"Error cleaning up audio: {e}")
                
        if self.graphics:
            try:
                self.graphics.cleanup()
            except Exception as e:
                print(f"Error cleaning up graphics: {e}")
                
        print("Game engine cleaned up successfully")
            
    async def _graphical_game_loop_async(self):
        """Async twin of _graphical_game_loop for browser (pygbag) builds.

        Mirrors the sync loop frame-for-frame (same event handling, update,
        and render calls), but yields control back to the browser's event
        loop every frame via `await asyncio.sleep(0)`. Without that yield,
        pygbag's emscripten runtime never gets a chance to service audio,
        input, or repaint the canvas, and the tab appears frozen.

        The sync `_graphical_game_loop` above is left completely untouched
        so the desktop build's behavior cannot regress. Only the web
        entrypoint (web_main.py) should ever call this method.
        """
        frame_count = 0
        last_mode = None

        print("Starting async graphical game loop...")

        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(60) / 1000.0  # Convert to seconds
            frame_count += 1

            # Print debug info every 100 frames or when mode changes
            if frame_count % 100 == 0 or self.mode != last_mode:
                print(f"Frame: {frame_count}, Mode: {self.mode}")
                # Print custom screen status if in menu mode
                if self.mode == GameMode.MENU and hasattr(self, 'custom_screen_active'):
                    print(f"Custom screen active: {self.custom_screen_active}, Type: {getattr(self, 'custom_screen_type', 'None')}")
                last_mode = self.mode

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    # Handle window resize
                    if self.graphics:
                        self.graphics.handle_resize(event)
                else:
                    # Call the appropriate event handler based on game mode
                    handler = self.event_handlers.get(self.mode)
                    if handler:
                        handler(event)

            # Update game state
            self._update(self.dt)

            # Clear the screen
            self.graphics.clear()

            # Render the current mode
            render_func = self.render_functions.get(self.mode)
            if render_func:
                render_func()
            else:
                print(f"No render function for mode: {self.mode}")

            # Update the display
            self.graphics.update_display()

            # Yield to the browser's event loop. This is what keeps the tab
            # responsive (and lets pygbag pump audio/input) instead of
            # blocking the single JS thread emscripten runs on.
            await asyncio.sleep(0)

        # Clean up
        if self.audio:
            try:
                self.audio.cleanup()
            except Exception as e:
                print(f"Error cleaning up audio: {e}")

        if self.graphics:
            try:
                self.graphics.cleanup()
            except Exception as e:
                print(f"Error cleaning up graphics: {e}")

        print("Game engine cleaned up successfully")

    async def start_async(self):
        """Async entrypoint for browser (pygbag) builds.

        Mirrors start(), but always drives the async graphical loop and
        never falls through to _text_game_loop (which is full of blocking
        input() calls that would hang/crash in a browser). Desktop code
        (main.py) never calls this - it keeps using the sync start().
        """
        self.running = True

        # Play intro music
        if self.audio:
            self.audio.play_music("intro_music")

        # Web build must NEVER reach the text loop, regardless of text_only.
        await self._graphical_game_loop_async()

    def _text_game_loop(self):
        """Main game loop for text-only mode."""
        # In text-only mode, we delegate to the menu system
        from game.ui.menu import MainMenu
        menu = MainMenu(self.game_state)
        menu.display()
        
    def _update(self, dt):
        """Update game state based on the current mode."""
        if self.mode == GameMode.CHARACTER_CREATION:
            self.character_creation.update(dt)
        elif self.mode == GameMode.DIALOGUE:
            # Update dialogue animation timers
            if hasattr(self, 'quest_acceptance_time'):
                # Remove the automatic timeout
                pass
        elif self.mode == GameMode.EXPLORATION:
            # Update travel message timer (removed auto-dismiss)
            if hasattr(self, 'show_travel_message') and self.show_travel_message:
                if hasattr(self, 'travel_message_time'):
                    # Remove automatic dismissal
                    pass
        
    def _handle_menu_events(self, event):
        """Handle events in menu mode."""
        # Check if we're showing a custom screen
        if hasattr(self, 'custom_screen_active') and self.custom_screen_active:
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_ESCAPE):
                # Return to main menu
                self.custom_screen_active = False
                if self.audio:
                    self.audio.play_sound("menu_select")
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Move menu selection up
                self.selected_menu_option = (self.selected_menu_option - 1) % len(self.menu_options)
                if self.audio:
                    self.audio.play_sound("menu_select")
            elif event.key == pygame.K_DOWN:
                # Move menu selection down
                self.selected_menu_option = (self.selected_menu_option + 1) % len(self.menu_options)
                if self.audio:
                    self.audio.play_sound("menu_select")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._handle_menu_selection()
                
    def _handle_menu_selection(self):
        """Handle menu selection."""
        selected_option = self.menu_options[self.selected_menu_option]
        
        if self.audio:
            self.audio.play_sound("menu_select")
            
        print(f"Menu selection: {selected_option}")
            
        if selected_option == "New Game":
            # Start character creation
            self.mode = GameMode.CHARACTER_CREATION
            self.character_creation = CharacterCreationScreen(self)
            
            # Continue playing intro music during character creation
            if self.audio:
                self.audio.play_music("intro_music")
        elif selected_option == "Gameplay":
            # Show gameplay instruction screen
            self._show_gameplay_instructions()
            print("Gameplay instructions screen should now be active")
        elif selected_option == "Credits":
            # Show credits screen
            self._show_credits()
            print("Credits screen should now be active")
        elif selected_option == "Exit":
            self.running = False
        elif selected_option == "Resume Game":
            print("Resuming game...")
            self.mode = GameMode.EXPLORATION
        elif selected_option == "Quit to Title":
            print("Quitting to title...")
            self.reset_game_state()
            self.mode = GameMode.TITLE
            
    def _show_gameplay_instructions(self):
        """Show gameplay instructions screen."""
        # Create and display the gameplay instructions screen
        print("Showing gameplay instructions screen")
        
        # Set attributes properly
        self.custom_screen_active = True
        self.custom_screen_type = "gameplay"
        self.custom_screen_title = "Gameplay"
        
        # Make sure custom_screen_text is set with the right data type (list)
        self.custom_screen_text = [
            "Riventide is a choose-your-own-adventure story game.",
            "",
            "How to play:",
            "- Use the arrow keys (↑/↓) to navigate between choices",
            "- Press Enter to select your choice",
            "- Press Escape to exit the game",
            "",
            "Note: This game does not have save points. Each choice you make will",
            "permanently affect your journey through the story."
        ]
        
        print(f"Set custom screen content: {self.custom_screen_text}")
        
    def _show_credits(self):
        """Show credits screen."""
        # Create and display the credits screen
        print("Showing credits screen")
        
        # Set attributes properly
        self.custom_screen_active = True
        self.custom_screen_type = "credits"
        self.custom_screen_title = "Credits"
        
        # Make sure custom_screen_text is set with the right data type (list)
        self.custom_screen_text = [
            "Riventide",
            "An Epic Fantasy Adventure",
            "",
            "Written and designed by: Kevin Sotka, 2025",
            "",
            "Story elements drawn from the Tanis podcast,",
            "by Terry Miles and Nic Silver"
        ]
        
        print(f"Set custom screen content: {self.custom_screen_text}")
        
    def _handle_character_creation_events(self, event):
        """Handle events in character creation mode."""
        self.character_creation.handle_event(event)
            
    def _start_new_game(self):
        """Start a new game."""
        # Set up initial game state
        self.game_state.reset()
        
        # Set initial location to the starting location
        starting_location = self.world.get_starting_location()
        if starting_location:
            self.game_state.current_location = starting_location
            print(f"Starting location set to: {starting_location['name']}")
        else:
            print("Warning: Could not get starting location from world")
            # Create a default location
            default_location = {
                "id": "royal_court",
                "name": "The Royal Court of Eldoria",
                "description": "You stand before the golden throne of Eldoria, where King Alaric sits in crimson and gold robes.",
                "connections": []
            }
            self.game_state.current_location = default_location
            
        # Initialize dialogue state for the starting location
        self.current_dialogue_index = 0
        self.dialogue_complete = False
        self.selected_dialogue_choice = 0
        
        # Change mode to dialogue for the intro scene
        self.set_mode(GameMode.DIALOGUE)
        
        # Continue playing intro music during the introduction scene
        if self.audio:
            self.audio.play_music("intro_music")
            
        # Print debug info
        print("Starting new game...")
        print(f"Current mode: {self.mode}")
        print(f"Current location: {self.game_state.current_location}")
        
        # Set the starting storyline
        self.game_state.current_storyline = "royal_court"
        
    def _handle_exploration_events(self, event):
        """Handle events in exploration mode."""
        if event.type == pygame.KEYDOWN:
            # Toggle text box visibility
            if event.key == pygame.K_x:
                self.text_box_visible = not self.text_box_visible
                if self.audio:
                    self.audio.play_sound("menu_select")
                return
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_LEFT:
                # Go back to previous location
                prev_location = self.world.go_back()
                if prev_location:
                    self.game_state.current_location = prev_location
                    # Reset exploration state for the previous location
                    self.selected_exploration_option = 0
                    if self.audio:
                        self.audio.play_sound("back")
                else:
                    # If no previous location, switch to menu mode
                    self.mode = GameMode.MENU
                    self.menu_options = ["Resume Game", "Save Game", "Load Game", "Options", "Help", "Quit to Title", "Exit"]
                    self.selected_menu_option = 0
            elif event.key == pygame.K_UP:
                # Move selection up in location with multiple choices
                location = self.game_state.current_location
                
                if location["id"] == "eldoria_capital":
                    # Check max index based on whether quest is active
                    max_index = 3  # Default to 4 options
                    
                    # Check if "defend_the_realm" quest is active
                    quest_active = False
                    defend_quest = self.game_state.quest_manager.get_quest("defend_the_realm")
                    if defend_quest and defend_quest.active:
                        quest_active = True
                        max_index = 4  # 5 options when quest is active
                    
                    # Move selection up (wrap around)
                    if self.selected_exploration_option <= 0:
                        self.selected_exploration_option = max_index
                    else:
                        self.selected_exploration_option -= 1
                    
                    # Play selection sound
                    if self.audio:
                        self.audio.play_sound("menu_select")
            elif event.key == pygame.K_DOWN:
                # Move selection down in location with multiple choices
                location = self.game_state.current_location
                
                if location["id"] == "eldoria_capital":
                    # Check max index based on whether quest is active
                    max_index = 3  # Default to 4 options
                    
                    # Check if "defend_the_realm" quest is active
                    quest_active = False
                    defend_quest = self.game_state.quest_manager.get_quest("defend_the_realm")
                    if defend_quest and defend_quest.active:
                        quest_active = True
                        max_index = 4  # 5 options when quest is active
                    
                    # Move selection down (wrap around)
                    if self.selected_exploration_option >= max_index:
                        self.selected_exploration_option = 0
                    else:
                        self.selected_exploration_option += 1
                    
                    # Play selection sound
                    if self.audio:
                        self.audio.play_sound("menu_select")
            elif event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT:
                # Check if we're showing the background preview
                if hasattr(self, 'show_background_preview') and self.show_background_preview:
                    # Dismiss the background preview
                    self.show_background_preview = False
                    self.world.acknowledge_background_preview()
                    return
                
                # Handle selection for travel message
                if hasattr(self, 'show_travel_message') and self.show_travel_message:
                    # Dismiss travel message and set location to destination
                    self.show_travel_message = False
                    
                    # Using travel message to determine the destination location
                    if hasattr(self, 'travel_destination'):
                        if self.travel_destination == "whisperwood_forest":
                            self.set_current_location("whisperwood_start")
                            self.mode = GameMode.DIALOGUE
                            self.current_dialogue_index = 0
                            self.dialogue_complete = False
                            self.selected_dialogue_choice = 0
                    return
                
                # Handle location-specific selections
                location = self.game_state.current_location
                if location["id"] == "eldoria_capital":
                    # Check if player has accepted the quest
                    quest_active = False
                    defend_quest = self.game_state.quest_manager.get_quest("defend_the_realm")
                    if defend_quest and defend_quest.active:
                        quest_active = True
                    
                    # Process selection based on index
                    self.play_sound("click")
                    if self.selected_exploration_option == 0:
                        print("Visiting the Royal Court...")
                        self.transition_to_royal_court()
                    elif self.selected_exploration_option == 1:
                        print("Exploring the Markets...")
                        # Will implement market exploration later
                    elif self.selected_exploration_option == 2:
                        print("Training with the Knights...")
                        # Will implement knight training later
                    elif self.selected_exploration_option == 3:
                        print("Investigating the Spires...")
                        # Will implement spire investigation later
                    elif quest_active and self.selected_exploration_option == 4:
                        print("Traveling to Whisperwood Forest...")
                        self.transition_to_whisperwood_forest()
            
            # Mode switching keys - ESC key removed
            if event.key == pygame.K_i:
                self.mode = GameMode.INVENTORY
            elif event.key == pygame.K_m:
                self.mode = GameMode.MAP
            elif event.key == pygame.K_c:
                self.mode = GameMode.CHARACTER
            elif event.key == pygame.K_q:
                self.mode = GameMode.QUEST
            
            # Handle location-specific navigation in Eldoria's capital
            if self.game_state.current_location["id"] == "eldoria_capital":
                # Check if player has accepted the quest
                quest_active = False
                defend_quest = self.game_state.quest_manager.get_quest("defend_the_realm")
                if defend_quest and defend_quest.active:
                    quest_active = True
                    max_option = 4  # 5 options when quest is active
                else:
                    max_option = 3  # 4 options normally
                
                if event.key == pygame.K_UP:
                    # Move selection up, with wraparound to bottom if at top
                    if self.selected_exploration_option == 0 and quest_active:
                        # Wrap to Whisperwood Forest option if at top
                        self.selected_exploration_option = max_option
                    else:
                        self.selected_exploration_option = max(0, self.selected_exploration_option - 1)
                    if self.audio:
                        self.audio.play_sound("menu_select")
                elif event.key == pygame.K_DOWN:
                    # Move selection down, with wraparound to top if at bottom
                    if self.selected_exploration_option == max_option:
                        # Wrap to first option if at bottom
                        self.selected_exploration_option = 0
                    else:
                        self.selected_exploration_option = min(max_option, self.selected_exploration_option + 1)
                    if self.audio:
                        self.audio.play_sound("menu_select")
                elif event.key == pygame.K_RETURN:
                    # Handle selection
                    self.play_sound("click")
                    if self.selected_exploration_option == 0:
                        print("Visiting the Royal Court...")
                        self.transition_to_royal_court()
                    elif self.selected_exploration_option == 1:
                        print("Exploring the Markets...")
                        # Will implement market exploration later
                    elif self.selected_exploration_option == 2:
                        print("Training with the Knights...")
                        # Will implement knight training later
                    elif self.selected_exploration_option == 3:
                        print("Investigating the Spires...")
                        # Will implement spire investigation later
                    elif quest_active and self.selected_exploration_option == 4:
                        print("Traveling to Whisperwood Forest...")
                        self.transition_to_whisperwood_forest()
                        
    def transition_to_royal_court(self):
        """Transition to the Royal Court location."""
        # Set the current location to Royal Court
        self.set_current_location("royal_court")
        
        # Initialize dialogue state for the royal court scene
        self.current_dialogue_index = 0
        self.dialogue_complete = False
        
        # Set mode to dialogue
        self.set_mode(GameMode.DIALOGUE)
        
        # Initialize choices for after dialogue
        self.dialogue_choices = [
            "Accept the quest to defend the realm",
            "Request more information",
            "Politely decline",
            "Return to the capital"
        ]
        self.selected_dialogue_choice = 0
                        
    def available_choices(self, location):
        """Return the choices in `location` the player can currently take.

        A choice may carry "modifier_required": <name>. Such a choice is only
        offered once the player has picked up that modifier earlier in the
        story (see GameState.player_modifiers / set_modifier). Choices with no
        "modifier_required" are always available.

        This is the single source of truth for which choices exist: rendering,
        up/down navigation bounds, and selection all go through it, so the
        index held in self.selected_dialogue_choice always refers to the same
        list the player is looking at.

        Fails open: if gating would leave the player with nothing to pick, the
        full unfiltered list is returned rather than soft-locking the run.
        """
        choices = location.get("choices") or []
        modifiers = getattr(self.game_state, "player_modifiers", {}) or {}

        available = [
            c for c in choices
            if not c.get("modifier_required")
            or modifiers.get(c["modifier_required"], False)
        ]
        return available if available else choices

    def _handle_dialogue_events(self, event):
        """Handle events in dialogue mode."""
        if event.type == pygame.KEYDOWN:
            # Toggle text box visibility
            if event.key == pygame.K_x:
                self.text_box_visible = not self.text_box_visible
                if self.audio:
                    self.audio.play_sound("menu_select")
                return
            if event.key == pygame.K_RETURN or event.key == pygame.K_RIGHT:
                # Check if we're showing the background preview
                if hasattr(self, 'show_background_preview') and self.show_background_preview:
                    # Dismiss the background preview
                    self.show_background_preview = False
                    self.world.acknowledge_background_preview()
                    return
                
                # Check if dialogue is complete but we have choices
                location = self.game_state.current_location
                if not hasattr(self, 'current_dialogue_index') or self.current_dialogue_index >= len(location.get("dialogue", [])):
                    # Dialogue complete, handle choice selection
                    if "choices" in location:
                        choices = self.available_choices(location)
                        # Guard against a stale index if the list shrank.
                        if self.selected_dialogue_choice >= len(choices):
                            self.selected_dialogue_choice = 0
                        selected_choice = choices[self.selected_dialogue_choice]
                        
                        # Use the new transition method to handle the choice
                        if "destination" in selected_choice:
                            destination = selected_choice["destination"]
                            modifier = selected_choice.get("modifier")
                            self.transition_to_location(destination, modifier)
                        else:
                            # Return to exploration if no destination specified
                            self.mode = GameMode.EXPLORATION
                        
                        # Play sound
                        if self.audio:
                            self.audio.play_sound("click")
                    elif hasattr(self, 'dialogue_choices'):
                        # Legacy dialogue choice handling
                        if self.selected_dialogue_choice == 0:
                            # Accept quest
                            print("Quest accepted: Defend the Realm")
                            # Add quest to player's quest log
                            if self.game_state.add_quest("defend_the_realm"):
                                # Show brief confirmation message
                                self.quest_accepted = True
                                self.quest_acceptance_time = 0
                                if self.audio:
                                    self.audio.play_sound("quest_accepted")
                            else:
                                print("Failed to add quest")
                            # Return to capital after a short delay
                            self.mode = GameMode.DIALOGUE
                        elif self.selected_dialogue_choice == 1:
                            # Request more information
                            print("Requesting more information about the quest")
                            # Show additional dialogue
                            self.show_additional_information = True
                            self.selected_dialogue_choice = 0  # Reset selection for the new choices
                        elif self.selected_dialogue_choice == 2:
                            # Decline quest
                            print("Quest declined")
                            self.mode = GameMode.EXPLORATION
                            self.set_current_location("eldoria_capital")
                        elif self.selected_dialogue_choice == 3:
                            # Return to capital
                            self.mode = GameMode.EXPLORATION
                            self.set_current_location("eldoria_capital")
                    else:
                        # No choices, go back to exploration
                        self.mode = GameMode.EXPLORATION
                else:
                    # Advance dialogue
                    self.current_dialogue_index += 1
                    if self.current_dialogue_index >= len(location["dialogue"]):
                        self.dialogue_complete = True
                    if self.audio:
                        self.audio.play_sound("dialogue_advance")
            
            elif event.key == pygame.K_LEFT or event.key == pygame.K_ESCAPE:
                # Go back to previous screen
                location = self.game_state.current_location
                
                # If we're in the middle of dialogue, go back to the previous dialogue line
                if hasattr(self, 'current_dialogue_index') and self.current_dialogue_index > 0 and self.current_dialogue_index < len(location.get("dialogue", [])):
                    self.current_dialogue_index -= 1
                    if self.audio:
                        self.audio.play_sound("dialogue_advance")
                # If dialogue is complete and we're showing choices, go back to the last dialogue line
                elif self.dialogue_complete and "dialogue" in location and len(location["dialogue"]) > 0:
                    self.current_dialogue_index = len(location["dialogue"]) - 1
                    self.dialogue_complete = False
                    if self.audio:
                        self.audio.play_sound("dialogue_advance")
                # Otherwise, go back to previous location
                else:
                    prev_location = self.world.go_back()
                    if prev_location:
                        self.game_state.current_location = prev_location
                        
                        # Check if previous location had dialogue and set it to show choices
                        if "dialogue" in prev_location:
                            # Skip to the choice selection screen by setting the dialogue as complete
                            self.current_dialogue_index = len(prev_location["dialogue"])
                            self.dialogue_complete = True
                            self.selected_dialogue_choice = 0
                        else:
                            # Reset dialogue state for non-dialogue locations
                            self.current_dialogue_index = 0
                            self.dialogue_complete = False
                            self.selected_dialogue_choice = 0
                        
                        if self.audio:
                            self.audio.play_sound("back")
                    else:
                        # If no previous location, go to exploration mode
                        self.mode = GameMode.EXPLORATION
                        if self.audio:
                            self.audio.play_sound("back")
            
            elif event.key == pygame.K_UP:
                # Move choice selection up
                location = self.game_state.current_location
                
                if not hasattr(self, 'current_dialogue_index') or self.current_dialogue_index >= len(location.get("dialogue", [])):
                    # Dialogue complete, navigate choices
                    if "choices" in location:
                        max_choice = len(self.available_choices(location)) - 1
                        self.selected_dialogue_choice = max(0, self.selected_dialogue_choice - 1)
                        if self.audio:
                            self.audio.play_sound("menu_select")
                    elif hasattr(self, 'dialogue_choices') and self.dialogue_complete:
                        # Legacy dialogue choices
                        self.selected_dialogue_choice = max(0, self.selected_dialogue_choice - 1)
                        if self.audio:
                            self.audio.play_sound("menu_select")
                            
            elif event.key == pygame.K_DOWN:
                # Move choice selection down
                location = self.game_state.current_location
                
                if not hasattr(self, 'current_dialogue_index') or self.current_dialogue_index >= len(location.get("dialogue", [])):
                    # Dialogue complete, navigate choices
                    if "choices" in location:
                        max_choice = len(self.available_choices(location)) - 1
                        self.selected_dialogue_choice = min(max_choice, self.selected_dialogue_choice + 1)
                        if self.audio:
                            self.audio.play_sound("menu_select")
                    elif hasattr(self, 'dialogue_choices') and self.dialogue_complete:
                        # Legacy dialogue choices
                        max_choice = len(self.dialogue_choices) - 1
                        self.selected_dialogue_choice = min(max_choice, self.selected_dialogue_choice + 1)
                        if self.audio:
                            self.audio.play_sound("menu_select")
                
    def _handle_combat_events(self, event):
        """Handle events in combat mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                # TODO: Try to flee combat
                pass
                
    def _handle_inventory_events(self, event):
        """Handle events in inventory mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = GameMode.EXPLORATION
                
    def _handle_map_events(self, event):
        """Handle events in map mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = GameMode.EXPLORATION
                
    def _handle_character_events(self, event):
        """Handle events in character mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = GameMode.EXPLORATION
                
    def _handle_quest_events(self, event):
        """Handle events in quest mode."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.mode = GameMode.EXPLORATION
                
    def _render_menu(self):
        """Render the menu screen."""
        # Check if we're showing a custom screen
        if hasattr(self, 'custom_screen_active') and self.custom_screen_active:
            self._render_custom_screen()
            return
            
        # Draw background
        if self.current_background:
            self.graphics.draw_background(self.current_background)
        else:
            # Default background
            self.graphics.clear((0, 0, 50))  # Dark blue background
            
        # Draw title
        title_text = "RIVENTIDE"
        subtitle_text = "An Epic Fantasy Adventure"
        
        # Draw title and subtitle as a text box
        self.graphics.draw_text_box(
            title_text, 
            (self.width // 4, 100), 
            (self.width // 2, 80), 
            font_size=72, 
            text_color=(255, 255, 100),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        self.graphics.draw_text_box(
            subtitle_text, 
            (self.width // 4, 180), 
            (self.width // 2, 50), 
            font_size=36, 
            text_color=(200, 200, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
            
        # Draw menu options
        for i, option in enumerate(self.menu_options):
            option_y = 300 + i * 50
            
            # Determine colors based on selection
            if i == self.selected_menu_option:
                text_color = (255, 255, 100)  # Yellow for selected option
                bg_color = (50, 50, 100)      # Lighter blue background
                border_color = (200, 200, 100)  # Yellow border
            else:
                text_color = (255, 255, 255)  # White for unselected options
                bg_color = (0, 0, 50)         # Dark blue background
                border_color = (0, 0, 50)     # No visible border
            
            self.graphics.draw_text_box(
                option, 
                (self.width // 3, option_y), 
                (self.width // 3, 40), 
                font_size=30,
                text_color=text_color,
                bg_color=bg_color,
                border_color=border_color
            )
            
    def _render_custom_screen(self):
        """Render a custom screen (gameplay or credits)."""
        # Draw background
        self.graphics.clear((0, 0, 50))  # Dark blue background
        
        # Debug prints
        print(f"Rendering custom screen: {self.custom_screen_type}")
        print(f"Title: {self.custom_screen_title}")
        print(f"Text content: {self.custom_screen_text}")
        
        # Draw title
        self.graphics.draw_text_box(
            self.custom_screen_title, 
            (self.width // 4, 80), 
            (self.width // 2, 60), 
            font_size=48, 
            text_color=(255, 255, 100),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
        # Draw text content with increased height per line
        text_y = 160
        line_height = 40  # Increased from 30 to ensure enough space
        
        for i, line in enumerate(self.custom_screen_text):
            if not line:  # If empty line, just add spacing
                text_y += line_height // 2  # Half spacing for empty lines
                continue
                
            print(f"Drawing line: '{line}' at y={text_y}")
            # Increased height for text boxes to ensure text fits
            self.graphics.draw_text_box(
                line, 
                (self.width // 6, text_y), 
                (self.width * 2 // 3, line_height), 
                font_size=20,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 50),
                border_color=(0, 0, 50)
            )
            text_y += line_height
        
        # Draw prompt to return
        self.graphics.draw_text_box(
            "Press Enter to return to the main menu", 
            (self.width // 4, self.height - 80), 
            (self.width // 2, 40), 
            font_size=20,
            text_color=(200, 200, 255),
            bg_color=(0, 0, 50),
            border_color=(0, 0, 50)
        )
        
    def _render_character_creation(self):
        """Render the character creation screen."""
        self.character_creation.render()
        
    def _render_exploration(self):
        """Render the exploration screen."""
        # Handle travel message if active
        if hasattr(self, 'show_travel_message') and self.show_travel_message:
            # Draw the travel background instead of a black background
            if hasattr(self, 'travel_destination') and self.travel_destination == "whisperwood_forest":
                self.graphics.draw_background("whisperwood_path")
            else:
                # Use a black background as fallback for other destinations
                self.graphics.clear((0, 0, 0))
            
            # Draw the travel message
            self.graphics.draw_text_box(
                self.travel_message,
                (self.width // 6, self.height // 2 - 50),
                (self.width * 2 // 3, 100),
                font_size=20,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
            
            # Draw prompt with clearer instructions
            self.graphics.draw_text_box(
                "Press Enter to arrive at your destination",
                (self.width // 4, self.height * 3 // 4),
                (self.width // 2, 30),
                font_size=16,
                text_color=(255, 255, 100),  # Yellow to make it more noticeable
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 200)  # Blue border to match UI style
            )
            
            return
        
        # Get current location
        location = self.game_state.current_location
        if not location:
            print("Warning: No current location set in _render_exploration")
            # Create a default location
            location = {
                "id": "unknown",
                "name": "Unknown Location",
                "description": "You find yourself in an unfamiliar place.",
                "connections": []
            }
            self.game_state.current_location = location
            
        # Draw background for the current location
        if "background" in location and location["background"]:
            self.graphics.draw_background(location["background"])
        else:
            # Check if we know the region for region-based backgrounds
            current_region = None
            for r_id, region in self.world.regions.items():
                for loc_id, loc in region["locations"].items():
                    if loc_id == location["id"]:
                        current_region = r_id
                        break
                if current_region:
                    break
                    
            if current_region:
                # Draw the background for this region
                self.graphics.draw_background(current_region)
            else:
                # Default background if region not found
                print(f"Region not found for location {location['id']}, using default background")
                self.graphics.clear((0, 0, 0))
        
        # Check if text boxes are hidden
        if not self.text_box_visible:
            # Draw only the background and a small overlay for the toggle hint
            overlay_text = "X = text on/off"
            font_size = 18
            padding = 10
            overlay_width = 160
            overlay_height = 32
            x = self.width - overlay_width - padding
            y = self.height - overlay_height - padding
            self.graphics.draw_text_box(
                overlay_text,
                (x, y),
                (overlay_width, overlay_height),
                font_size=font_size,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
            return
        
        # Check if we should show only the background with "press enter to continue"
        if hasattr(self, 'show_background_preview') and self.show_background_preview:
            # Draw only the prompt to continue - no text boxes
            self.graphics.draw_text_box(
                "Press Enter to continue",
                (self.width // 4, self.height * 3 // 4),
                (self.width // 2, 40),
                font_size=20,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
            return  # Skip rendering the rest of the location
        
        # Draw location description
        self.graphics.draw_text_box(
            location["description"],
            (50, 50),  # Moved up from 80
            (self.width - 100, 120),  # Slightly smaller height
            font_size=24,
            bg_color=(0, 0, 0, 180),
            border_color=(100, 100, 100)
        )
        
        # Draw available actions based on current location
        if location["id"] == "eldoria_capital":
            # Check if player has accepted the "defend_the_realm" quest
            quest_active = False
            defend_quest = self.game_state.quest_manager.get_quest("defend_the_realm")
            if defend_quest and defend_quest.active:
                quest_active = True
            
            actions = [
                ["Visit the Royal Court", "Seek an audience with the king in the grand throne room atop the castle's highest spire."],
                ["Explore the Markets", "Wander through the bustling markets, where merchants hawk wares beneath the spires."],
                ["Train with the Knights", "Join the knights in their training yard, where steel clashes beneath the royal banner."],
                ["Investigate the Spires", "Climb the shadowed stairways of the towering spires, rumored to hide ancient secrets."]
            ]
            
            # If quest is active, add a fifth option to go to Whisperwood Forest
            # (only if not already in the actions list)
            if quest_active and not any("Travel to Whisperwood Forest" in action for action in actions):
                actions.append(["Travel to Whisperwood Forest", "Follow the eastern road to the mysterious forest where Lord Malgrim's spies are rumored to hide."])
            
            # Spacing for options
            option_spacing = 90
            option_start_y = 200  # Moved up from 250
            
            for i, (action, description) in enumerate(actions):
                # Calculate y position for this option
                y_pos = option_start_y + i * option_spacing
                
                # Determine if this option is selected
                is_selected = (i == self.selected_exploration_option)
                
                # Set colors based on selection
                if is_selected:
                    text_color = (255, 255, 100)  # Yellow for selected option
                    bg_color = (50, 50, 100, 220)  # Lighter blue background
                    border_color = (200, 200, 100)  # Yellow border
                    desc_text_color = (220, 220, 150)  # Lighter yellow for description
                    desc_bg_color = (30, 30, 80, 200)  # Slightly different background for description
                else:
                    text_color = (255, 255, 255)  # White for unselected options
                    bg_color = (0, 0, 50, 220)  # Dark blue background
                    border_color = (100, 100, 200)  # Blue border
                    desc_text_color = (200, 200, 200)  # Light gray for description
                    desc_bg_color = (10, 10, 60, 200)  # Slightly different background for description
                
                # Draw action button
                self.graphics.draw_text_box(
                    action,
                    (50, y_pos),  # Back to left-justified position
                    (300, 40),
                    font_size=22,
                    text_color=text_color,
                    bg_color=bg_color,
                    border_color=border_color
                )
                
                # Draw description below the action
                self.graphics.draw_text_box(
                    description,
                    (50, y_pos + 40),  # Back to left-justified position
                    (700, 40),  # Increased height for description
                    font_size=16,
                    text_color=desc_text_color,
                    bg_color=desc_bg_color,
                    border_color=(0, 0, 50)
                )
                
        else:
            # Generic actions for other locations
            actions = ["Look around", "Talk to someone", "Check inventory", "Open map", "Return to menu"]
            for i, action in enumerate(actions):
                self.graphics.draw_text_box(
                    action,
                    (50, 250 + i * 40),
                    (200, 30),
                    font_size=20,
                    bg_color=(0, 0, 50),
                    border_color=(100, 100, 200)
                )
        
    def _format_dialogue_text(self, text):
        """
        Format dialogue text by replacing placeholders with actual values.
        
        Args:
            text (str): The text to format
            
        Returns:
            str: The formatted text
        """
        if not text:
            return ""
            
        # Replace player name placeholder
        if self.game_state.player and self.game_state.player.name:
            text = text.replace("{player_name}", self.game_state.player.name)
        else:
            text = text.replace("{player_name}", "Adventurer")
            
        return text
        
    def _render_dialogue(self):
        """Render the dialogue screen."""
        location = self.game_state.current_location
        
        # Draw background for dialogue screen
        if "background" in location and location["background"]:
            self.graphics.draw_background(location["background"])
        else:
            # Default background if specific one not found
            self.graphics.draw_background("eldoria")
        
        # Check if text boxes are hidden
        if not self.text_box_visible:
            overlay_text = "X = text on/off"
            font_size = 18
            padding = 10
            overlay_width = 160
            overlay_height = 32
            x = self.width - overlay_width - padding
            y = self.height - overlay_height - padding
            self.graphics.draw_text_box(
                overlay_text,
                (x, y),
                (overlay_width, overlay_height),
                font_size=font_size,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
            return
        
        # Check if we should show only the background with "press enter to continue"
        if hasattr(self, 'show_background_preview') and self.show_background_preview:
            # Draw only the prompt to continue - no text boxes
            self.graphics.draw_text_box(
                "Press Enter to continue",
                (self.width // 4, self.height * 3 // 4),
                (self.width // 2, 40),
                font_size=20,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
            return  # Skip rendering the rest of the dialogue

        # --- Always show the scene description at the top ---
        if "modifiers" in location and hasattr(self.game_state, 'player_modifiers'):
            # Build a modified description with relevant modifier text
            modified_description = self._format_dialogue_text(location["description"])
            for modifier, text in location["modifiers"].items():
                if self.game_state.has_modifier(modifier):
                    modified_description += f"\n\n{self._format_dialogue_text(text)}"
            self.graphics.draw_text_box(
                modified_description,
                (50, 20),
                (self.width - 100, 180),
                font_size=18,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
        else:
            self.graphics.draw_text_box(
                self._format_dialogue_text(location["description"]),
                (50, 20),
                (self.width - 100, 180),
                font_size=18,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 180),
                border_color=(100, 100, 100)
            )
        # --- End description box ---

        # Check if we have dialogue to display
        if "dialogue" in location and location["dialogue"]:
            dialogue = location["dialogue"]
            
            # Render the current dialogue line
            if hasattr(self, 'current_dialogue_index') and self.current_dialogue_index < len(dialogue):
                current_line = dialogue[self.current_dialogue_index]
                
                # Draw speaker name if not "Narration"
                if current_line["speaker"] != "Narration":
                    self.graphics.draw_text_box(
                        current_line["speaker"] + ":",
                        (50, 210),
                        (self.width - 100, 40),
                        font_size=24,
                        text_color=(255, 255, 100),
                        bg_color=(0, 0, 0, 200),
                        border_color=(100, 100, 100)
                    )
                
                # Draw dialogue text with different positioning based on whether it's narration
                y_pos = 260 if current_line["speaker"] != "Narration" else 210
                height = 150 if current_line["speaker"] != "Narration" else 200
                
                # Format the dialogue text to replace placeholders
                formatted_text = self._format_dialogue_text(current_line["text"])
                
                self.graphics.draw_text_box(
                    formatted_text,
                    (50, y_pos),
                    (self.width - 100, height),
                    font_size=20,
                    text_color=(255, 255, 255),
                    bg_color=(0, 0, 0, 200),
                    border_color=(100, 100, 100)
                )
                
                # Draw prompt to continue
                self.graphics.draw_text_box(
                    "Press Enter to continue" if not self.dialogue_complete else "Choose your response:",
                    (self.width // 4, self.height - 100),
                    (self.width // 2, 40),
                    font_size=20,
                    text_color=(200, 200, 200),
                    bg_color=(0, 0, 0, 180),
                    border_color=(100, 100, 100)
                )
            else:
                # Dialogue complete, show choices
                if "choices" in location:
                    # Draw choices prompt - MOVED UP
                    prompt_y = 210 # Moved up from 240
                    self.graphics.draw_text_box(
                        "What will you do?",
                        (50, prompt_y),
                        (self.width - 100, 40),
                        font_size=24,
                        text_color=(255, 255, 100),
                        bg_color=(0, 0, 0, 200),
                        border_color=(100, 100, 100)
                    )
                    
                    # Draw choices with more space - MOVED UP
                    choices = self.available_choices(location)
                    choice_start_y = prompt_y + 50 # Start choices below the prompt
                    choice_height = 35 # Height for choice text
                    desc_height = 40 # Height for choice description
                    choice_spacing = choice_height + desc_height + 10 # Total space per choice

                    for i, choice in enumerate(choices):
                        y_pos = choice_start_y + i * choice_spacing
                        
                        # Determine if this choice is selected
                        is_selected = (i == self.selected_dialogue_choice)
                        
                        # Set colors based on selection
                        if is_selected:
                            text_color = (255, 255, 100)  # Yellow for selected option
                            bg_color = (50, 50, 100, 220)  # Lighter blue background
                            border_color = (200, 200, 100)  # Yellow border
                            desc_color = (220, 220, 150)  # Lighter yellow for description
                        else:
                            text_color = (255, 255, 255)  # White for unselected options
                            bg_color = (0, 0, 50, 220)  # Dark blue background
                            border_color = (100, 100, 200)  # Blue border
                            desc_color = (200, 200, 200)  # Light gray for description
                        
                        # Draw choice title
                        self.graphics.draw_text_box(
                            self._format_dialogue_text(choice["text"]),
                            (70, y_pos),
                            (self.width - 140, choice_height), # Adjusted height
                            font_size=18,
                            text_color=text_color,
                            bg_color=bg_color,
                            border_color=border_color
                        )
                        
                        # Draw choice description underneath
                        if "description" in choice:
                            self.graphics.draw_text_box(
                                self._format_dialogue_text(choice["description"]),
                                (90, y_pos + choice_height + 5), # Position below choice text
                                (self.width - 180, desc_height), # Adjusted height
                                font_size=16,
                                text_color=desc_color,
                                bg_color=(10, 10, 30, 180), # Slightly different background
                                border_color=(0, 0, 0, 0) # No border for description
                            )
                elif self.dialogue_complete and hasattr(self, 'dialogue_choices'):
                    # Legacy dialogue choice system
                    for i, choice in enumerate(self.dialogue_choices):
                        y_pos = self.height - 250 + i * 45
                        
                        # Determine if this choice is selected
                        is_selected = (i == self.selected_dialogue_choice)
                        
                        # Set colors based on selection
                        if is_selected:
                            text_color = (255, 255, 100)  # Yellow for selected option
                            bg_color = (50, 50, 100, 220)  # Lighter blue background
                            border_color = (200, 200, 100)  # Yellow border
                        else:
                            text_color = (255, 255, 255)  # White for unselected options
                            bg_color = (0, 0, 50, 220)  # Dark blue background
                            border_color = (100, 100, 200)  # Blue border
                        
                        # Draw choice
                        self.graphics.draw_text_box(
                            choice,
                            (70, y_pos),
                            (self.width - 140, 40),
                            font_size=18,
                            text_color=text_color,
                            bg_color=bg_color,
                            border_color=border_color
                        )
                else:
                    # No current dialogue or dialogue completed
                    self.graphics.draw_text_box(
                        "The conversation has ended.",
                        (self.width // 4, self.height // 2),
                        (self.width // 2, 50),
                        font_size=24,
                        text_color=(255, 255, 255),
                        bg_color=(0, 0, 0, 200),
                        border_color=(100, 100, 100)
                    )
        else:
            # No dialogue found for location
            self.graphics.draw_text_box(
                "There is no one to talk to here.",
                (self.width // 4, self.height // 2),
                (self.width // 2, 50),
                font_size=24,
                text_color=(255, 255, 255),
                bg_color=(0, 0, 0, 200),
                border_color=(100, 100, 100)
            )
        
    def _render_combat(self):
        """Render the combat screen."""
        # TODO: Implement combat rendering
        pass
        
    def _render_inventory(self):
        """Render the inventory screen."""
        # TODO: Implement inventory rendering
        pass
        
    def _render_map(self):
        """Render the map screen."""
        # Clear background
        self.graphics.clear((0, 0, 0))
        
        # Draw map title
        title_text = self.graphics.render_text("World Map", 36, (255, 255, 255))
        if title_text:
            title_x = (self.width - title_text.get_width()) // 2
            self.graphics.screen.blit(title_text, (title_x, 20))
            
        # Draw the world map
        self.graphics.draw_map("world", 50, 70, self.width - 100, self.height - 150)
        
        # Draw player location
        if self.game_state.current_location:
            # TODO: Calculate player position on map based on current location
            player_pos = (0.5, 0.5)  # Default to center for now
            
    def _render_character(self):
        """Render the character screen."""
        # TODO: Implement character screen rendering
        pass
        
    def _render_quest(self):
        """Render the quest screen."""
        # TODO: Implement quest screen rendering
        pass
        
    def set_mode(self, mode):
        """Set the game mode."""
        print(f"Setting game mode from {self.mode} to {mode}")
        self.mode = mode
        
        # Play appropriate music for the mode
        if self.audio:
            if mode == GameMode.COMBAT:
                self.audio.play_music("combat")
            elif mode == GameMode.EXPLORATION and self.game_state.current_location:
                # Get the region for the current location
                region_id = None
                for r_id, region in self.world.regions.items():
                    for loc_id in region["locations"]:
                        if loc_id == self.game_state.current_location["id"]:
                            region_id = r_id
                            break
                    if region_id:
                        break
                        
                # Special case: if we're in Whisperwood area, preserve the Whisperwood music
                is_whisperwood_area = (region_id == "whisperwood" or 
                                     self.game_state.current_location["id"].startswith("whisperwood") or
                                     self.game_state.current_location["id"] in ["eldoria_gate", "mushroom_path", 
                                                                          "alien_tech_discovery", "synthetic_clearing", 
                                                                          "tech_ambush_risk"])
                
                if region_id and not is_whisperwood_area:
                    print(f"Playing music for region: {region_id}")
                    self.audio.play_music(region_id)
                elif is_whisperwood_area:
                    print("Preserving Whisperwood music in Whisperwood area")
                    self.audio.play_music("whisperwood")
                    
    def play_sound(self, sound_effect):
        """Play a sound effect."""
        if self.audio:
            self.audio.play_sound(sound_effect)
            
    def set_current_location(self, location_id):
        """
        Set the current location.
        
        Args:
            location_id (str): The ID of the location to set as current.
        """
        print(f"Setting current location to: {location_id}")
        
        # Try to get the location from the world
        location = self.world.get_location(location_id)
        
        if location:
            print(f"Found location: {location['name']}")
            self.game_state.current_location = location
            
            # Determine the region for this location
            region_id = None
            for r_id, region in self.world.regions.items():
                if location_id in region["locations"]:
                    region_id = r_id
                    break
                    
            if region_id:
                self.current_background = f"background_{region_id}"
                
                # Play region music
                if self.audio:
                    self.audio.play_music(region_id)
                    
                print(f"Set current location to {location_id} in {region_id}")
                return
            else:
                print(f"Warning: Could not determine region for location {location_id}")
        else:
            print(f"Warning: Location {location_id} not found in any region")
        
        # Create a default location if not found
        default_location = {
            "id": location_id,
            "name": "Unknown Location",
            "description": "You find yourself in an unfamiliar place.",
            "connections": []
        }
        self.game_state.current_location = default_location
        self.current_background = "background_eldoria"  # Default background
        
    def toggle_music(self):
        """Toggle music on/off."""
        if self.audio:
            self.audio.toggle_music()
            
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        if self.audio:
            self.audio.toggle_sound()
            
    def toggle_graphics(self):
        """Toggle graphics on/off."""
        if self.graphics:
            self.graphics.toggle_graphics()
            
    def cleanup(self):
        """Clean up resources."""
        if self.audio:
            try:
                self.audio.cleanup()
            except Exception as e:
                print(f"Error cleaning up audio: {e}")
                
        if self.graphics:
            try:
                self.graphics.cleanup()
            except Exception as e:
                print(f"Error cleaning up graphics: {e}")
                
        print("Game engine cleaned up successfully")
        
    def transition_to_whisperwood_forest(self):
        """Transition to the Whisperwood Forest location."""
        # Set the current location to Whisperwood Forest
        self.set_current_location("whisperwood_forest")
        
        # Reset selected option for the new location
        self.selected_exploration_option = 0
        
        # Play transition music and sound
        if self.audio:
            self.audio.play_music("whisperwood")
            # Stop any existing forest ambience to prevent overlapping
            self.audio.stop_sound("forest_ambience")
            # Play forest ambience sound in a loop for continuous ambient effect
            self.audio.play_looping_sound("forest_ambience")
        
        # Show brief travel message
        self.show_travel_message = True
        self.travel_message_time = 0
        self.travel_destination = "whisperwood_forest"  # Set destination for background selection
        self.travel_message = "You travel east from Eldoria, following the winding road until it disappears into the mysterious Whisperwood Forest. The trees loom overhead, their branches creating a canopy that blocks much of the sunlight."
        # Play forest ambience sound for the whisperwood start location
        if self.audio:
            # Stop any existing forest ambience to prevent overlapping (just in case)
            self.audio.stop_sound("forest_ambience")
            # Play forest ambience sound in a loop for continuous ambient effect
            self.audio.play_looping_sound("forest_ambience")

    def _handle_title_events(self, event):
        """Handle events in title mode."""
        if event.type == pygame.KEYDOWN:
            # ESC key removed - player can only use title menu options
            if event.key == pygame.K_UP:
                self.selected_title_option = (self.selected_title_option - 1) % len(self.title_options)
                if self.audio:
                    self.audio.play_sound("menu_select")
            elif event.key == pygame.K_DOWN:
                self.selected_title_option = (self.selected_title_option + 1) % len(self.title_options)
                if self.audio:
                    self.audio.play_sound("menu_select")
            elif event.key == pygame.K_RETURN:
                self.play_sound("click")
                if self.title_options[self.selected_title_option] == "New Game":
                    # Route through character creation (same as the main menu's
                    # "New Game") rather than calling _start_new_game() directly.
                    # That direct call used to skip character creation entirely,
                    # so a "Quit to Title" -> "New Game" replay would start with
                    # no player object and no race/class modifiers set at all.
                    self.mode = GameMode.CHARACTER_CREATION
                    self.character_creation = CharacterCreationScreen(self)
                    if self.audio:
                        self.audio.play_music("intro_music")
                elif self.title_options[self.selected_title_option] == "Load Game":
                    print("Loading game...")
                    # Implement load game
                elif self.title_options[self.selected_title_option] == "Options":
                    print("Opening options...")
                    # Implement options
                elif self.title_options[self.selected_title_option] == "Exit":
                    self.running = False 

    def transition_to_location(self, location_id, modifier=None):
        """
        Transition to a new story location.
        
        Args:
            location_id (str): The ID of the location to transition to
            modifier (str, optional): A modifier to apply to the player
        """
        print(f"Transitioning to location: {location_id}")
        
        # Set any modifier provided
        if modifier and hasattr(self.game_state, 'set_modifier'):
            self.game_state.set_modifier(modifier)
            print(f"Applied modifier: {modifier}")
        
        # Navigate to the new location using World's navigate_to_location method
        # (which will track background changes)
        location = self.world.navigate_to_location(location_id)
        
        # Check if the location exists
        if not location:
            print(f"ERROR: Location {location_id} not found. Creating fallback location.")
            # Create a fallback location
            location = {
                "id": location_id,
                "name": "Unknown Location",
                "description": "This area is still being discovered. The scene is not yet fully implemented.",
                "dialogue": [
                    {
                        "speaker": "Narration",
                        "text": "This path is still being uncovered. You decide to turn back for now."
                    }
                ],
                "choices": [
                    {
                        "text": "Return to previous location",
                        "description": "You turn back to where you came from.",
                        "destination": self._prev_location_id or "eldoria_introduction"
                    }
                ],
                "background": self.game_state.current_location.get("background", "eldoria") if self.game_state.current_location else "eldoria"
            }
        
        # Set the current location in game state
        self.game_state.current_location = location
        
        # Play appropriate music and SFX for the location
        if self.audio:
            # Priority: location's own music field > LOCATION_MUSIC dict > fallback
            music_field = location.get("music")
            if music_field:
                self.audio.play_music(music_field)
            elif location_id in LOCATION_MUSIC:
                self.audio.play_music(LOCATION_MUSIC[location_id])
            else:
                self.audio.play_music("main_theme")

            # Play SFX for the location
            if location_id in LOCATION_SFX:
                for sfx in LOCATION_SFX[location_id]:
                    if sfx in LOOPING_SFX:
                        self.audio.stop_sound(sfx)
                        self.audio.play_looping_sound(sfx)
                    else:
                        self.audio.play_sound(sfx)

            # Stop forest ambience when leaving Whisperwood areas
            if location_id not in WHISPERWOOD_AREAS:
                self.audio.stop_sound("forest_ambience")
        
        # Store current location for next transition
        self._prev_location_id = location_id
        
        # Flag to indicate background preview is needed
        self.show_background_preview = self.world.should_preview_background()
        
        # If the location has dialogue, set up for dialogue mode
        if "dialogue" in self.game_state.current_location:
            self.current_dialogue_index = 0
            self.dialogue_complete = False
            self.selected_dialogue_choice = 0
            self.set_mode(GameMode.DIALOGUE)
        else:
            # Otherwise, set to exploration mode
            self.set_mode(GameMode.EXPLORATION)
            self.selected_exploration_option = 0
        
        # Update storyline tracking
        if hasattr(self.game_state, 'advance_storyline'):
            self.game_state.advance_storyline(location_id)
        
        # Play appropriate sound effect if available
        if location_id == "whisperwood_start":
            self.show_travel_message = True
            self.travel_message = "You journey from the royal court through the gates of Eldoria and east to the mysterious Whisperwood. The forest's edge looms before you, silver-barked trees reflecting strange glimmers of light, unlike any natural woodland you've seen."
            self.travel_destination = "whisperwood_start" 
            # Play forest ambience sound for the whisperwood start location
            if self.audio:
                # Stop any existing forest ambience to prevent overlapping
                self.audio.stop_sound("forest_ambience")
                # Play forest ambience sound in a loop for continuous ambient effect
                self.audio.play_looping_sound("forest_ambience") 