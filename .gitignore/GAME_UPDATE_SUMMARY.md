# Space Fighters - Game Update Summary

## Game Overview
Space Fighters is a classic 2D space shooter game built with Python 3.x and Pygame 2.x. It's a vertical scrolling shoot 'em up featuring 5 progressive levels, epic boss battles, 3 unlockable ships, dynamic power-ups, and a complete save/load system. The game runs at 60 FPS with responsive controls and a fully resizable window.

## Platform and Technical Specifications

### Platform
- **Language**: Python 3.7+
- **Framework**: Pygame 2.x
- **Genre**: 2D Vertical Scrolling Shooter (Shmup)
- **Graphics**: 2D sprite-based raster graphics
- **Audio**: Pygame Mixer (SDL_mixer)
- **OS Support**: Windows, macOS, Linux
- **Performance**: 60 FPS locked frame rate
- **Resolution**: Resizable window (minimum 800x600)

### Programming Techniques
- Object-Oriented Programming (OOP) with sprite inheritance
- State machine pattern for game flow
- Sprite group pattern for efficient collision detection
- Factory pattern for entity creation
- Event-driven input handling
- JSON-based persistence system
- Modular architecture (~2,100 lines across 8 files)

## Core Features

### 1. Level System
- **5 Progressive Levels**: Each level increases in difficulty with more enemies and tougher bosses
- **Level-Specific Content**:
  - Unique enemy types for each level (enemy_L1 through enemy_L5)
  - Level-specific bosses (boss_L1 through boss_L5_ship)
  - Unique planets displayed at center of each level (planet-1 through planet-5)
  - Rotating space backgrounds (space1.jpg, space2.jpg, space3.jpg)

### 2. Ship System
- **3 Unlockable Ships**:
  - **Ship 1** (Default): Available from start, uses ship_shoot.wav
  - **Ship 2**: Unlocked after completing Level 1, uses player_shoot.wav
  - **Blue Ship**: Unlocked after completing Level 3, uses blue_laser.png and laser_shooting.wav with 20% faster fire rate

### 3. Weapon System
- **4 Bullet Power Levels**:
  - bullet_1.png (default, 1 damage)
  - bullet_2.png (first upgrade, 2 damage, double shot)
  - bullet_3.png (second upgrade, 3 damage, triple spread)
  - bullet_4.png (third upgrade, 4 damage, quad shot)
- **Power Progression**: Collect power-ups to increase bullet power
- **Damage Penalty**: Bullet power reduces by 1 level when taking 10+ damage
- **Fire Rate**: 250ms delay (4 shots/sec) for Ship 1 & 2, 200ms (5 shots/sec) for Blue Ship
- **Bullet Speed**: 10 pixels per frame upward

### 4. Boss Battles
- **5 Unique Bosses**: One for each level
- **Final Boss**: Level 5 features the ultimate boss (boss_L5_ship)
- **Progressive Difficulty**: Bosses get stronger and shoot more bullets as levels progress
- **Boss Patterns**:
  - Level 1-2: Single bullet
  - Level 3-4: Triple bullet spread
  - Level 5: Five bullet spread

### 5. Audio System
- **Background Music**: Continuous background_sound.wav
- **Ship-Specific Sounds**:
  - Ship 1: ship_shoot.wav
  - Ship 2: player_shoot.wav
  - Blue Ship: laser_shooting.wav
- **Combat Sounds**:
  - Enemy explosions: explosion_1.wav
  - Boss explosions: explosion_2.wav
  - Boss shooting: boss_shoot.wav
- **Mission Sounds**:
  - Level complete (1-4): mission_complete.wav
  - Final victory: Win.mp3
  - Game over: game_over.wav followed by loose.wav
- **Volume Controls**: Separate music and sound volume sliders with mute options

### 6. Power-Up System
- **Bullet Power**: Increases weapon strength
- **Health**: Restores player health
- **Shield**: Temporary invincibility with health boost

### 7. Save/Load System
- **Progress Tracking**:
  - Highest level reached
  - Completed levels
  - Unlocked ships
  - Audio settings (music/sound volume, mute states)
- **Persistent Storage**: JSON-based save file (game_save.json)

### 8. UI Features
- **Splash Screen**: Game icon with animated loading bar (5 seconds, skippable)
- **Main Menu**: Play, Settings, Quit options
- **Level Map**: Visual level selection with completion status
- **Ship Selection**: Visual ship selector with unlock requirements
- **Pause Menu**: Resume, Settings, Main Menu, Quit
- **Settings Menu**:
  - Music volume slider with visual bar
  - Sound volume slider with visual bar
  - Mute toggles for music and sounds
  - Game reset option
  - Mouse-interactive volume bars
- **HUD Display**:
  - Current level
  - Score
  - Enemy kill count
  - Time remaining
  - Bullet power level
  - Health bar
  - Active power-up indicator
  - Boss health bar

### 9. Controls
- **Movement**: WASD or Arrow Keys
- **Shooting**: SPACE or Left Mouse Button (auto-fire)
- **Mouse Drag**: Right/Middle Mouse Button to drag player
- **Pause**: ESC or P key
- **Menu Navigation**: Arrow Keys, ENTER, ESC
- **Volume Adjustment**: LEFT/RIGHT arrows or mouse drag on volume bars

### 10. Game Mechanics
- **Time Limits**: 
  - Formula: 120 + (level × 30) seconds
  - Level 1: 150 seconds (2:30)
  - Level 2: 180 seconds (3:00)
  - Level 3: 210 seconds (3:30)
  - Level 4: 240 seconds (4:00)
  - Level 5: 270 seconds (4:30)
- **Enemy Requirements**:
  - Formula: 15 + ((level - 1) × 5) enemies
  - Level 1: 15 enemies
  - Level 2: 20 enemies
  - Level 3: 25 enemies
  - Level 4: 30 enemies
  - Level 5: 35 enemies
- **Scoring**:
  - Regular enemies: 10 × level points
  - Bosses: 500 points
  - Power-ups: 50 points
- **Difficulty Scaling**:
  - Enemy speed: 1 + (level × 0.3) pixels/frame
  - Enemy health: 1 + (level ÷ 2) hits
  - Enemy shoot delay: max(1500 - level × 100, 800) ms
  - More enemies spawn simultaneously in higher levels
  - Boss health: 30 + (level × 10) HP
  - Boss attack patterns scale with level

## Enemy AI and Algorithms

### Basic Enemy AI
- **Movement**: Vertical descent + horizontal tracking toward player
- **Tracking Algorithm**: Simple pursuit - moves toward player's X position at 50% speed
- **Shooting**: Time-based with level-scaled delay (1400ms at L1, 1000ms at L5)
- **Spawning**: Random position at top of screen, uniform distribution
- **No Evasion**: Enemies don't avoid bullets (intentional for gameplay balance)

### Boss AI
- **Movement Pattern**: 
  - Phase 1: Descend from top to position (y = 50)
  - Phase 2: Horizontal oscillation across screen
- **Attack Patterns**:
  - Level 1-2: Single bullet (800ms delay)
  - Level 3-4: Triple spread (800ms delay)
  - Level 5 (Final Boss): Five-bullet spread (500ms delay)
- **No Player Tracking**: Predictable pattern for fair gameplay
- **Health Scaling**: 30 + (level × 10) HP

### AI Algorithms Used
1. **Simple Pursuit Algorithm**: Enemy horizontal tracking
2. **Spawn Distribution**: Uniform random positioning
3. **Difficulty Scaling**: Linear progression formulas
4. **AABB Collision Detection**: Pygame's optimized rect collision
5. **Random Power-Up Drops**: 20% chance, equal distribution
6. **Boss State Machine**: ENTERING → ACTIVE → EXPLODING → DEAD

### Performance
- All AI calculations: O(1) per entity per frame
- Collision detection: O(n × m) optimized by Pygame's C implementation
- No expensive pathfinding or raycasting
- Efficient for 60 FPS gameplay

## Technical Features

### Graphics Implementation
- **Type**: 2D raster graphics, sprite-based
- **Art Style**: Pixel art with PNG transparency
- **Color Depth**: 32-bit RGBA
- **Rendering**: Pygame's hardware-accelerated blitting
- **Dynamic Scaling**: All elements scale with window resize
- **Layering**: Background → Planet → Sprites → Effects → HUD → Overlays
- **Procedural Graphics**: Health bars, power-ups, enemy bullets
- **Visual Effects**: Shield circles, explosion animations, selection rectangles
- **Text Rendering**: Anti-aliased fonts (36pt and 24pt)

### Audio Implementation
- **Background Music**: Looping ambient track (background_sound.wav)
- **Sound Effects**: 12 WAV files for combat, UI, and mission events
- **Volume System**: Separate music and sound volume controls (0-100%)
- **Mute Toggles**: Independent mute for music and sounds
- **Volume Mixing**: Each sound has base multiplier × global volume
- **Persistence**: Audio settings saved to JSON
- **Real-time Updates**: Volume changes apply immediately

### Player Controls
- **Movement**: WASD or Arrow Keys (8-directional, 5 px/frame)
- **Alternative Movement**: Right/Middle mouse drag (up to 10 px/frame)
- **Shooting**: SPACE or Left Mouse (auto-fire with rate limiting)
- **Pause**: ESC or P key
- **Menu Navigation**: Arrow keys, ENTER, ESC
- **Volume Adjustment**: Arrow keys or mouse drag on sliders
- **Boundary Clamping**: Player confined to screen bounds

### Window Management
- **Responsive Design**: Fully resizable window
- **Dynamic Scaling**: All elements scale with window size
- **Event Handling**: Proper handling of window resize events

### Performance
- **60 FPS**: Smooth gameplay at 60 frames per second
- **Efficient Rendering**: Optimized sprite groups and collision detection
- **Resource Management**: Proper cleanup and memory management

### Code Structure
- **Modular Design**: Separated into logical modules
  - `main.py`: Entry point and game flow
  - `game.py`: Core game logic
  - `entities.py`: Player, enemies, bosses, bullets, power-ups
  - `ui.py`: All UI screens and menus
  - `settings_menu.py`: Settings interface
  - `assets.py`: Asset loading and management
  - `constants.py`: Game constants and configuration
  - `save_system.py`: Save/load functionality
- **Clean Architecture**: Clear separation of concerns
- **Error Handling**: Graceful fallbacks for missing assets

## Recent Updates

### Removed Features
- **Bonus Mission**: Removed asteroid bonus mission after level 4
  - Simplified level progression
  - Direct advancement from level 4 to level 5
  - Removed asteroid spawning and collision logic
  - Removed bonus-specific UI and prompts

### Bug Fixes
- Fixed ship unlock logic (Ship 2 after level 1, Blue Ship after level 3)
- Fixed level 5 progression after completing level 4
- Fixed pause menu window resize handling
- Fixed settings menu ESC behavior from pause
- Fixed player stats persistence between levels
- Fixed time limits for better gameplay balance
- Fixed Win.mp3 stopping when restart/quit is clicked

### UI Improvements
- Added ESC key to ship selection screen to return to menu
- Improved volume bar interaction with mouse
- Better selection rectangle coverage for volume controls
- Added button navigation and click sounds throughout all menus
- Updated instructions to show all available controls

## File Structure

```
space-fighters/
├── main.py                 # Entry point
├── game.py                 # Core game logic
├── entities.py             # Game entities
├── ui.py                   # UI screens
├── settings_menu.py        # Settings interface
├── assets.py               # Asset management
├── constants.py            # Game constants
├── save_system.py          # Save/load system
├── game_save.json          # Save file
├── assets/
│   ├── images/
│   │   ├── player/         # Player ships, bullets, UI
│   │   ├── enemy/          # Enemy ships and bosses
│   │   └── levels/         # Planets and backgrounds
│   └── sounds/             # All audio files
└── docs/                   # Documentation
```

## Assets Required

### Images
- **Player**: ship1.png, ship2.png, blue_ship.png, blue_laser.png
- **Bullets**: bullet_1.png through bullet_4.png
- **Enemies**: enemy_L1 through enemy_L5 (4 variants each)
- **Bosses**: boss_L1 through boss_L5_ship
- **Explosions**: enemy_explosion.png, player_explosion.png
- **Levels**: planet-1 through planet-5, space1-3.jpg
- **UI**: game_icon.png, life_bar.png

### Sounds
- **Background**: background_sound.wav
- **Shooting**: ship_shoot.wav, player_shoot.wav, laser_shooting.wav, boss_shoot.wav
- **Explosions**: explosion_1.wav, explosion_2.wav
- **UI**: button_nav.wav, button_click.wav
- **Mission**: mission_complete.wav, Win.mp3, game_over.wav, loose.wav

## How to Play

1. **Start Game**: Launch main.py
2. **Select Level**: Choose from unlocked levels on the level map
3. **Select Ship**: Choose your ship (unlock more by completing levels)
4. **Play**: Destroy enemies, avoid bullets, defeat the boss
5. **Progress**: Complete levels to unlock new ships and advance
6. **Pause**: Press ESC or P to pause anytime
7. **Settings**: Adjust audio, reset progress, or quit

## Victory Conditions
- Defeat all required enemies in each level
- Defeat the level boss
- Complete all 5 levels and defeat the final boss

## Game Over Conditions
- Player health reaches 0
- Time runs out (before boss appears)

## Tips
- Collect power-ups to increase bullet strength
- Shield power-ups provide temporary invincibility
- Higher bullet power means more damage
- Avoid taking damage to maintain bullet power
- Use the Blue Ship's faster fire rate for level 4 and 5
- Manage your time - defeat enemies quickly to face the boss

---

**Version**: 2.0
**Last Updated**: 2024
**Status**: Complete ✓
