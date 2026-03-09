# Score Point Acquisition & Game Save System

## Score Point Acquisition

The player earns score points through the following actions during gameplay:

### 1. Destroying Regular Enemies
- **Formula**: `10 × Current Level`
- **Examples**:
  - Level 1: 10 points per enemy
  - Level 2: 20 points per enemy
  - Level 3: 30 points per enemy
  - Level 4: 40 points per enemy
  - Level 5: 50 points per enemy
- **Location**: `game.py` line ~293
- **Trigger**: When enemy health reaches 0

### 2. Defeating Bosses
- **Points**: 500 points (flat rate)
- **Location**: `game.py` line ~260
- **Trigger**: When boss health reaches 0
- **Note**: Final boss (Level 5) does not award points but triggers victory

### 3. Collecting Power-Ups (Bullet Power Only)
- **Points**: 50 points
- **Location**: `game.py` line ~323
- **Trigger**: Only when collecting Bullet Power power-up (yellow square)
- **Important**: Health and Shield power-ups do NOT award score points

## Score Calculation Summary

| Action | Points Awarded | Notes |
|--------|---------------|-------|
| Enemy Kill (Level 1) | 10 | Scales with level |
| Enemy Kill (Level 2) | 20 | Scales with level |
| Enemy Kill (Level 3) | 30 | Scales with level |
| Enemy Kill (Level 4) | 40 | Scales with level |
| Enemy Kill (Level 5) | 50 | Scales with level |
| Boss Defeat | 500 | Fixed amount |
| Bullet Power Pickup | 50 | Only this power-up type |
| Health Pickup | 0 | No points awarded |
| Shield Pickup | 0 | No points awarded |

## Power-Up System

### Power-Up Types

There are three types of power-ups that drop randomly (20% chance) when enemies are destroyed:

#### 1. Bullet Power (Yellow Square with Orange Center)
- **Visual**: 20×20 yellow square with 10×10 orange inner rectangle
- **Effect**: Increases bullet power level by 1 (max level 3)
- **Duration**: 300 frames (~5 seconds at 60 FPS)
- **Score**: +50 points
- **Progression**:
  - Level 0 → 1: Single shot → Double shot
  - Level 1 → 2: Double shot → Triple spread shot
  - Level 2 → 3: Triple spread → Quad shot (4 bullets)
- **Note**: Bullet power decreases by 1 when taking 10+ damage

#### 2. Health (Red Circle with White Center)
- **Visual**: 20×20 red square with white circle
- **Effect**: Restores +30 HP (max 100 HP)
- **Duration**: Instant
- **Score**: 0 points

#### 3. Shield (Green Circle with White Center)
- **Visual**: 20×20 green square with white circle
- **Effect**: Temporary invulnerability + 20 HP restoration
- **Duration**: 300 frames (~5 seconds at 60 FPS)
- **Score**: 0 points
- **Visual Indicator**: Green circle drawn around player ship

## Game Save System

### Save File Location
- **File**: `game_save.json`
- **Format**: JSON
- **Location**: Root directory of the game

### Saved Data Structure

```json
{
    "highest_level": 1,
    "completed_levels": [false, false, false, false, false],
    "unlocked_ships": [true, false, false],
    "bullet_power": 0,
    "player_health": 100,
    "music_volume": 0.3,
    "sound_volume": 0.5,
    "music_muted": false,
    "sound_muted": false
}
```

### Save Data Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `highest_level` | Integer | Maximum level reached by player | 1 |
| `completed_levels` | Boolean Array | Completion status for each of 5 levels | [false, false, false, false, false] |
| `unlocked_ships` | Boolean Array | Unlock status for 3 ships | [true, false, false] |
| `bullet_power` | Integer | Current bullet power level (0-3) | 0 |
| `player_health` | Integer | Current player health | 100 |
| `music_volume` | Float | Background music volume (0.0-1.0) | 0.3 |
| `sound_volume` | Float | Sound effects volume (0.0-1.0) | 0.5 |
| `music_muted` | Boolean | Music mute status | false |
| `sound_muted` | Boolean | Sound effects mute status | false |

### Save Triggers

The game automatically saves progress in the following situations:

1. **Level Completion** - When a level is successfully completed
   - Location: `game.py` in `next_level()` method
   - Saves: Level completion status, unlocked ships, player stats

2. **Game Exit** - When the player quits the game
   - Location: `game.py` in `handle_events()` method (QUIT event)
   - Location: `main.py` in main menu quit option
   - Saves: All current progress and settings

3. **Ship Unlock** - When new ships are unlocked
   - Ship 2: Unlocked after completing Level 1
   - Ship 3 (Blue Ship): Unlocked after completing Level 3
   - Location: `game.py` in `next_level()` method

### Load Behavior

- **On Game Start**: Automatically loads saved progress from `game_save.json`
- **If No Save Exists**: Creates default progress with only Ship 1 unlocked
- **Location**: `game.py` in `load_game_progress()` method

### Progression Continuity

#### When Continuing Through Levels (Sequential Play)
- Bullet power level carries over to next level
- Player health carries over to next level
- Flag: `continuing_game = True`

#### When Selecting Level from Map
- Bullet power resets to 0
- Player health resets to 100
- Allows replaying levels with fresh stats

### Ship Unlock System

| Ship | Unlock Condition | Special Ability |
|------|-----------------|-----------------|
| Ship 1 | Always unlocked | Standard shooting |
| Ship 2 | Complete Level 1 | Standard shooting |
| Ship 3 (Blue) | Complete Level 3 | Faster shooting (200ms vs 250ms delay) + Laser bullets |

### Save System Functions

#### `save_progress(data)` - `save_system.py`
- Writes game progress to JSON file
- Returns: `True` on success, `False` on error
- Error handling: Prints error message if save fails

#### `load_progress()` - `save_system.py`
- Reads game progress from JSON file
- Returns: Dictionary with progress data or `None` if no save exists
- Error handling: Returns `None` if file doesn't exist or read fails

#### `get_default_progress()` - `save_system.py`
- Returns default progress structure for new games
- Used when no save file exists

## Implementation Details

### Code Locations

- **Score Calculation**: `game.py` lines 236-340 in `update()` method
- **Power-Up Collection**: `game.py` lines 318-323
- **Power-Up Types**: `entities.py` lines 14-20 (PowerUpType enum)
- **Power-Up Creation**: `entities.py` lines 399-429 (PowerUp class)
- **Save System**: `save_system.py` (entire file)
- **Save/Load Calls**: `game.py` in `Game` class methods

### Enemy Spawn Rate
- **Drop Chance**: 20% (0.2 probability)
- **Location**: `game.py` line ~296
- **Random Selection**: Power-up type is randomly chosen from all three types

### Level Progression
- **Total Levels**: 5
- **Enemies Required**: `20 + (level - 1) × 5`
  - Level 1: 20 enemies
  - Level 2: 25 enemies
  - Level 3: 30 enemies
  - Level 4: 35 enemies
  - Level 5: 40 enemies
- **Time Limit**: `45 + (level × 5)` seconds
  - Level 1: 50 seconds
  - Level 2: 55 seconds
  - Level 3: 60 seconds
  - Level 4: 65 seconds
  - Level 5: 70 seconds

## Notes

- Score is NOT saved between sessions - it resets when returning to main menu
- Only progression (levels, ships, settings) is saved
- Bullet power can be lost during gameplay when taking damage (10+ damage = -1 level)
- Maximum bullet power level is 3 (Quad shot)
- Power-ups have a 20% drop rate from destroyed enemies
- All three power-up types have equal probability of dropping
