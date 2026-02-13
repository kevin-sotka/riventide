"""
Audio management for Riventide
"""

import os
import pygame
import threading
import time
from enum import Enum
import logging
import random

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
    """Manages music and sound effects for the game."""
    
    def __init__(self):
        """Initialize the audio manager."""
        self.initialized = False
        self.music_enabled = True
        self.sound_enabled = True
        self.music_volume = 0.5
        self.sound_volume = 0.7
        self.current_music = None
        self.fade_thread = None
        
        # Music file paths
        self.music_paths = {
            MusicType.MAIN_THEME: "assets/audio/music/main_theme.mp3",
            MusicType.ELDORIA: "assets/audio/music/eldoria.mp3",
            MusicType.DRAKKAR: "assets/audio/music/drakkar.mp3",
            MusicType.FAERIE: "assets/audio/music/faerie.mp3",
            MusicType.BARBARIAN: "assets/audio/music/barbarian.mp3",
            MusicType.SHADOWLANDS: "assets/audio/music/shadowlands.mp3",
            MusicType.COMBAT: "assets/audio/music/combat.mp3",
            MusicType.VICTORY: "assets/audio/music/victory.mp3",
            MusicType.DEFEAT: "assets/audio/music/defeat.mp3",
            MusicType.LEVEL_UP: "assets/audio/music/level_up.mp3",
            MusicType.QUEST_COMPLETE: "assets/audio/music/quest_complete.mp3",
            MusicType.BOSS_BATTLE: "assets/audio/music/boss_battle.mp3",
            MusicType.TAVERN: "assets/audio/music/tavern.mp3",
            MusicType.TRAGIC: "assets/audio/music/tragic.mp3",
            MusicType.WHISPERWOOD: "assets/audio/music/whisperwood.mp3",
            MusicType.ROYAL_COURT: "assets/audio/music/royal_court.mp3",
            MusicType.ALIEN_TECH: "assets/audio/music/alien_tech.mp3",
            MusicType.SYNTHETIC: "assets/audio/music/synthetic.mp3",
            # New music for scenes 7-11
            MusicType.FAERIE_REALM: "assets/audio/music/faerie_realm.mp3",
            MusicType.CRYSTAL_GROVE: "assets/audio/music/crystal_grove.mp3",
            MusicType.KNOWLEDGE_INTERFACE: "assets/audio/music/knowledge_interface.mp3",
            MusicType.TWILIGHT_MARSHES: "assets/audio/music/twilight_marshes.mp3",
            MusicType.GRACKLE_ENCOUNTER: "assets/audio/music/grackle_encounter.mp3",
            MusicType.FAERIE_SCOUTS: "assets/audio/music/faerie_scouts.wav",
            # Prison and escape music (all replaced with vanlander_prison.wav)
            MusicType.PRISON: "assets/audio/music/vanlander_prison.wav",
            MusicType.PRISON_ALARM: "assets/audio/music/vanlander_prison.wav",
            MusicType.PRISON_ESCAPE: "assets/audio/music/vanlander_prison.wav",
            MusicType.CAPTURED_BY_GRACKLES: "assets/audio/music/captured_by_grackles.wav",
            MusicType.VOID_AMBIENT: "assets/audio/music/void_ambient.mp3",
            MusicType.CRASH_SITE: "assets/audio/music/crash_site.mp3",
            MusicType.SHUTTLE_CHASE: "assets/audio/music/shuttle_chase.mp3",
            MusicType.FINAL_BATTLE: "assets/audio/music/final_battle.mp3",
            MusicType.MAGIC_TAVERN: "assets/audio/music/magic_tavern.mp3",
            MusicType.DEATH_MUSIC: "assets/audio/music/death_music.wav"
        }
        
        # Sound effect file paths
        self.sound_paths = {
            SoundEffect.SWORD_SLASH: "assets/audio/sfx/sword_slash.wav",
            SoundEffect.MAGIC_CAST: "assets/audio/sfx/magic_cast.wav",
            SoundEffect.ARROW_SHOT: "assets/audio/sfx/arrow_shot.wav",
            SoundEffect.HEAL: "assets/audio/sfx/heal.wav",
            SoundEffect.ITEM_PICKUP: "assets/audio/sfx/item_pickup.wav",
            SoundEffect.DOOR_OPEN: "assets/audio/sfx/door_open.wav",
            SoundEffect.CHEST_OPEN: "assets/audio/sfx/chest_open.wav",
            SoundEffect.MONSTER_GROWL: "assets/audio/sfx/monster_growl.wav",
            SoundEffect.MONSTER_DEATH: "assets/audio/sfx/monster_death.wav",
            SoundEffect.PLAYER_HIT: "assets/audio/sfx/player_hit.wav",
            SoundEffect.PLAYER_DEATH: "assets/audio/sfx/player_death.wav",
            SoundEffect.MENU_SELECT: "assets/audio/sfx/menu_select.wav",
            SoundEffect.DICE_ROLL: "assets/audio/sfx/dice_roll.wav",
            SoundEffect.TECH_HUM: "assets/audio/sfx/tech_hum.wav",
            SoundEffect.ALIEN_COMMUNICATION: "assets/audio/sfx/alien_communication.wav",
            SoundEffect.ENERGY_WEAPON: "assets/audio/sfx/energy_weapon.wav",
            SoundEffect.TECH_ACTIVATION: "assets/audio/sfx/tech_activation.wav",
            SoundEffect.FOREST_AMBIENCE: "assets/audio/sfx/forest_ambience.wav",
            SoundEffect.STATIC_WHISPERS: "assets/audio/sfx/static_whispers.wav",
            SoundEffect.CLICK: "assets/audio/sfx/click.wav",
            SoundEffect.DIALOGUE_ADVANCE: "assets/audio/sfx/dialogue_advance.wav",
            # New sound effects for scenes 7-11
            SoundEffect.FAERIE_CHIMES: "assets/audio/sfx/faerie_chimes.wav",
            SoundEffect.CRYSTAL_RESONANCE: "assets/audio/sfx/crystal_resonance.wav",
            SoundEffect.DATA_TRANSMISSION: "assets/audio/sfx/data_transmission.wav",
            SoundEffect.HEARTSTONE_PULSE: "assets/audio/sfx/heartstone_pulse.wav",
            SoundEffect.DRONE_BUZZ: "assets/audio/sfx/drone_buzz.wav",
            SoundEffect.SCANNER_BEAM: "assets/audio/sfx/scanner_beam.wav",
            SoundEffect.GRACKLE_ALARM: "assets/audio/sfx/grackle_alarm.wav",
            SoundEffect.HOLOGRAM_ACTIVATE: "assets/audio/sfx/hologram_activate.wav",
            SoundEffect.CRYSTAL_OVERLOAD: "assets/audio/sfx/crystal_overload.wav",
            # Prison and escape sound effects
            SoundEffect.PRISON_DOOR: "assets/audio/sfx/prison_door.wav",
            SoundEffect.ALARM_BLARE: "assets/audio/sfx/alarm_blare.wav",
            SoundEffect.VENTILATION_AMBIENCE: "assets/audio/sfx/ventilation_ambience.wav",
            SoundEffect.METAL_CREAK: "assets/audio/sfx/metal_creak.wav",
            SoundEffect.ENERGY_BARRIER: "assets/audio/sfx/energy_barrier.wav",
            SoundEffect.SHUTTLE_ENGINE: "assets/audio/sfx/shuttle_engine.wav",
            SoundEffect.CRASH_IMPACT: "assets/audio/sfx/crash_impact.wav",
            SoundEffect.VOID_WIND: "assets/audio/sfx/void_wind.wav",
            SoundEffect.TRACTOR_BEAM: "assets/audio/sfx/tractor_beam.wav",
            SoundEffect.REALITY_WARP: "assets/audio/sfx/reality_warp.wav",
            SoundEffect.TAVERN_AMBIENCE: "assets/audio/sfx/tavern_ambience.wav"
        }
        
        # Sound effect cache
        self.sound_cache = {}
        
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
            # Prison and escape mappings (all replaced with vanlander_prison)
            "captured_by_grackles": MusicType.CAPTURED_BY_GRACKLES,
            "vanlander_prison_capture": MusicType.PRISON,
            "vent_escape": MusicType.PRISON,
            "alarm_escape": MusicType.PRISON,
            "panel_escape": MusicType.PRISON,
            "outer_pursuit": MusicType.PRISON,
            "delayed_escape": MusicType.PRISON,
            "hidden_exit": MusicType.PRISON,
            "lockdown": MusicType.PRISON,
            "alternate_route": MusicType.PRISON,
            "power_core": MusicType.ALIEN_TECH,
            "void_survival": MusicType.VOID_AMBIENT,
            "shuttle_chase": MusicType.SHUTTLE_CHASE,
            "maintenance_shaft": MusicType.PRISON,
            "safe_exit": MusicType.PRISON,
            "crash_landing": MusicType.CRASH_SITE,
            "final_showdown": MusicType.FINAL_BATTLE,
            "story_end": MusicType.MAGIC_TAVERN,
            "tech_soldiers_parley": MusicType.DEATH_MUSIC,
            "combat_tech_soldiers": MusicType.DEATH_MUSIC
        }
        
        # Location to music mapping
        self.location_music = {
            # Add any location-specific music here
            "royal_court": MusicType.ROYAL_COURT,
            "whisperwood_start": MusicType.WHISPERWOOD,
            "alien_tech_discovery": MusicType.ALIEN_TECH,
            "synthetic_clearing": MusicType.SYNTHETIC,
            "mushroom_path": MusicType.WHISPERWOOD,
            "tech_ambush_risk": MusicType.COMBAT,
            "faerie_border": MusicType.FAERIE,
            "faerie_realm_entry": MusicType.FAERIE_REALM,
            "test_of_loyalty": MusicType.FAERIE_REALM,
            "crystal_interface": MusicType.KNOWLEDGE_INTERFACE,
            "crash_site_retrieval": MusicType.CRASH_SITE,
            "grackle_encounter": MusicType.GRACKLE_ENCOUNTER,
            # Prison and escape locations (all replaced with vanlander_prison)
            "captured_by_grackles": MusicType.CAPTURED_BY_GRACKLES,
            "vanlander_prison_capture": MusicType.PRISON,
            "vent_escape": MusicType.PRISON,
            "alarm_escape": MusicType.PRISON,
            "outer_pursuit": MusicType.PRISON,
            "void_survival": MusicType.VOID_AMBIENT,
            "shuttle_chase": MusicType.SHUTTLE_CHASE,
            "final_showdown": MusicType.FINAL_BATTLE,
            "story_end": MusicType.MAGIC_TAVERN,
            "tech_soldiers_parley": MusicType.DEATH_MUSIC,
            "combat_tech_soldiers": MusicType.DEATH_MUSIC
        }
        
        # Initialize pygame mixer
        self._initialize()
        
    def _initialize(self):
        """Initialize the pygame mixer."""
        try:
            pygame.mixer.init()
            self.initialized = True
            
            # Create directories if they don't exist
            os.makedirs("assets/audio/music", exist_ok=True)
            os.makedirs("assets/audio/sfx", exist_ok=True)
            
            # Load sound effects into cache
            for sound, path in self.sound_paths.items():
                try:
                    if os.path.exists(path):
                        self.sound_cache[sound] = pygame.mixer.Sound(path)
                except:
                    print(f"Failed to load sound effect: {path}")
        except:
            print("Failed to initialize audio. Music and sound effects will be disabled.")
            self.initialized = False
            self.music_enabled = False
            self.sound_enabled = False
            
    def play_music(self, music_type, loop=True, fade_ms=1000):
        """
        Play a music track.
        
        Args:
            music_type (MusicType): The type of music to play.
            loop (bool): Whether to loop the music.
            fade_ms (int): Fade-in time in milliseconds.
        """
        if not self.initialized or not self.music_enabled:
            return
            
        if self.current_music == music_type:
            return
            
        path = self.music_paths.get(music_type)
        if not path or not os.path.exists(path):
            print(f"Music file not found: {path}")
            return
            
        try:
            # Stop any current fade thread
            if self.fade_thread and self.fade_thread.is_alive():
                self.fade_thread.join()
                
            # Fade out current music
            pygame.mixer.music.fadeout(fade_ms)
            time.sleep(fade_ms / 1000)
            
            # Load and play new music
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
            self.current_music = music_type
        except Exception as e:
            print(f"Error playing music: {e}")
            
    def play_music_for_region(self, region_id):
        """
        Play music appropriate for the given region.
        
        Args:
            region_id (str): The ID of the region.
        """
        music_type = self.region_music.get(region_id, MusicType.MAIN_THEME)
        self.play_music(music_type)
        
    def play_sound(self, sound_effect):
        """
        Play a sound effect.
        
        Args:
            sound_effect (SoundEffect): The sound effect to play.
        """
        if not self.initialized or not self.sound_enabled:
            return
            
        sound = self.sound_cache.get(sound_effect)
        if sound:
            sound.set_volume(self.sound_volume)
            sound.play()
        else:
            path = self.sound_paths.get(sound_effect)
            if not path or not os.path.exists(path):
                print(f"Sound effect file not found: {path}")
                return
                
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sound_volume)
                sound.play()
                self.sound_cache[sound_effect] = sound
            except Exception as e:
                print(f"Error playing sound effect: {e}")
                
    def play_looping_sound(self, sound_effect, loops=-1):
        """
        Play a sound effect in a loop.
        
        Args:
            sound_effect (SoundEffect): The sound effect to play.
            loops (int): Number of times to loop the sound. -1 for infinite looping.
        """
        if not self.initialized or not self.sound_enabled:
            return
            
        sound = self.sound_cache.get(sound_effect)
        if sound:
            sound.set_volume(self.sound_volume)
            sound.play(loops=loops)
        else:
            path = self.sound_paths.get(sound_effect)
            if not path or not os.path.exists(path):
                print(f"Sound effect file not found: {path}")
                return
                
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(self.sound_volume)
                sound.play(loops=loops)
                self.sound_cache[sound_effect] = sound
            except Exception as e:
                print(f"Error playing looping sound effect: {e}")
                
    def stop_music(self, fade_ms=1000):
        """
        Stop the currently playing music.
        
        Args:
            fade_ms (int): Fade-out time in milliseconds.
        """
        if not self.initialized:
            return
            
        pygame.mixer.music.fadeout(fade_ms)
        self.current_music = None
        
    def stop_sound(self, sound_effect):
        """
        Stop a specific sound effect.
        
        Args:
            sound_effect (SoundEffect): The sound effect to stop.
        """
        if not self.initialized:
            return
            
        sound = self.sound_cache.get(sound_effect)
        if sound:
            sound.stop()
        
    def set_music_volume(self, volume):
        """
        Set the music volume.
        
        Args:
            volume (float): Volume level from 0.0 to 1.0.
        """
        self.music_volume = max(0.0, min(1.0, volume))
        if self.initialized:
            pygame.mixer.music.set_volume(self.music_volume)
            
    def set_sound_volume(self, volume):
        """
        Set the sound effect volume.
        
        Args:
            volume (float): Volume level from 0.0 to 1.0.
        """
        self.sound_volume = max(0.0, min(1.0, volume))
        
    def toggle_music(self):
        """Toggle music on/off."""
        self.music_enabled = not self.music_enabled
        if self.initialized:
            if not self.music_enabled:
                pygame.mixer.music.stop()
            elif self.current_music:
                self.play_music(self.current_music)
                
    def toggle_sound(self):
        """Toggle sound effects on/off."""
        self.sound_enabled = not self.sound_enabled
        
    def cleanup(self):
        """Clean up resources."""
        if self.initialized:
            pygame.mixer.quit()
            self.initialized = False

    def play_scene_music(self, scene_id: str) -> None:
        """Play music specific to a scene."""
        scene_music = {
            "grackle_incursion": "synthetic",
            "vision_of_tanis": "alien_tech",
            "void_exile": "tragic",
            "spire_shielded": "synthetic",
            "warship_focus": "synthetic",
            "cave_shelter": "void_ambient",
            "injured_retreat": "vanlander_prison",
            "crash_site_retrieval": "crash_site"
        }
        
        if scene_id in scene_music:
            self.play_music(scene_music[scene_id])

    def fade_out_music(self, time_ms=1000):
        """
        Fade out the currently playing music.
        
        Args:
            time_ms (int): Time in milliseconds to fade out
        """
        pygame.mixer.music.fadeout(time_ms)
        self.current_music = None
        logging.info("Music faded out")

    def play_random_music(self, category=None):
        """
        Play a random music track from a category.
        
        Args:
            category (str): Optional category to filter music by
        """
        if not self.initialized or not self.music_enabled:
            return False
            
        # Get all music files
        music_files = list(self.music_paths.glob("*.wav"))
        if not music_files:
            logging.warning("No music files found")
            return False
            
        # Filter by category if specified
        if category:
            music_files = [f for f in music_files if category in f.name]
            if not music_files:
                logging.warning(f"No music files found for category: {category}")
                return False
        
        # Select random file
        music_file = random.choice(music_files)
        
        try:
            # Stop any currently playing music
            pygame.mixer.music.stop()
            
            # Load and play the new track
            pygame.mixer.music.load(str(music_file))
            pygame.mixer.music.play(-1)  # Loop indefinitely
            
            # Update current music
            self.current_music = music_file.stem
            
            logging.info(f"Playing random music: {self.current_music}")
            return True
            
        except Exception as e:
            logging.error(f"Error playing random music: {str(e)}")
            return False 

    def play_music_for_location_or_scene(self, location_id=None, scene_id=None):
        """
        Play music for a given scene or location, prioritizing:
        1. Scene-specific music (via play_scene_music)
        2. Location-specific music (location_music)
        3. Region-based music (region_music)
        4. Default/main theme as a last resort
        Args:
            location_id (str): The location ID.
            scene_id (str, optional): The scene ID.
        """
        # 1. Scene-specific music
        if scene_id:
            scene_music = {
                "grackle_incursion": "synthetic",
                "vision_of_tanis": "alien_tech",
                "void_exile": "tragic",
                "spire_shielded": "synthetic",
                "warship_focus": "synthetic",
                "cave_shelter": "void_ambient",
                "injured_retreat": "vanlander_prison",
                "crash_site_retrieval": "crash_site"
            }
            if scene_id in scene_music:
                self.play_music(scene_music[scene_id])
                return
        # 2. Location-specific music
        if location_id and location_id in self.location_music:
            self.play_music(self.location_music[location_id])
            return
        # 3. Region-based music
        if location_id:
            # Try to infer region from location_id
            for region, music_type in self.region_music.items():
                if location_id.startswith(region):
                    self.play_music(music_type)
                    return
        # 4. Default
        self.play_music(MusicType.MAIN_THEME) 