"""
Graphics management for Riventide
"""

import os
import pygame
from enum import Enum
import math

class GraphicsType(Enum):
    """Types of graphics in the game."""
    BACKGROUND = "background"
    CHARACTER = "character"
    ENEMY = "enemy"
    ITEM = "item"
    ICON = "icon"
    MAP = "map"
    ANIMATION = "animation"
    VIDEO = "video"  # New type for video backgrounds

class GraphicsManager:
    """Manages graphics for the game."""
    
    def __init__(self, width=800, height=600):
        """Initialize the graphics manager."""
        self.initialized = False
        self.graphics_enabled = True
        self.width = width
        self.height = height
        self.screen = None
        self.clock = None
        self.fps = 30
        
        # Video backgrounds
        self.video_backgrounds = {}
        self.current_video = None
        self.video_frame = None
        self.video_clock = 0
        
        # Asset paths
        self.asset_paths = {
            # Backgrounds for each region
            "background_eldoria": "assets/graphics/backgrounds/eldoria.png",
            "background_drakkar": "assets/graphics/backgrounds/drakkar.png",
            "background_faerie": "assets/graphics/backgrounds/faerie.png",
            "background_barbarian": "assets/graphics/backgrounds/barbarian.png",
            "background_shadowlands": "assets/graphics/backgrounds/shadowlands.png",
            "background_whisperwood": "assets/graphics/backgrounds/whisperwood.png",
            "background_whisperwood_forest": "assets/graphics/backgrounds/whisperwood.png",
            "background_whisperwood_clearing": "assets/graphics/backgrounds/whisperwood.png",
            "background_whisperwood_path": "assets/graphics/backgrounds/whisperwood_path.png",
            "background_royal_court": "assets/graphics/backgrounds/royal_court.png",
            "background_eldoria_gate": "assets/graphics/backgrounds/eldoria_gate.png",
            
            # New backgrounds for the sci-fi fantasy storyline
            "background_whisperwood_start": "assets/graphics/backgrounds/whisperwood_start.png",
            "background_alien_tech": "assets/graphics/backgrounds/alien_tech.png",
            "background_synthetic_clearing": "assets/graphics/backgrounds/synthetic_clearing.png",
            "background_mushroom_path": "assets/graphics/backgrounds/mushroom_path.png",
            "background_tech_ambush": "assets/graphics/backgrounds/tech_ambush.png",
            "background_faerie_border": "assets/graphics/backgrounds/faerie_border.png",
            "background_faerie_scouts": "assets/graphics/backgrounds/faerie_scouts.png",
            "background_faerie_path": "assets/graphics/backgrounds/faerie_path.png",
            "background_faerie_realm_entry": "assets/graphics/backgrounds/faerie_realm_entry.png",
            "background_faerie_realm": "assets/graphics/backgrounds/faerie_realm.png",
            "background_crystal_grove": "assets/graphics/backgrounds/crystal_grove.png",
            "background_knowledge_repository": "assets/graphics/backgrounds/knowledge_repository.png",
            "background_twilight_marshes": "assets/graphics/backgrounds/twilight_marshes.png",
            "background_grackle_scout": "assets/graphics/backgrounds/grackle_scout.png",

            # Additional backgrounds for story scenes
            "background_test_of_loyalty": "assets/graphics/backgrounds/test_of_loyalty.png",
            "background_crash_site": "assets/graphics/backgrounds/crash_site.png",
            "background_grackle_battle": "assets/graphics/backgrounds/grackle_battle.png",
            "background_faerie_vision": "assets/graphics/backgrounds/faerie_vision.png",
            "background_bioengineered_creatures": "assets/graphics/backgrounds/bioengineered_creatures.png",
            "background_captured_by_grackles": "assets/graphics/backgrounds/captured_by_grackles.png",
            "background_vanlander_prison": "assets/graphics/backgrounds/vanlander_prison.png",
            "background_prison_vents": "assets/graphics/backgrounds/prison_vents.png",
            "background_prison_alarm": "assets/graphics/backgrounds/prison_alarm.png",
            "background_prison_tunnel": "assets/graphics/backgrounds/prison_tunnel.png",
            "background_prison_yard": "assets/graphics/backgrounds/prison_yard.png",
            "background_hidden_passage": "assets/graphics/backgrounds/hidden_passage.png",
            "background_prison_lockdown": "assets/graphics/backgrounds/prison_lockdown.png",
            "background_maintenance_corridor": "assets/graphics/backgrounds/maintenance_corridor.png",
            "background_power_core": "assets/graphics/backgrounds/power_core.png",
            "background_space_pursuit": "assets/graphics/backgrounds/space_pursuit.png",
            "background_maintenance_shaft": "assets/graphics/backgrounds/maintenance_shaft.png",
            "background_void_starscape": "assets/graphics/backgrounds/void_starscape.png",
            "background_prison_exterior": "assets/graphics/backgrounds/prison_exterior.png",
            "background_crash_site_asteroid": "assets/graphics/backgrounds/crash_site_asteroid.png",
            "background_magic_tavern": "assets/graphics/backgrounds/magic_tavern.png",
            "background_tavern_interior": "assets/graphics/backgrounds/tavern_interior.png",
            "background_whisperwood_death": "assets/graphics/backgrounds/whisperwood_death.png",
            "background_void_exile": "assets/graphics/backgrounds/void_exile.png",
            "background_faerie_realm_entrance": "assets/graphics/backgrounds/faerie_realm_entrance.png",
            
            # Video backgrounds
            "background_video_bioengineered_creatures": "assets/graphics/videos/bioengineered_creatures.mp4",
            
            # Character portraits
            "portrait_warrior": "assets/graphics/characters/warrior.png",
            "portrait_mage": "assets/graphics/characters/mage.png",
            "portrait_rogue": "assets/graphics/characters/rogue.png",
            "portrait_healer": "assets/graphics/characters/healer.png",
            "portrait_archer": "assets/graphics/characters/archer.png",
            
            # Companion portraits
            "portrait_sir_gareth": "assets/graphics/characters/sir_gareth.png",
            "portrait_luna": "assets/graphics/characters/luna.png",
            "portrait_krag": "assets/graphics/characters/krag.png",
            "portrait_sera": "assets/graphics/characters/sera.png",
            
            # Enemy sprites
            "enemy_goblin": "assets/graphics/enemies/goblin.png",
            "enemy_orc": "assets/graphics/enemies/orc.png",
            "enemy_troll": "assets/graphics/enemies/troll.png",
            "enemy_skeleton": "assets/graphics/enemies/skeleton.png",
            "enemy_dragon": "assets/graphics/enemies/dragon.png",
            "enemy_shadow_beast": "assets/graphics/enemies/shadow_beast.png",
            
            # Item icons
            "item_sword": "assets/graphics/items/sword.png",
            "item_staff": "assets/graphics/items/staff.png",
            "item_bow": "assets/graphics/items/bow.png",
            "item_potion": "assets/graphics/items/potion.png",
            "item_scroll": "assets/graphics/items/scroll.png",
            "item_artifact": "assets/graphics/items/artifact.png",
            
            # UI icons
            "icon_health": "assets/graphics/icons/health.png",
            "icon_mana": "assets/graphics/icons/mana.png",
            "icon_experience": "assets/graphics/icons/experience.png",
            "icon_gold": "assets/graphics/icons/gold.png",
            "icon_inventory": "assets/graphics/icons/inventory.png",
            "icon_quest": "assets/graphics/icons/quest.png",
            "icon_combat": "assets/graphics/icons/combat.png",
            "icon_dice": "assets/graphics/icons/dice.png",
            
            # Maps
            "map_world": "assets/graphics/maps/world_map.png",
            "map_eldoria": "assets/graphics/maps/eldoria_map.png",
            "map_drakkar": "assets/graphics/maps/drakkar_map.png",
            "map_faerie": "assets/graphics/maps/faerie_map.png",
            "map_barbarian": "assets/graphics/maps/barbarian_map.png",
            "map_shadowlands": "assets/graphics/maps/shadowlands_map.png",
            
            # Animations
            "anim_sword_slash": "assets/graphics/animations/sword_slash.png",
            "anim_magic_cast": "assets/graphics/animations/magic_cast.png",
            "anim_arrow_shot": "assets/graphics/animations/arrow_shot.png",
            "anim_heal": "assets/graphics/animations/heal.png",
            "anim_level_up": "assets/graphics/animations/level_up.png",
            "background_tanis_portal": "assets/graphics/backgrounds/tanis_portal.png",
            "background_grackle_battle": "assets/graphics/backgrounds/grackle_battle.png",
            "background_faerie_realm": "assets/graphics/backgrounds/faerie_realm.png",
            "background_asteroid_cave": "assets/graphics/backgrounds/asteroid_cave.png",
            "background_prison_yard": "assets/graphics/backgrounds/prison_yard.png",
            "background_grackle_alliance_offer": "assets/graphics/backgrounds/grackle_alliance_offer.png",
            "background_corrupted_outpost": "assets/graphics/backgrounds/corrupted_outpost.png",
            "background_map_escape": "assets/graphics/backgrounds/map_escape.png",
            "background_grackle_incursion": "assets/graphics/backgrounds/grackle_incursion.png",
            "background_grackle_ship": "assets/graphics/backgrounds/grackle_ship.png",
            "background_mission_preparation": "assets/graphics/backgrounds/mission_preparation.png",
            "background_sneak_aboard": "assets/graphics/backgrounds/sneak_aboard.png",
        }
        
        # Asset cache
        self.asset_cache = {}
        
        # Region to background mapping
        self.region_backgrounds = {
            "eldoria": "background_eldoria",
            "drakkar": "background_drakkar",
            "faerie": "background_faerie",
            "barbarian": "background_barbarian",
            "shadowlands": "background_shadowlands",
            "whisperwood": "background_whisperwood",
            "whisperwood_forest": "background_whisperwood_forest",
            "whisperwood_clearing": "background_whisperwood_clearing",
            "royal_court": "background_royal_court",
            "whisperwood_start": "background_whisperwood_start",
            "alien_tech_discovery": "background_alien_tech",
            "synthetic_clearing": "background_synthetic_clearing",
            "mushroom_path": "background_mushroom_path",
            "tech_ambush_risk": "background_tech_ambush",
            "tech_soldiers_parley": "background_whisperwood_death",
            "combat_tech_soldiers": "background_whisperwood_death",
            "bioengineered_creatures": "background_bioengineered_creatures",
            "eldoria_gate": "background_eldoria_gate",
            "faerie_border": "background_faerie_border",
            "faerie_scouts": "background_faerie_scouts",
            "faerie_path": "background_faerie_path",
            "faerie_realm_entry": "background_faerie_realm_entry",
            "faerie_realm": "background_faerie_realm",
            "crystal_grove": "background_crystal_grove",
            "knowledge_repository": "background_knowledge_repository",
            "twilight_marshes": "background_twilight_marshes",
            "faerie_vision": "background_faerie_vision",
            "grackle_scout_encounter": "background_grackle_scout",
            "test_of_loyalty": "background_test_of_loyalty",
            "crash_site_retrieval": "background_crash_site",
            "heartstone_retrieval": "background_crash_site",
            "grackle_encounter": "background_grackle_scout",
            "grackle_deception": "background_grackle_scout",
            "scout_ship_battle": "background_grackle_battle",
            "captured_by_grackles": "background_captured_by_grackles",
            "vanlander_prison_capture": "background_vanlander_prison",
            "vent_escape": "background_prison_vents",
            "alarm_escape": "background_prison_alarm",
            "panel_escape": "background_prison_tunnel",
            "outer_pursuit": "background_prison_yard",
            "delayed_escape": "background_prison_vents",
            "hidden_exit": "background_hidden_passage",
            "lockdown": "background_prison_lockdown",
            "alternate_route": "background_maintenance_corridor",
            "power_core": "background_power_core",
            "shuttle_chase": "background_space_pursuit",
            "maintenance_shaft": "background_maintenance_shaft",
            "void_survival": "background_void_starscape",
            "safe_exit": "background_prison_exterior",
            "crash_landing": "background_crash_site_asteroid",
            "final_showdown": "background_magic_tavern",
            "story_end": "background_tavern_interior",
            "forest_escape": "background_whisperwood_path",
            "heartstone_secured": "background_crash_site",
            "crash_site_collapse": "background_faerie_realm",
            "whisperwood_death": "background_whisperwood_death",
            "grackle_incursion": "background_grackle_incursion",
            "vision_of_tanis": "background_tanis_portal",
            "void_exile": "background_void_exile",
            "spire_shielded": "background_faerie_realm",
            "warship_focus": "background_grackle_battle",
            "cave_shelter": "background_asteroid_cave",
            "injured_retreat": "background_prison_yard",
            "bioengineered_creatures": "background_bioengineered_creatures",
            "faerie_realm_entrance": "background_faerie_realm_entrance",
            "grackle_alliance_offer": "background_grackle_alliance_offer",
            "corrupted_outpost": "background_corrupted_outpost",
            "map_escape": "background_map_escape",
            "grackle_ship_mission": "background_grackle_ship",
            "mission_preparation": "background_mission_preparation",
            "sneak_aboard": "background_sneak_aboard",
        }
        
        # Class to portrait mapping
        self.class_portraits = {
            "warrior": "portrait_warrior",
            "mage": "portrait_mage",
            "rogue": "portrait_rogue",
            "healer": "portrait_healer",
            "archer": "portrait_archer",
            "sir_gareth": "portrait_sir_gareth",
            "luna": "portrait_luna",
            "krag": "portrait_krag",
            "sera": "portrait_sera"
        }
        
        # Enemy mapping
        self.enemy_sprites = {
            "goblin": "enemy_goblin",
            "orc": "enemy_orc",
            "troll": "enemy_troll",
            "skeleton": "enemy_skeleton",
            "dragon": "enemy_dragon",
            "shadow_beast": "enemy_shadow_beast"
        }
        
        # Icon mapping
        self.icons = {
            "health": "icon_health",
            "mana": "icon_mana",
            "experience": "icon_experience",
            "gold": "icon_gold",
            "inventory": "icon_inventory",
            "quest": "icon_quest",
            "combat": "icon_combat",
            "dice": "icon_dice"
        }
        
        # Animation mapping
        self.animations = {
            "sword_slash": "anim_sword_slash",
            "magic_cast": "anim_magic_cast",
            "arrow_shot": "anim_arrow_shot",
            "heal": "anim_heal",
            "level_up": "anim_level_up"
        }
        
        # Initialize pygame
        self._initialize()
        
    def _initialize(self):
        """Initialize pygame and create the game window."""
        try:
            pygame.init()
            pygame.display.set_caption("Riventide")
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            self.clock = pygame.time.Clock()
            
            # Explicitly initialize the font module
            if not pygame.font.get_init():
                pygame.font.init()
                print("Initialized pygame font module")
                
            self.initialized = True
            
            # Create directories if they don't exist
            os.makedirs("assets/graphics/backgrounds", exist_ok=True)
            os.makedirs("assets/graphics/characters", exist_ok=True)
            os.makedirs("assets/graphics/enemies", exist_ok=True)
            os.makedirs("assets/graphics/items", exist_ok=True)
            os.makedirs("assets/graphics/icons", exist_ok=True)
            os.makedirs("assets/graphics/maps", exist_ok=True)
            os.makedirs("assets/graphics/animations", exist_ok=True)
            
            # Load default assets
            self._load_default_assets()
            
            # Verify font initialization
            if pygame.font.get_init():
                print("Font module is initialized")
                fonts = pygame.font.get_fonts()
                print(f"Available system fonts: {fonts[:5]}... (showing first 5 of {len(fonts)})")
            else:
                print("WARNING: Font module is NOT initialized")
            
        except Exception as e:
            print(f"Failed to initialize graphics: {e}")
            self.initialized = False
            self.graphics_enabled = False
            
    def _load_default_assets(self):
        """Load default assets that are always needed."""
        # Load some essential assets into cache
        for key in ["map_world", "icon_health", "icon_mana", "icon_experience"]:
            self._load_asset(key)
            
    def _load_asset(self, asset_key):
        """
        Load an asset into the cache.
        
        Args:
            asset_key (str): The key of the asset to load.
            
        Returns:
            pygame.Surface: The loaded asset, or None if loading failed.
        """
        if asset_key in self.asset_cache:
            return self.asset_cache[asset_key]
            
        path = self.asset_paths.get(asset_key)
        if not path:
            print(f"Asset path not found for key: {asset_key}")
            return self._create_placeholder_surface(64, 64)
            
        # Check if this is a video background
        if asset_key.startswith("background_video_"):
            return self._load_video_background(asset_key, path)
            
        try:
            if os.path.exists(path):
                asset = pygame.image.load(path).convert_alpha()
                self.asset_cache[asset_key] = asset
                return asset
            else:
                print(f"Asset file not found: {path}")
                return self._create_placeholder_surface(64, 64)
        except Exception as e:
            print(f"Error loading asset {path}: {e}")
            return self._create_placeholder_surface(64, 64)
            
    def _load_video_background(self, asset_key, path):
        """
        Load a video background.
        
        Args:
            asset_key (str): The key of the video asset.
            path (str): Path to the video file.
            
        Returns:
            pygame.Surface: A placeholder surface for the video.
        """
        try:
            # Check if OpenCV is available
            import cv2
            print(f"Loading video background: {path}")
            
            # Create a placeholder surface for now
            placeholder = self._create_placeholder_surface(self.width, self.height, (50, 0, 50))
            font = pygame.font.SysFont(None, 36)
            text = font.render("VIDEO BACKGROUND", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.width//2, self.height//2))
            placeholder.blit(text, text_rect)
            
            # Cache this placeholder - we'll replace with actual video frames when playing
            self.asset_cache[asset_key] = placeholder
            
            # For now, we'll simulate a video by creating a simple animation
            # This will be replaced with actual video loading in a real implementation
            frames = []
            for i in range(10):
                frame = placeholder.copy()
                pulse_val = 128 + int(127 * abs(math.sin(i * 0.2)))
                frame.fill((pulse_val, 30, pulse_val), special_flags=pygame.BLEND_MULT)
                frames.append(frame)
            
            # Store the frames for this video
            self.video_backgrounds[asset_key] = frames
            
            return placeholder
            
        except ImportError:
            print("OpenCV (cv2) not installed. Using placeholder for video background.")
            placeholder = self._create_placeholder_surface(self.width, self.height, (150, 0, 150))
            self.asset_cache[asset_key] = placeholder
            return placeholder
        except Exception as e:
            print(f"Error loading video background {path}: {e}")
            placeholder = self._create_placeholder_surface(self.width, self.height, (150, 0, 150))
            self.asset_cache[asset_key] = placeholder
            return placeholder
            
    def _create_placeholder_surface(self, width, height, color=(128, 128, 128)):
        """Create a placeholder surface when an asset can't be loaded."""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill(color)
        # Draw an X to indicate it's a placeholder
        pygame.draw.line(surface, (255, 0, 0), (0, 0), (width, height), 2)
        pygame.draw.line(surface, (255, 0, 0), (0, height), (width, 0), 2)
        return surface
            
    def get_asset(self, asset_key):
        """
        Get an asset from the cache, loading it if necessary.
        
        Args:
            asset_key (str): The key of the asset to get.
            
        Returns:
            pygame.Surface: The asset, or None if not found.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        asset = self.asset_cache.get(asset_key)
        if asset:
            return asset
            
        return self._load_asset(asset_key)
        
    def get_background_for_region(self, region_id):
        """
        Get the background image for a region.
        
        Args:
            region_id (str): The ID of the region.
            
        Returns:
            pygame.Surface: The background image, or None if not found.
        """
        background_key = self.region_backgrounds.get(region_id)
        if background_key:
            return self.get_asset(background_key)
        return None
        
    def get_portrait_for_class(self, class_name):
        """
        Get the portrait for a character class.
        
        Args:
            class_name (str): The name of the class.
            
        Returns:
            pygame.Surface: The portrait, or None if not found.
        """
        portrait_key = self.class_portraits.get(class_name)
        if portrait_key:
            return self.get_asset(portrait_key)
        return None
        
    def get_map(self, map_key):
        """
        Get a map image.
        
        Args:
            map_key (str): The key of the map to get.
            
        Returns:
            pygame.Surface: The map image, or None if not found.
        """
        return self.get_asset(f"map_{map_key}")
        
    def render_text(self, text, font_size=20, color=(255, 255, 255), font_name=None):
        """
        Render text to a surface.
        
        Args:
            text (str): The text to render.
            font_size (int): The font size.
            color (tuple): RGB color tuple.
            font_name (str): Name of the font to use, or None for default.
            
        Returns:
            pygame.Surface: The rendered text.
        """
        if not self.initialized:
            print("Cannot render text: Graphics not initialized")
            return None
            
        if not pygame.font.get_init():
            print("Font module not initialized, attempting to initialize now")
            pygame.font.init()
            
        try:
            # Ensure we have a valid text value
            if text is None:
                text = "None"
            elif not isinstance(text, str):
                text = str(text)
                
            print(f"Rendering text: '{text}' with font_size={font_size}")
            
            # Create font object safely
            try:
                if font_name:
                    font = pygame.font.Font(font_name, font_size)
                else:
                    # Try specific built-in fonts first
                    try:
                        font = pygame.font.SysFont("arial", font_size)
                    except:
                        # Fall back to default font
                        font = pygame.font.SysFont(None, font_size)
            except Exception as e:
                print(f"Error creating font: {e}, falling back to default")
                font = pygame.font.SysFont(None, font_size)
                
            # Render the text
            rendered_text = font.render(text, True, color)
            return rendered_text
            
        except Exception as e:
            print(f"Error rendering text '{text}': {e}")
            # Create a placeholder surface as a last resort
            surface = pygame.Surface((len(text) * font_size // 2, font_size), pygame.SRCALPHA)
            surface.fill((100, 100, 100, 128))
            return surface
            
    def draw_text_box(self, text, pos, size, font_size=20, text_color=(255, 255, 255), 
                     bg_color=(0, 0, 0), border_color=(100, 100, 100), padding=10):
        """
        Draw a text box with wrapped text.
        
        Args:
            text (str): The text to display.
            pos (tuple): (x, y) position of the top-left corner.
            size (tuple): (width, height) of the box.
            font_size (int): Size of the font.
            text_color (tuple): RGB color for the text.
            bg_color (tuple): RGB or RGBA color for the background.
            border_color (tuple): RGB color for the border.
            padding (int): Padding inside the box.
            
        Returns:
            pygame.Rect: The rectangle of the text box.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        x, y = pos
        width, height = size
        
        # Debug print
        print(f"Drawing text box: '{text}' at position {pos}, size {size}")
        
        # Create the box
        box_rect = pygame.Rect(x, y, width, height)
        
        # Handle RGBA background color
        if len(bg_color) == 4:
            # Create a surface with per-pixel alpha
            bg_surface = pygame.Surface((width, height), pygame.SRCALPHA)
            bg_surface.fill(bg_color)
            self.screen.blit(bg_surface, (x, y))
        else:
            pygame.draw.rect(self.screen, bg_color, box_rect)
            
        pygame.draw.rect(self.screen, border_color, box_rect, 2)
        
        # Check if text is empty
        if not text:
            print("Text is empty, returning early")
            return box_rect
        
        # Create a safe font - use render_text which has better error handling
        font = pygame.font.SysFont(None, font_size)
        line_height = max(font.get_height(), 20)  # Ensure minimum line height
        
        # Split text into lines first (respect explicit line breaks)
        lines = []
        for line in text.split('\n'):
            if not line:  # Handle empty lines
                lines.append('')
                continue
                
            words = line.split(' ')
            space_width = font.size(' ')[0]
            max_width = width - (padding * 2)
            current_line = []
            current_width = 0
            
            for word in words:
                word_surface = font.render(word, True, text_color)
                word_width = word_surface.get_width()
                
                if current_width + word_width <= max_width:
                    current_line.append(word)
                    current_width += word_width + space_width
                else:
                    lines.append(' '.join(current_line))
                    current_line = [word]
                    current_width = word_width + space_width
                    
            if current_line:
                lines.append(' '.join(current_line))
        
        # Debug print
        print(f"Wrapped into {len(lines)} lines: {lines}")
        
        # To ensure text is visible, make sure line_height gives enough space
        available_height = height - (padding * 2)
        max_lines = max(1, available_height // line_height)
        
        # Render each line
        for i, line in enumerate(lines):
            # Stop if we've reached the maximum number of lines that can fit
            if i >= max_lines:
                # Draw ellipsis to indicate more text
                if i < len(lines):
                    ellipsis_surf = font.render("...", True, text_color)
                    self.screen.blit(ellipsis_surf, (x + padding, y + height - padding - line_height))
                break
                
            if line:  # Skip rendering empty lines, but still advance position
                try:
                    line_surface = font.render(line, True, text_color)
                    line_y = y + padding + (i * line_height)
                    self.screen.blit(line_surface, (x + padding, line_y))
                    print(f"Rendered line {i}: '{line}' at y={line_y}")
                except Exception as e:
                    print(f"Error rendering line '{line}': {e}")
            
        return box_rect
            
    def draw_character_portrait(self, character_key, pos, width=64, height=64):
        """
        Draw a character portrait.
        
        Args:
            character_key (str): The key of the character.
            pos (tuple): (x, y) position to draw at.
            width (int): Width to draw the portrait.
            height (int): Height to draw the portrait.
            
        Returns:
            pygame.Rect: The rectangle of the portrait.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        # Try to get the portrait from the class mapping
        portrait_key = self.class_portraits.get(character_key.lower())
        if not portrait_key:
            # If not found in mapping, try direct key
            portrait_key = f"portrait_{character_key.lower()}"
            
        portrait = self.get_asset(portrait_key)
        if not portrait:
            # If still not found, create a placeholder
            portrait = self._create_placeholder_surface(width, height, (150, 150, 150))
            
        # Scale and draw the portrait
        portrait = pygame.transform.scale(portrait, (width, height))
        self.screen.blit(portrait, pos)
        return pygame.Rect(pos[0], pos[1], width, height)
            
    def draw_background(self, background_key):
        """
        Draw a background image.
        
        Args:
            background_key (str): The key of the background.
            
        Returns:
            pygame.Rect: The rectangle of the background.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
        
        # Initialize the tracking variables if they don't exist
        if not hasattr(self, '_last_rendered_frame'):
            self._last_rendered_frame = 0
        if not hasattr(self, '_last_background_key'):
            self._last_background_key = None
        if not hasattr(self, 'background_warning_shown'):
            self.background_warning_shown = set()
        if not hasattr(self, 'missing_asset_warnings'):
            self.missing_asset_warnings = set()
            
        # Get the current frame count
        current_frame = pygame.time.get_ticks() // 33  # About 30fps
        
        # Only log when the background changes (not just every frame)
        is_new_frame = current_frame > self._last_rendered_frame
        is_new_background = background_key != self._last_background_key
        
        if is_new_background:
            print(f"Drawing new background: {background_key}")
            self._last_background_key = background_key
            
        self._last_rendered_frame = current_frame
        
        # Try to get the background from the region mapping
        background_asset_key = self.region_backgrounds.get(background_key)
        if not background_asset_key:
            # If not found in mapping, try direct key
            background_asset_key = f"background_{background_key}"
            if background_key not in self.background_warning_shown and is_new_background:
                self.background_warning_shown.add(background_key)
                print(f"Background mapping not found for {background_key}, trying: {background_asset_key}")
        
        # Check if this is a video background
        if background_asset_key.startswith("background_video_"):
            return self._draw_video_background(background_asset_key)
            
        background = self.get_asset(background_asset_key)
        if not background:
            # If still not found, create a placeholder
            if background_asset_key not in self.missing_asset_warnings and is_new_background:
                self.missing_asset_warnings.add(background_asset_key)
                print(f"Background asset not found for key: {background_asset_key}")
            background = self._create_placeholder_surface(self.width, self.height, (50, 50, 100))
            
        # Scale and draw the background
        background = pygame.transform.scale(background, (self.width, self.height))
        self.screen.blit(background, (0, 0))
        return pygame.Rect(0, 0, self.width, self.height)
        
    def _draw_video_background(self, video_asset_key):
        """
        Draw a video background frame.
        
        Args:
            video_asset_key (str): The key of the video background.
            
        Returns:
            pygame.Rect: The rectangle of the background.
        """
        # Check if we have frames for this video
        if video_asset_key not in self.video_backgrounds:
            print(f"Video background not loaded: {video_asset_key}")
            placeholder = self._create_placeholder_surface(self.width, self.height, (100, 0, 100))
            self.screen.blit(placeholder, (0, 0))
            return pygame.Rect(0, 0, self.width, self.height)
            
        # Get the video frames
        frames = self.video_backgrounds[video_asset_key]
        
        # Calculate which frame to show based on time
        frame_index = (pygame.time.get_ticks() // 100) % len(frames)
        
        # Get the current frame
        current_frame = frames[frame_index]
        
        # Draw the frame
        self.screen.blit(current_frame, (0, 0))
        
        return pygame.Rect(0, 0, self.width, self.height)
        
    def draw_map(self, map_key, pos, size, player_pos=None):
        """
        Draw a map with optional player position.
        
        Args:
            map_key (str): The key of the map.
            pos (tuple): (x, y) position to draw at.
            size (tuple): (width, height) of the map.
            player_pos (tuple, optional): (x, y) position of the player on the map.
            
        Returns:
            pygame.Rect: The rectangle of the map.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        x, y = pos
        width, height = size
        
        map_surface = self.get_map(map_key)
        if not map_surface:
            # If not found, create a placeholder
            map_surface = self._create_placeholder_surface(width, height, (100, 150, 100))
            
        # Scale and draw the map
        map_surface = pygame.transform.scale(map_surface, (width, height))
        self.screen.blit(map_surface, (x, y))
        
        # Draw player position if provided
        if player_pos:
            px, py = player_pos
            # Convert to screen coordinates
            screen_x = x + int(px * width)
            screen_y = y + int(py * height)
            # Draw player marker
            pygame.draw.circle(self.screen, (255, 0, 0), (screen_x, screen_y), 5)
            
        return pygame.Rect(x, y, width, height)
        
    def draw_progress_bar(self, pos, size, value, label=None, color=(0, 255, 0), 
                         bg_color=(50, 50, 50), border_color=(200, 200, 200)):
        """
        Draw a progress bar.
        
        Args:
            pos (tuple): (x, y) position of the top-left corner.
            size (tuple): (width, height) of the bar.
            value (float): Value between 0.0 and 1.0.
            label (str, optional): Label to display on the bar.
            color (tuple): RGB color for the filled portion.
            bg_color (tuple): RGB color for the background.
            border_color (tuple): RGB color for the border.
            
        Returns:
            pygame.Rect: The rectangle of the progress bar.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        x, y = pos
        width, height = size
        
        # Clamp value between 0 and 1
        value = max(0.0, min(1.0, value))
        
        # Draw background
        bg_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, bg_rect)
        
        # Draw filled portion
        fill_width = int(width * value)
        fill_rect = pygame.Rect(x, y, fill_width, height)
        pygame.draw.rect(self.screen, color, fill_rect)
        
        # Draw border
        pygame.draw.rect(self.screen, border_color, bg_rect, 1)
        
        # Draw label if provided
        if label:
            label_surface = self.render_text(label, font_size=height - 4)
            if label_surface:
                label_width = label_surface.get_width()
                label_height = label_surface.get_height()
                label_x = x + (width - label_width) // 2
                label_y = y + (height - label_height) // 2
                self.screen.blit(label_surface, (label_x, label_y))
                
        return bg_rect
            
    def draw_icon(self, icon_key, pos, width=32, height=32):
        """
        Draw an icon.
        
        Args:
            icon_key (str): The key of the icon.
            pos (tuple): (x, y) position to draw at.
            width (int): Width to draw the icon.
            height (int): Height to draw the icon.
            
        Returns:
            pygame.Rect: The rectangle of the icon.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        # Try to get the icon from the icon mapping
        icon_asset_key = self.icons.get(icon_key.lower())
        if not icon_asset_key:
            # If not found in mapping, try direct key
            icon_asset_key = f"icon_{icon_key.lower()}"
            
        icon = self.get_asset(icon_asset_key)
        if not icon:
            # If still not found, create a placeholder
            icon = self._create_placeholder_surface(width, height, (150, 150, 200))
            
        # Scale and draw the icon
        icon = pygame.transform.scale(icon, (width, height))
        self.screen.blit(icon, pos)
        return pygame.Rect(pos[0], pos[1], width, height)
            
    def draw_animation(self, animation_key, pos, frame, width=64, height=64):
        """
        Draw a frame of an animation.
        
        Args:
            animation_key (str): The key of the animation.
            pos (tuple): (x, y) position to draw at.
            frame (int): The frame number to draw.
            width (int): Width to draw the frame.
            height (int): Height to draw the frame.
            
        Returns:
            pygame.Rect: The rectangle of the animation frame.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        # Try to get the animation from the animation mapping
        anim_asset_key = self.animations.get(animation_key.lower())
        if not anim_asset_key:
            # If not found in mapping, try direct key
            anim_asset_key = f"anim_{animation_key.lower()}"
            
        animation = self.get_asset(anim_asset_key)
        if not animation:
            # If still not found, create a placeholder
            animation = self._create_placeholder_surface(width, height, (200, 200, 100))
            
        # Scale and draw the animation frame
        # In a real implementation, we would have a spritesheet or multiple frames
        animation = pygame.transform.scale(animation, (width, height))
        self.screen.blit(animation, pos)
        return pygame.Rect(pos[0], pos[1], width, height)
            
    def update(self):
        """Update the game clock."""
        if self.initialized and self.graphics_enabled:
            self.clock.tick(self.fps)
    
    def update_display(self):
        """Update the display to show all drawn elements."""
        if self.initialized and self.graphics_enabled:
            pygame.display.flip()
        
    def clear(self, color=(0, 0, 0)):
        """Clear the screen."""
        if self.initialized and self.graphics_enabled:
            self.screen.fill(color)
            
    def toggle_graphics(self):
        """Toggle graphics on/off."""
        self.graphics_enabled = not self.graphics_enabled
        
    def cleanup(self):
        """Clean up resources."""
        if self.initialized:
            pygame.quit()
            self.initialized = False
            
    def handle_resize(self, event):
        """Handle window resize events."""
        if event.type == pygame.VIDEORESIZE:
            self.width = event.w
            self.height = event.h
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
            
    def draw_enemy_sprite(self, enemy_key, pos, width=64, height=64):
        """
        Draw an enemy sprite.
        
        Args:
            enemy_key (str): The key of the enemy.
            pos (tuple): (x, y) position to draw at.
            width (int): Width to draw the sprite.
            height (int): Height to draw the sprite.
            
        Returns:
            pygame.Rect: The rectangle of the sprite.
        """
        if not self.initialized or not self.graphics_enabled:
            return None
            
        # Try to get the sprite from the enemy mapping
        sprite_key = self.enemy_sprites.get(enemy_key.lower())
        if not sprite_key:
            # If not found in mapping, try direct key
            sprite_key = f"enemy_{enemy_key.lower()}"
            
        sprite = self.get_asset(sprite_key)
        if not sprite:
            # If still not found, create a placeholder
            sprite = self._create_placeholder_surface(width, height, (200, 100, 100))
            
        # Scale and draw the sprite
        sprite = pygame.transform.scale(sprite, (width, height))
        self.screen.blit(sprite, pos)
        return pygame.Rect(pos[0], pos[1], width, height) 