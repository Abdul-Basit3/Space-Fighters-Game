# Space Fighters - Complete Game Guide

## Quick Start

1. Run `python main.py`
2. Watch the splash screen (or press any key to skip)
3. Select "Play" from the main menu
4. Choose your level from the level map
5. Select your ship
6. Press SPACE to start
7. Destroy enemies and defeat the boss!

## Game Flow

### Main Menu
- **Play**: Start the game
- **Settings**: Adjust audio and game settings
- **Quit**: Exit the game

### Level Selection
- View all 5 levels on the map
- Completed levels are marked in GREEN
- Available levels are marked in WHITE
- Locked levels are marked in GRAY
- Use arrow keys or click to select
- Press SPACE/ENTER or click to start

### Ship Selection
- Choose from unlocked ships
- Ship 1: Always available
- Ship 2: Unlocked after Level 2
- Blue Ship: Unlocked after Level 4
- Each ship has unique shooting sounds

## Gameplay Mechanics

### Objective
Each level has two phases:
1. **Enemy Phase**: Destroy the required number of enemies
2. **Boss Phase**: Defeat the level boss

### Power-Up System
Power-ups drop randomly when you destroy enemies:
- **Yellow (Bullet Power)**: Upgrades your weapon
  - Level 0 → 1: Single → Double shot
  - Level 1 → 2: Double → Triple spread
  - Level 2 → 3: Triple → Quad shot
- **Red (Health)**: Restores 30 HP
- **Green (Shield)**: Temporary invincibility + 20 HP

### Damage System
- Enemy bullets: 10 damage each
- Enemy collision: 20 damage
- Asteroid collision: 15 damage
- **Important**: Taking damage reduces your bullet power level!

### Time Limits
- Regular levels: 90 seconds
- Bonus mission: 60 seconds
- Timer stops during boss battles

## Bonus Mission

### Unlocking
- Complete Level 4 to unlock
- Appears as an option after Level 4 completion
- Can be skipped if desired

### Objective
- Destroy 30 asteroids within 60 seconds
- Asteroids have 2 HP each
- Higher power-up drop rate (40% vs 20%)

### Benefits
- Gain extra bullet power
- Restore health
- Prepare for the final boss battle

### Tips
- Asteroids rotate and fall at varying speeds
- Focus on collecting power-ups
- Use this mission to maximize your power before Level 5

## Boss Battles

### Boss Mechanics
- Bosses move horizontally across the screen
- They shoot multiple bullets
- Health bar displayed at top of screen
- More aggressive in higher levels

### Boss Progression
- **Level 1-2 Bosses**: Single bullet, 30-40 HP
- **Level 3-4 Bosses**: Triple bullets, 50-60 HP
- **Level 5 Final Boss**: Five bullets, 80 HP

### Strategy
- Stay mobile to avoid bullet patterns
- Use power-ups before the boss fight
- Focus fire on the boss
- Watch for bullet spread patterns

## Ship Characteristics

### Ship 1 (Default)
- Balanced stats
- Standard shooting rate
- Sound: ship_shoot.wav

### Ship 2 (Unlock: Level 2)
- Improved handling
- Standard shooting rate
- Sound: player_shoot.wav

### Blue Ship (Unlock: Level 4)
- Uses blue laser bullets
- **20% faster shooting rate**
- Best for rapid fire gameplay
- Sound: laser_shooting.wav

## Pause Menu

Press **ESC** or **P** during gameplay to pause.

While paused:
- Game freezes completely
- Press ESC or P again to resume
- No progress is lost

## Settings Menu

Access from main menu or pause screen.

### Options
1. **Music Volume**: 0-100% (LEFT/RIGHT to adjust)
2. **Sound Volume**: 0-100% (LEFT/RIGHT to adjust)
3. **Mute Music**: Toggle music on/off
4. **Mute Sounds**: Toggle sound effects on/off
5. **Reset Game**: Clear all progress (requires confirmation)
6. **Back**: Return to previous screen

### Volume Controls
- Use LEFT/RIGHT arrow keys to adjust
- Changes apply immediately
- Settings are saved automatically

## Save System

### Auto-Save
Progress is automatically saved:
- After completing each level
- When accessing settings
- When quitting the game

### Saved Data
- Highest level reached
- Completed levels
- Unlocked ships
- Current bullet power
- Current health
- Bonus mission completion
- Audio settings

### Manual Save
- Access Settings menu
- Adjust settings (triggers auto-save)
- Or simply quit the game

### Reset Progress
1. Go to Settings
2. Select "Reset Game"
3. Press Y to confirm
4. All progress will be cleared

## Advanced Tips

### Maximizing Score
- Enemy kills: 10 × level points
- Boss kills: 500 points
- Power-ups: 50 points
- Complete bonus mission for extra points

### Survival Strategies
1. **Stay Mobile**: Constant movement avoids bullets
2. **Collect Power-Ups**: Higher bullet power = faster kills
3. **Manage Health**: Don't let it drop too low
4. **Use Shields Wisely**: Save for tough situations
5. **Learn Patterns**: Each boss has predictable movements

### Optimal Progression
1. Complete Levels 1-3 normally
2. Complete Level 4
3. **Do the Bonus Mission** - maximize power-ups
4. Tackle Level 5 with maximum power

### Power Management
- Try to maintain Bullet Level 3 or 4
- Avoid taking damage to preserve bullet power
- Use bonus mission to stack power-ups
- Shield power-ups protect your bullet level

## Troubleshooting

### Game Won't Start
- Ensure Python 3.7+ is installed
- Install pygame: `pip install pygame`
- Check that all files are in the same directory

### No Sound
- Check Settings menu - ensure not muted
- Verify sound files are in assets/sounds/
- Adjust volume levels in Settings

### Missing Graphics
- Verify image files are in assets/images/
- Game will use placeholders if images missing
- Check file names match exactly

### Progress Not Saving
- Ensure write permissions in game directory
- Check for game_save.json file
- Try running as administrator (Windows)

### Performance Issues
- Close other applications
- Reduce window size
- Update graphics drivers

## Keyboard Shortcuts Reference

### In-Game
- **WASD / Arrows**: Move
- **Space / Left Click**: Shoot
- **ESC / P**: Pause
- **Right Click**: Drag ship

### Menus
- **Arrow Keys**: Navigate
- **Enter / Space**: Select
- **ESC**: Back
- **Left Click**: Select option

### Settings
- **Up/Down**: Navigate options
- **Left/Right**: Adjust values
- **Enter**: Toggle/Select
- **ESC**: Back

## Achievement Goals

Try to accomplish these challenges:
- [ ] Complete all 5 levels
- [ ] Complete bonus mission
- [ ] Unlock all 3 ships
- [ ] Reach Bullet Level 4
- [ ] Complete a level without taking damage
- [ ] Defeat final boss with full health
- [ ] Score over 5000 points
- [ ] Complete Level 5 with Ship 1

## Credits

**Game Design**: Enhanced space shooter with progression
**Programming**: Python + Pygame
**Features**: 5 levels, bonus mission, save system, settings menu
**Audio**: Dynamic sound system with volume controls

Enjoy your space adventure!
