# Riventide

Riventide is a text-based RPG with simple graphics and audio, set in a rich fantasy world that draws inspiration from various fantasy sources. The game combines traditional text-based gameplay with atmospheric visuals and sound to create an immersive experience.

## Features

- **Text-Based Gameplay**: Core gameplay is driven by text, allowing for rich storytelling and player choice.
- **Simple Graphics**: Visual elements enhance the atmosphere without overwhelming the text-based nature.
- **Dynamic Audio**: Region-specific music and context-appropriate sound effects.
- **Rich World**: Explore the diverse regions of Riventide, each with unique characteristics and challenges.
- **Character Development**: Create and develop your character with various classes and skills.
- **Companion System**: Recruit companions to join you on your journey.
- **Combat System**: Strategic turn-based combat with dice mechanics.

## Regions of Riventide

- **Eldoria**: The central kingdom, with castles, villages, and farmlands.
- **Drakkar**: A militaristic region with fortresses and training grounds.
- **Faerie**: A mystical forest realm with magical creatures.
- **Barbarian Steppes**: Rugged plains inhabited by tribal warriors.
- **Shadowlands**: A dark, corrupted area filled with undead and demons.

## Character Classes

- **Warrior**: Masters of combat with strength and resilience.
- **Mage**: Wielders of arcane magic with powerful spells.
- **Rogue**: Stealthy operators with skills in deception and precision.
- **Healer**: Practitioners of restorative magic and support abilities.
- **Archer**: Ranged specialists with keen eyes and deadly accuracy.

## Companions

- **Sir Gareth**: A noble knight from Eldoria.
- **Luna**: A mysterious mage from the Faerie realm.
- **Krag**: A fierce barbarian warrior from the Steppes.
- **Sera**: A skilled rogue with a shadowy past.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/riventide.git
   cd riventide
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

### Quick Start

For the easiest way to play:

- **Windows**: Double-click `play_riventide.bat`
- **macOS/Linux**: Double-click `play_riventide.py` or run `./play_riventide.sh` in a terminal

### Command Line Options

To start the game with default settings:
```
python main.py
```

Command line options:
```
python main.py --text-only  # Run in text-only mode without graphics
python main.py --width 1024 --height 768  # Set custom window size
python main.py --no-music  # Disable music
python main.py --no-sound  # Disable sound effects
```

### Controls

- **Main Menu**:
  - Use **Up/Down arrow keys** to navigate menu options
  - Press **Enter** or **Space** to select an option
  - Press **Escape** to exit the game

- **Exploration Mode**:
  - Press **I** to open inventory
  - Press **M** to open map
  - Press **C** to open character screen
  - Press **Q** to open quest log
  - Press **Escape** to return to the main menu

- **Other Modes**:
  - Press **Escape** to return to the previous mode or menu

### Creating a macOS Application (macOS only)

To create a standalone macOS application:
```
python create_macos_app.py
```
This will create a `Riventide.app` that you can double-click to play.

## Testing

To test the audio and graphics systems:
```
python test_audio_graphics.py
```

## Project Structure

- `game/`: Core game modules
  - `audio/`: Audio management
  - `ui/`: User interface and graphics
  - `world/`: World and region definitions
  - `characters/`: Character classes and NPCs
  - `combat/`: Combat system
  - `items/`: Items and inventory
  - `quests/`: Quest system
- `assets/`: Game assets
  - `audio/`: Music and sound effects
  - `graphics/`: Images and animations
- `main.py`: Main game entry point
- `requirements.txt`: Required Python packages

## Development Status

Riventide is currently in active development. The following components have been implemented:

- [x] Basic game engine
- [x] Graphics management
- [x] Audio management
- [x] Character classes
- [x] World structure
- [ ] Complete quest system
- [ ] Full combat system
- [ ] Save/load functionality
- [ ] Complete storyline

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Inspired by classic text-based RPGs and modern fantasy literature
- Built with Python and Pygame 