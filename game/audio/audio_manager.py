#!/usr/bin/env python3
"""
Audio Manager for Riventide
Handles music and sound effects playback
"""

import os
import pygame
import logging
import random
from pathlib import Path
from enum import Enum

from game.assets_config import AUDIO_BASE, AUDIO_EXT

class MusicType(Enum):
    """Types of music in the game."""
    MAIN_THEME = "main_theme"
    ELDORIA = "eldoria"
    DRAKKAR = "drakkar"
    FAERIE = "faerie"
    BARBARIAN = "barbarian"
    SHADOWLANDS = "shadowlands"
    COMBAT = "combat"
    VICTORY = "victory"
    DEFEAT = "defeat"
    LEVEL_UP = "level_up"
    QUEST_COMPLETE = "quest_complete"
    BOSS_BATTLE = "boss_battle"
    TAVERN = "tavern"
    TRAGIC = "tragic"
    # New sci-fi music types
    WHISPERWOOD = "whisperwood"
    ROYAL_COURT = "royal_court"
    ALIEN_TECH = "alien_tech"
    SYNTHETIC = "synthetic"
    # Music for scenes 7-11
    FAERIE_REALM = "faerie_realm"
    CRYSTAL_GROVE = "crystal_grove"
    KNOWLEDGE_INTERFACE = "knowledge_interface"
    TWILIGHT_MARSHES = "twilight_marshes"
    GRACKLE_ENCOUNTER = "grackle_encounter"
    FAERIE_SCOUTS = "faerie_scouts"
    # Additional music for prison and escape scenes
    PRISON = "prison"
    PRISON_ALARM = "prison_alarm"
    PRISON_ESCAPE = "prison_escape"
    CAPTURED_BY_GRACKLES = "captured_by_grackles"
    VOID_AMBIENT = "void_ambient"
    CRASH_SITE = "crash_site"
    SHUTTLE_CHASE = "shuttle_chase"
    FINAL_BATTLE = "final_battle"
    MAGIC_TAVERN = "magic_tavern"
    DEATH_MUSIC = "death_music"

class SoundEffect(Enum):
    """Sound effects in the game."""
    SWORD_SLASH = "sword_slash"
    MAGIC_CAST = "magic_cast"
    ARROW_SHOT = "arrow_shot"
    HEAL = "heal"
    ITEM_PICKUP = "item_pickup"
    DOOR_OPEN = "door_open"
    CHEST_OPEN = "chest_open"
    MONSTER_GROWL = "monster_growl"
    MONSTER_DEATH = "monster_death"
    PLAYER_HIT = "player_hit"
    PLAYER_DEATH = "player_death"
    MENU_SELECT = "menu_select"
    DICE_ROLL = "dice_roll"
    # New sci-fi sound effects
    TECH_HUM = "tech_hum"
    ALIEN_COMMUNICATION = "alien_communication"
    ENERGY_WEAPON = "energy_weapon"
    TECH_ACTIVATION = "tech_activation"
    FOREST_AMBIENCE = "forest_ambience"
    STATIC_WHISPERS = "static_whispers"
    CLICK = "click"
    DIALOGUE_ADVANCE = "dialogue_advance"
    # Sound effects for scenes 7-11
    FAERIE_CHIMES = "faerie_chimes"
    CRYSTAL_RESONANCE = "crystal_resonance"
    DATA_TRANSMISSION = "data_transmission"
    HEARTSTONE_PULSE = "heartstone_pulse"
    DRONE_BUZZ = "drone_buzz"
    SCANNER_BEAM = "scanner_beam"
    GRACKLE_ALARM = "grackle_alarm"
    HOLOGRAM_ACTIVATE = "hologram_activate"
    CRYSTAL_OVERLOAD = "crystal_overload"
    # Additional sound effects for prison and escape scenes
    PRISON_DOOR = "prison_door"
    ALARM_BLARE = "alarm_blare"
    VENTILATION_AMBIENCE = "ventilation_ambience"
    METAL_CREAK = "metal_creak"
    ENERGY_BARRIER = "energy_barrier"
    SHUTTLE_ENGINE = "shuttle_engine"
    CRASH_IMPACT = "crash_impact"
    VOID_WIND = "void_wind"
    TRACTOR_BEAM = "tractor_beam"
    REALITY_WARP = "reality_warp"
    TAVERN_AMBIENCE = "tavern_ambience"

class AudioManager:
    """
    Manages all audio for the game, including music and sound effects.
    Provides methods for playing, pausing, and stopping audio.
    """
    
    def __init__(self, music_volume=0.5, sound_volume=0.6):
        """
        Initialize the audio manager.
        
        Args:
            music_volume (float): Initial music volume (0.0 to 1.0)
            sound_volume (float): Initial sound effects volume (0.0 to 1.0)
        """
        # Initialize pygame mixer if not already initialized
        self.initialized = False
        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
            self.initialized = True
        except Exception as e:
            print(f"Error initializing audio mixer: {e}")
            self.initialized = False
        
        # Set up paths
        self.base_path = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        # Base dir switches between assets/audio (desktop) and
        # web/assets/audio (RIVENTIDE_WEB=1) via game/assets_config.py.
        self.music_path = self.base_path / AUDIO_BASE / "music"
        self.sfx_path = self.base_path / AUDIO_BASE / "sfx"
        
        # Create directories if they don't exist
        self._initialize()
        
        # Set volumes
        self.music_volume = music_volume
        self.sound_volume = sound_volume
        if self.initialized:
            pygame.mixer.music.set_volume(self.music_volume)
        
        # Cache for sound effects
        self.sound_cache = {}
        
        # Current music track
        self.current_music = None
        
        # Audio enabled flags
        self.music_enabled = True
        self.sound_enabled = True
        
        # Region to music mapping
        self.region_music = {
            "eldoria": MusicType.ELDORIA,
            "drakkar": MusicType.DRAKKAR,
            "faerie": MusicType.FAERIE,
            "barbarian": MusicType.BARBARIAN,
            "shadowlands": MusicType.SHADOWLANDS,
            "whisperwood": MusicType.WHISPERWOOD,
            "whisperwood_start": MusicType.WHISPERWOOD,
            "royal_court": MusicType.ROYAL_COURT,
            "alien_tech_discovery": MusicType.ALIEN_TECH,
            "synthetic_clearing": MusicType.SYNTHETIC,
            "mushroom_path": MusicType.WHISPERWOOD,
            "tech_ambush_risk": MusicType.COMBAT,
            # New music mappings for scenes 7-11
            "faerie_scouts": MusicType.FAERIE_SCOUTS,
            "faerie_invasion_reaction": MusicType.FAERIE_SCOUTS,
            "faerie_escort": MusicType.FAERIE_SCOUTS,
            "faerie_path": MusicType.FAERIE_REALM,
            "faerie_border": MusicType.FAERIE_REALM,
            "faerie_realm_entrance": MusicType.FAERIE_REALM,
            "faerie_vision": MusicType.FAERIE_REALM,
            "crystal_grove": MusicType.CRYSTAL_GROVE,
            "drone_aftermath": MusicType.CRYSTAL_GROVE,
            "test_of_loyalty": MusicType.CRYSTAL_GROVE,
            "knowledge_repository": MusicType.KNOWLEDGE_INTERFACE,
            "crystal_interface": MusicType.KNOWLEDGE_INTERFACE,
            "overloaded_connection": MusicType.KNOWLEDGE_INTERFACE,
            "safe_disconnect": MusicType.KNOWLEDGE_INTERFACE,
            "faerie_favor": MusicType.KNOWLEDGE_INTERFACE,
            "twilight_marshes": MusicType.TWILIGHT_MARSHES,
            "crash_site_retrieval": MusicType.CRASH_SITE,
            "heartstone_retrieval": MusicType.TWILIGHT_MARSHES,
            "grackle_scout_encounter": MusicType.GRACKLE_ENCOUNTER,
            "grackle_encounter": MusicType.GRACKLE_ENCOUNTER,
            "grackle_deception": MusicType.GRACKLE_ENCOUNTER,
            "forest_escape": MusicType.GRACKLE_ENCOUNTER,
            "scout_ship_battle": MusicType.COMBAT,
            # Prison and escape mappings
            "captured_by_grackles": MusicType.CAPTURED_BY_GRACKLES,
            "vanlander_prison_capture": MusicType.PRISON,
            "vent_escape": MusicType.PRISON_ESCAPE,
            "alarm_escape": MusicType.PRISON_ALARM,
            "panel_escape": MusicType.PRISON_ESCAPE,
            "outer_pursuit": MusicType.PRISON_ESCAPE,
            "delayed_escape": MusicType.PRISON_ESCAPE,
            "hidden_exit": MusicType.PRISON_ESCAPE,
            "lockdown": MusicType.PRISON_ALARM,
            "alternate_route": MusicType.PRISON_ESCAPE,
            "power_core": MusicType.ALIEN_TECH,
            "void_survival": MusicType.VOID_AMBIENT,
            "shuttle_chase": MusicType.SHUTTLE_CHASE,
            "maintenance_shaft": MusicType.PRISON_ESCAPE
        }
        
        # Logging
        logging.info("AudioManager initialized")
    
    def _initialize(self):
        """Initialize directories and check for audio files."""
        # Ensure directories exist
        os.makedirs(self.music_path, exist_ok=True)
        os.makedirs(self.sfx_path, exist_ok=True)
        
        # Check for audio files
        music_files = list(self.music_path.glob(f"*{AUDIO_EXT}"))
        sfx_files = list(self.sfx_path.glob(f"*{AUDIO_EXT}"))
        
        if not music_files:
            logging.warning("No music files found in %s", self.music_path)
        
        if not sfx_files:
            logging.warning("No sound effect files found in %s", self.sfx_path)
    
    def play_music(self, track_name, loop=True):
        """
        Play a music track.
        
        Args:
            track_name (str): Name of the track to play (without extension)
            loop (bool): Whether to loop the track
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.initialized or not self.music_enabled:
            return False
            
        # Don't restart the same track
        if self.current_music == track_name:
            return True
        
        # Build the file path
        file_path = self.music_path / f"{track_name}{AUDIO_EXT}"
        
        # Check if file exists
        if not file_path.exists():
            logging.error("Music file not found: %s", file_path)
            return False
        
        try:
            # Stop any currently playing music
            pygame.mixer.music.stop()
            
            # Load and play the new track
            pygame.mixer.music.load(str(file_path))
            pygame.mixer.music.play(-1 if loop else 0)
            
            # Update current music
            self.current_music = track_name
            
            logging.info("Playing music: %s", track_name)
            return True
            
        except Exception as e:
            logging.error("Error playing music %s: %s", track_name, str(e))
            return False
    
    def stop_music(self):
        """Stop the currently playing music."""
        pygame.mixer.music.stop()
        self.current_music = None
        logging.info("Music stopped")
    
    def pause_music(self):
        """Pause the currently playing music."""
        pygame.mixer.music.pause()
        logging.info("Music paused")
    
    def unpause_music(self):
        """Unpause the currently playing music."""
        pygame.mixer.music.unpause()
        logging.info("Music unpaused")
    
    def fade_out_music(self, time_ms=1000):
        """
        Fade out the currently playing music.
        
        Args:
            time_ms (int): Time in milliseconds to fade out
        """
        pygame.mixer.music.fadeout(time_ms)
        self.current_music = None
        logging.info("Music faded out")
    
    def stop_sound(self, sound_name):
        """
        Stop a specific sound effect.
        
        Args:
            sound_name (str): Name of the sound to stop (without extension)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.initialized:
            return False
            
        # Check if sound is in cache
        if sound_name in self.sound_cache:
            sound = self.sound_cache[sound_name]
            sound.stop()
            logging.debug("Stopped sound: %s", sound_name)
            return True
        else:
            logging.warning("Tried to stop sound that wasn't loaded: %s", sound_name)
            return False
    
    def play_sound(self, sound_name):
        """
        Play a sound effect.
        
        Args:
            sound_name (str): Name of the sound to play (without extension)
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.initialized or not self.sound_enabled:
            return False
            
        # Check if sound is already in cache
        if sound_name in self.sound_cache:
            sound = self.sound_cache[sound_name]
        else:
            # Build the file path
            file_path = self.sfx_path / f"{sound_name}{AUDIO_EXT}"
            
            # Check if file exists
            if not file_path.exists():
                logging.error("Sound file not found: %s", file_path)
                return False
            
            try:
                # Load the sound
                sound = pygame.mixer.Sound(str(file_path))
                sound.set_volume(self.sound_volume)
                
                # Add to cache
                self.sound_cache[sound_name] = sound
                
            except Exception as e:
                logging.error("Error loading sound %s: %s", sound_name, str(e))
                return False
        
        # Play the sound
        try:
            sound.play()
            logging.debug("Playing sound: %s", sound_name)
            return True
            
        except Exception as e:
            logging.error("Error playing sound %s: %s", sound_name, str(e))
            return False
    
    def play_looping_sound(self, sound_name, loops=-1):
        """
        Play a sound effect in a loop.
        
        Args:
            sound_name (str): Name of the sound to play (without extension)
            loops (int): Number of times to loop the sound. -1 for infinite looping.
            
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.initialized or not self.sound_enabled:
            return False
            
        # Check if sound is already in cache
        if sound_name in self.sound_cache:
            sound = self.sound_cache[sound_name]
        else:
            # Build the file path
            file_path = self.sfx_path / f"{sound_name}{AUDIO_EXT}"
            
            # Check if file exists
            if not file_path.exists():
                logging.error("Sound file not found: %s", file_path)
                return False
            
            try:
                # Load the sound
                sound = pygame.mixer.Sound(str(file_path))
                sound.set_volume(self.sound_volume)
                
                # Add to cache
                self.sound_cache[sound_name] = sound
                
            except Exception as e:
                logging.error("Error loading sound %s: %s", sound_name, str(e))
                return False
        
        # Play the sound with looping
        try:
            sound.play(loops=loops)
            logging.debug("Playing looping sound: %s", sound_name)
            return True
            
        except Exception as e:
            logging.error("Error playing looping sound %s: %s", sound_name, str(e))
            return False
    
    def set_music_volume(self, volume):
        """
        Set the music volume.
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.initialized:
            pygame.mixer.music.set_volume(self.music_volume)
        logging.info("Music volume set to %f", self.music_volume)
    
    def set_sound_volume(self, volume):
        """
        Set the sound effects volume.
        
        Args:
            volume (float): Volume level (0.0 to 1.0)
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        
        # Update volume for all cached sounds
        for sound in self.sound_cache.values():
            sound.set_volume(self.sound_volume)
            
        logging.info("Sound volume set to %f", self.sound_volume)
    
    def get_music_volume(self):
        """Get the current music volume."""
        return self.music_volume
    
    def get_sound_volume(self):
        """Get the current sound effects volume."""
        return self.sound_volume
    
    def is_music_playing(self):
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()
    
    def play_random_music(self, category=None):
        """
        Play a random music track, optionally from a specific category.
        
        Args:
            category (str, optional): Category to choose from (e.g., 'combat', 'region')
        
        Returns:
            bool: True if successful, False otherwise
        """
        # Get all available music files
        music_files = list(self.music_path.glob(f"*{AUDIO_EXT}"))
        
        if not music_files:
            logging.error("No music files available")
            return False
        
        # Filter by category if specified
        if category:
            filtered_files = [f for f in music_files if category in f.stem]
            if filtered_files:
                music_files = filtered_files
        
        # Choose a random file
        random_file = random.choice(music_files)
        track_name = random_file.stem
        
        # Play the selected track
        return self.play_music(track_name)
    
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if not self.music_enabled and self.initialized:
            pygame.mixer.music.stop()
        elif self.music_enabled and self.current_music and self.initialized:
            self.play_music(self.current_music)
            
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled
            
    def cleanup(self):
        """Clean up audio resources."""
        pygame.mixer.quit()
        self.initialized = False
        logging.info("AudioManager cleaned up")

    def play_scene_music(self, scene_id: str) -> None:
        """Play music specific to a scene."""
        scene_music = {
            "grackle_incursion": "synthetic",
            "vision_of_tanis": "alien_tech",
            "void_exile": "tragic",
            "spire_shielded": "synthetic",
            "warship_focus": "synthetic",
            "cave_shelter": "void_ambient",
            "injured_retreat": "prison_alarm",
            "crash_site_retrieval": "crash_site",
            "captured_by_grackles": "captured_by_grackles"
        }
        
        if scene_id in scene_music:
            self.play_music(scene_music[scene_id])

    def play_music_for_location_or_scene(self, location_id=None, scene_id=None):
        """
        Play music for a given scene or location, prioritizing:
        1. Scene-specific music
        2. Location-specific music
        3. Region-based music
        4. Default/main theme as a last resort
        Args:
            location_id (str): The location ID.
            scene_id (str, optional): The scene ID.
        """
        # 1. Scene-specific music
        scene_music = {
            "grackle_incursion": "synthetic",
            "vision_of_tanis": "alien_tech",
            "void_exile": "tragic",
            "spire_shielded": "synthetic",
            "warship_focus": "synthetic",
            "cave_shelter": "void_ambient",
            "injured_retreat": "prison_alarm",
            "crash_site_retrieval": "crash_site",
            "captured_by_grackles": "captured_by_grackles"
        }
        if scene_id and scene_id in scene_music:
            self.play_music(scene_music[scene_id])
            return
        # 2. Location-specific music
        if location_id and hasattr(self, 'location_music') and location_id in self.location_music:
            self.play_music(self.location_music[location_id])
            return
        # 3. Region-based music
        if location_id:
            for region, music_type in self.region_music.items():
                if location_id.startswith(region):
                    self.play_music(music_type.value if hasattr(music_type, 'value') else music_type)
                    return
        # 4. Default
        self.play_music(MusicType.MAIN_THEME.value if hasattr(MusicType.MAIN_THEME, 'value') else MusicType.MAIN_THEME) 