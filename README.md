# Space Fighters - Enhanced Edition

A comprehensive space shooter game built with Python and Pygame featuring 5 progressive levels, bonus missions, multiple ships, and advanced gameplay mechanics.

## Features

### Game Progression
- **5 Progressive Levels**: Each level features unique enemies, bosses, and increasing difficulty
- **Bonus Asteroid Mission**: Unlocked after completing Level 4, destroy asteroids to gain power-ups
- **Boss Battles**: Face unique bosses at the end of each level, culminating in the final boss at Level 5
- **Save/Load System**: Your progress, bullet power, health, and unlocked ships are automatically saved

### Ships & Unlockables
- **Ship 1** (Default): Standard spaceship available from the start
  - Shooting sound: `ship_shoot.wav`
- **Ship 2**: Unlocked after completing Level 2
  - Shooting sound: `player_shoot.wav`
- **Blue Ship**: Unlocked after completing Level 4
  - Uses blue laser bullets
  - Faster shooting rate
  - Shooting sound: `laser_shooting.wav`

### Weapons & Power-ups
- **Bullet Progression**:
  - Bullet 1: Default single shot
  - Bullet 2: Double shot (first power-up)
  - Bullet 3: Triple spread shot (second power-up)
  - Bullet 4: Quad shot (third power-up)
- **Power-up Types**:
  - Bullet Power: Increases your bullet level
  - Health: Restores 30 HP
  - Shield: Temporary invincibility + 20 HP
- **Bullet Power Reduction**: Your bullet power decreases when hit by enemies

### Levels & Environments
- **Dynamic Backgrounds**: Rotates through Space 1, Space 2, and Space 3
- **Planet Visuals**: Each level displays its corresponding planet (Planet-1 through Planet-5) at the center
- **Bonus Mission**: Special asteroid field with bonus.jpg background

### Enemies
- **Level-Specific Enemies**: Each level has unique enemy ships (enemy_L1 through enemy_L5)
- **Progressive AI**: Enemies become smarter and more aggressive in higher levels
- **Boss Progression**: Unique boss for each level (boss_L1 through boss_L5_ship)

### Audio System
- **Background Music**: Continuous background music with volume control
- **Sound Effects**:
  - Enemy explosions: `explosion_1.wav`
  - Boss explosions: `explosion_2.wav`
  - Mission complete: `mission_complete.wav` (Levels 1-4)
  - Final victory: `Win.mp3` (Level 5 boss defeat)
  - Game over: `game_over.wav` followed by `loose.wav`
- **Settings Menu**:
  - Adjust music volume (0-100%)
  - Adjust sound effects volume (0-100%)
  - Mute music independently
  - Mute sounds independently

### Gameplay Features
- **Pause System**: Press ESC or P to pause the game
- **Responsive Window**: Fully resizable game window
- **Mouse & Keyboard Controls**:
  - WASD or Arrow Keys: Move ship
  - Space or Left Mouse: Shoot
  - Right/Middle Mouse: Drag ship to position
  - ESC/P: Pause game
- **Visual Effects**:
  - Explosion animations for enemies and player
  - Shield visual indicator
  - Boss health bar
  - Bullet power indicator
  - Real-time HUD with score, health, time, and objectives

### Settings & Progress
- **Settings Menu**: Access from main menu
  - Volume controls
  - Mute options
  - Reset game progress
- **Auto-Save**: Progress automatically saved after each level
- **Manual Save**: Save before quitting from settings menu

## Installation

1. Install Python 3.7 or higher
2. Install Pygame:
   ```bash
   pip install pygame
   ```
3. Run the game:
   ```bash
   python main.py
   ```

## Controls

### Movement
- **WASD** or **Arrow Keys**: Move your ship
- **Right Mouse Button**: Drag ship to position

### Combat
- **Space** or **Left Mouse Button**: Shoot (hold for continuous fire)

### Menu Navigation
- **Arrow Keys**: Navigate menus
- **Enter/Space**: Select option
- **ESC**: Go back/Pause game

### Game Controls
- **P** or **ESC**: Pause/Resume game

## Game Progression

1. **Level 1-3**: Complete levels to unlock Ship 2
2. **Level 4**: Complete to unlock Blue Ship and Bonus Mission
3. **Bonus Mission**: Optional asteroid destruction mission for power-ups
4. **Level 5**: Final level with the ultimate boss battle

## Tips

- Collect power-ups to increase your bullet power
- Your bullet power decreases when hit, so avoid enemy fire
- Use the bonus mission to maximize your power before Level 5
- Shield power-ups provide temporary invincibility
- Each ship has unique characteristics - experiment to find your favorite
- Pause the game to access settings and adjust audio levels

## File Structure

- `main.py`: Main game loop and level management
- `game.py`: Core game logic, collision detection, and state management
- `entities.py`: Player, enemies, bosses, bullets, power-ups, and asteroids
- `ui.py`: All UI screens and menus
- `settings_menu.py`: Settings and audio controls
- `assets.py`: Asset loading and audio management
- `save_system.py`: Save/load game progress
- `constants.py`: Game constants and configuration
- `assets/`: All game assets (images and sounds)

## Credits

Developed with Python and Pygame
Enhanced Edition with advanced features and progression system
