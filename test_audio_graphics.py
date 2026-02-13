#!/usr/bin/env python3
"""
Test script for Riventide audio and graphics systems
"""

import os
import sys
import time
import pygame
import random
from game.ui.graphics_manager import GraphicsManager
from game.audio.audio_manager import AudioManager

def test_graphics():
    """Test the graphics manager functionality"""
    print("Testing Graphics Manager...")
    
    # Initialize the graphics manager
    graphics = GraphicsManager(800, 600)
    
    # Test background rendering
    regions = ["eldoria", "drakkar", "faerie", "barbarian", "shadowlands"]
    for region in regions:
        print(f"Displaying background for {region}...")
        graphics.draw_background(region)
        graphics.update_display()
        time.sleep(1)
    
    # Test character portraits
    characters = ["warrior", "mage", "rogue", "healer", "archer", "sir_gareth", "luna", "krag", "sera"]
    for character in characters:
        print(f"Displaying portrait for {character}...")
        graphics.draw_background("eldoria")  # Use a consistent background
        graphics.draw_character_portrait(character, (50, 50))
        graphics.update_display()
        time.sleep(1)
    
    # Test enemy sprites
    enemies = ["goblin", "orc", "troll", "skeleton", "dragon", "shadow_beast"]
    for enemy in enemies:
        print(f"Displaying sprite for {enemy}...")
        graphics.draw_background("shadowlands")  # Use a consistent background
        graphics.draw_enemy_sprite(enemy, (400, 300))
        graphics.update_display()
        time.sleep(1)
    
    # Test UI elements
    print("Testing UI elements...")
    graphics.draw_background("eldoria")
    
    # Draw text box
    graphics.draw_text_box("This is a test of the text box system in Riventide. It should wrap text appropriately and display it in a nice box.", (50, 400), (700, 150))
    
    # Draw progress bars
    graphics.draw_progress_bar((50, 50), (200, 20), 0.75, "Health")
    graphics.draw_progress_bar((50, 80), (200, 20), 0.5, "Mana")
    graphics.draw_progress_bar((50, 110), (200, 20), 0.25, "Stamina")
    
    # Draw icons
    icons = ["health", "mana", "experience", "gold", "inventory", "quest", "combat"]
    for i, icon in enumerate(icons):
        graphics.draw_icon(icon, (300 + i*50, 50))
    
    graphics.update_display()
    time.sleep(2)
    
    # Test animations
    animations = ["sword_slash", "magic_cast", "arrow_shot", "heal", "level_up"]
    for animation in animations:
        print(f"Playing animation: {animation}...")
        graphics.draw_background("eldoria")
        
        # Simulate animation frames
        for frame in range(5):  # Assume 5 frames per animation
            graphics.draw_background("eldoria")
            graphics.draw_animation(animation, (400, 300), frame)
            graphics.update_display()
            time.sleep(0.2)
    
    print("Graphics tests completed!")
    return graphics

def test_audio(audio):
    """Test the audio manager functionality"""
    print("Testing Audio Manager...")
    
    # Test music playback
    music_types = [
        "main_theme", "eldoria", "drakkar", "faerie", "barbarian", "shadowlands",
        "combat", "victory", "defeat", "level_up", "quest_complete", "boss_battle",
        "tavern", "tragic"
    ]
    
    for music_type in music_types:
        print(f"Playing music: {music_type}...")
        audio.play_music(music_type)
        time.sleep(3)  # Listen for 3 seconds
    
    # Test sound effects
    sound_effects = [
        "sword_slash", "magic_cast", "arrow_shot", "heal", "item_pickup",
        "door_open", "chest_open", "monster_growl", "monster_death",
        "player_hit", "player_death", "menu_select", "dice_roll"
    ]
    
    for sound_effect in sound_effects:
        print(f"Playing sound effect: {sound_effect}...")
        audio.play_sound(sound_effect)
        time.sleep(1)  # Wait for sound to finish
    
    print("Audio tests completed!")

def main():
    """Main test function"""
    print("Starting Riventide Audio and Graphics Test")
    
    # Initialize pygame
    pygame.init()
    
    try:
        # Test graphics first
        graphics = test_graphics()
        
        # Initialize audio manager
        audio = AudioManager()
        
        # Test audio
        test_audio(audio)
        
        # Final test: combined audio and graphics
        print("Testing combined audio and graphics...")
        
        # Display a random background
        region = random.choice(["eldoria", "drakkar", "faerie", "barbarian", "shadowlands"])
        graphics.draw_background(region)
        
        # Play corresponding music
        audio.play_music(region)
        
        # Display a character and enemy
        character = random.choice(["warrior", "mage", "rogue", "healer", "archer"])
        enemy = random.choice(["goblin", "orc", "troll", "skeleton", "dragon"])
        
        graphics.draw_character_portrait(character, (100, 300))
        graphics.draw_enemy_sprite(enemy, (500, 300))
        
        # Draw UI elements
        graphics.draw_text_box(f"A {character} faces off against a {enemy} in {region}!", (50, 450), (700, 100))
        graphics.draw_progress_bar((100, 250), (150, 15), 0.8, "Health")
        graphics.draw_progress_bar((500, 250), (150, 15), 0.6, "Health")
        
        graphics.update_display()
        
        # Play a combat sound
        audio.play_sound("sword_slash")
        
        print("Test complete! Press any key to exit...")
        
        # Wait for user to press a key
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    waiting = False
            time.sleep(0.1)
        
    except Exception as e:
        print(f"Error during testing: {e}")
    finally:
        pygame.quit()
        print("Test script finished.")

if __name__ == "__main__":
    main() 