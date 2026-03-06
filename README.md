# Space Fighters

An exhilarating space shooter game developed with Python and Pygame featuring progressive enemy AI, boss battles, and power-ups.

## Features

- 3 progressive levels with unique space backgrounds
- Progressive ship unlocking system (unlock ships by completing levels)
- Interactive level map for level selection and replay
- Boss battles at the end of each level
- Final boss battle with enhanced difficulty
- 3 types of power-ups: Enhanced Bullets (Bullet 2), Super Bullets (Bullet 3), and Shield
- Time-based challenges (90 seconds per level)
- Progressive enemy count (15 enemies in level 1, increasing by 10 each level)
- Score system with level multipliers
- Health system with visual health bar
- Sound effects for shooting, explosions, and game events
- Background music
- Level replay system - replay any completed level
- **Full window management support** - resize, minimize, maximize, close
- **Responsive design** - game scales to any window size
- **Full mouse support** - play entirely with mouse if desired

## Progression System

- Start with Ship 1 unlocked
- Complete Level 1 to unlock Ship 2
- Complete Level 2 to unlock Ship 3
- Replay any completed level with any unlocked ship
- Level map shows your progress with completed/locked levels

## Requirements

- Python 3.7+
- Pygame

## Installation

```bash
pip install pygame
```

## Assets Required

Place these files in the same directory as main.py:

### Images:
- `space1.jpg`, `space2.jpg`, `space3.jpg` - Level backgrounds
- `ship1.png`, `ship2.png`, `ship3.png` - Player ship options
- `enemy_1.png`, `enemy_2.png`, `enemy_3.png` - Enemy ships
- `boss.png` - Mid-level boss
- `boss_ship.png` - Final boss
- `bullet_1.png`, `bullet_2.png`, `bullet_3.png` - Bullet types
- `life_bar.png` - Health bar (optional, will use default if missing)

### Sounds:
- `background_sound.wav` - Background music
- `player_shoot.wav` - Player shooting sound
- `space_shoot1.wav` - Enemy shooting sound
- `boss_shoot.wav` - Boss shooting sound
- `explosion_1.wav` - Enemy destruction sound
- `explosion_2.wav` - Boss destruction sound
- `game_over.wav` - Game over sound

Note: The game will work without assets by using placeholder graphics and no sound.

## How to Play

```bash
python main.py
```

## Controls

**Space Fighters supports FULL MOUSE CONTROL!** You can play the entire game with just your mouse, or use keyboard, or mix both.

### Mouse Controls (Full Game Support):
- **Left Click / Hold**: Fire weapons (in-game)
- **Right Click + Drag**: Move spaceship by dragging (in-game)
- **Middle Click + Drag**: Alternative ship movement (in-game)
- **Click Buttons**: Navigate all menus and screens
- **Click Levels**: Select levels on the map
- **Click Ships**: Select ships in ship selection
- **Click Continue/Restart/Quit**: All message screens

### Keyboard Controls:
- **Arrow Keys / WASD**: Move spaceship (in-game)
- **Spacebar**: Fire weapons (in-game)
- **LEFT/RIGHT Arrows**: Navigate menus
- **SPACE**: Confirm selections
- **R**: Restart (on game over screen)
- **Q**: Quit (on game over screen)

### Hybrid Controls (Recommended):
You can combine mouse and keyboard for optimal control:
- **WASD + Left Click**: Keyboard movement + Mouse shooting
- **Right Mouse Drag + Spacebar**: Mouse movement + Keyboard shooting
- **Full Mouse**: Right button to move + Left button to shoot

**See CONTROLS.md for complete control guide**

## Power-Ups

- **Yellow (Bullet 2)**: Enhanced double-shot bullets
- **Purple (Bullet 3)**: Super triple-shot bullets with increased damage
- **Green (Shield)**: Protects from damage and restores 30 health

## Gameplay

- Start by viewing the level map - only Level 1 is available initially
- Select your spaceship (only Ship 1 is unlocked at start)
- Destroy the required number of enemies to spawn the boss
- Defeat the boss to complete the level
- Completing levels unlocks new ships and levels
- Collect power-ups to enhance your weapons
- Avoid enemy bullets and collisions
- Complete all 3 levels and defeat the final boss to win
- Each level increases enemy speed, health, and fire rate
- Return to the level map after completing or failing a level
- Replay any completed level to improve your score

## Level Progression

1. Level 1: Complete to unlock Ship 2 and Level 2
2. Level 2: Complete to unlock Ship 3 and Level 3
3. Level 3: Final level with the ultimate boss battle

## Window Management

Space Fighters supports all standard window operations:
- **Resize**: Drag window edges or corners to any size
- **Minimize**: Click minimize button or Windows + Down Arrow
- **Maximize**: Click maximize button or Windows + Up Arrow
- **Close**: Click X button or Alt + F4
- **Responsive**: Game automatically scales to window size
- **Adaptive HUD**: UI elements reposition based on window size

See **WINDOW_FEATURES.md** for detailed window management guide.

---

- After destroying the required enemies, a boss appears
- Bosses have significantly more health and shoot more frequently
- The final boss (level 3) shoots triple bullets and is extra tough
- Defeat the boss to progress to the next level

## Scoring

- Enemy destruction: 10 × current level points
- Boss destruction: 500 points
- Power-up collection: 50 points

Good luck, pilot!

