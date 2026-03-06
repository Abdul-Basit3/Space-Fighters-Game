# Space Fighters - Code Structure

## Overview
The codebase has been refactored into a modular structure for better maintainability and organization.

## File Structure

```
Space Fighters/
├── main.py              # Main entry point and game loop
├── constants.py         # Game constants and colors
├── assets.py            # Asset loading (images, sounds)
├── entities.py          # Game entities (Player, Enemy, Boss, Bullets, PowerUps)
├── game.py              # Core game logic and state management
├── ui.py                # UI screens and menus
├── images/              # Image assets
├── sounds/              # Sound assets
├── enemy/               # Enemy images
└── docs/                # Documentation files
```

## Module Descriptions

### main.py (130 lines)
**Purpose**: Entry point and main game loop
**Key Functions**:
- `main()` - Initializes pygame, creates game instance, runs main loop
- Handles level progression flow
- Manages transitions between screens

**Dependencies**: All other modules

---

### constants.py (20 lines)
**Purpose**: Centralized configuration and constants
**Contents**:
- Window dimensions (INITIAL_WIDTH, INITIAL_HEIGHT)
- FPS setting
- Color definitions (BLACK, WHITE, RED, GREEN, etc.)

**Dependencies**: None

---

### assets.py (110 lines)
**Purpose**: Asset loading and management
**Key Functions**:
- `load_image(filename, default_size)` - Loads and scales images
- `load_sound(filename)` - Loads sound effects
- `initialize_sounds()` - Sets volumes and starts background music

**Assets Loaded**:
- Background images (3 levels)
- Player ships (3 options)
- Enemy images (3 types)
- Boss images (2 types)
- Bullet images (3 levels)
- Sound effects (7 types)

**Dependencies**: constants.py

---

### entities.py (350 lines)
**Purpose**: Game entity classes
**Classes**:
- `PowerUpType` - Enum for power-up types
- `Player` - Player spaceship with movement, shooting, health
- `Enemy` - Enemy ships with AI tracking
- `Boss` - Boss enemies with special patterns
- `Bullet` - Player bullets
- `EnemyBullet` - Enemy bullets
- `PowerUp` - Collectible power-ups

**Key Features**:
- Sprite-based entities
- Collision detection ready
- Progressive difficulty scaling
- Mouse and keyboard controls

**Dependencies**: constants.py, assets.py

---

### game.py (280 lines)
**Purpose**: Core game logic and state management
**Class**: `Game`

**Key Methods**:
- `__init__()` - Initialize game window and state
- `reset_game(level)` - Reset for new level
- `spawn_enemy()` - Spawn enemy ships
- `spawn_boss(is_final)` - Spawn boss
- `next_level()` - Progress to next level
- `handle_window_resize(w, h)` - Handle window resize
- `handle_events()` - Process input events
- `update()` - Update game state
- `draw()` - Render game

**Manages**:
- Game state (score, level, time)
- Sprite groups
- Collision detection
- Progression system
- Window responsiveness

**Dependencies**: constants.py, assets.py, entities.py

---

### ui.py (380 lines)
**Purpose**: UI screens and menus
**Class**: `UI`

**Key Methods**:
- `show_splash_screen()` - Animated title screen
- `show_message(msg, submsg, restart)` - Message screens
- `wait_for_key(allow_restart)` - Wait for input
- `show_level_map()` - Level selection screen
- `select_ship()` - Ship selection screen

**Features**:
- Responsive to window resize
- Mouse and keyboard support
- Animated transitions
- Visual feedback

**Dependencies**: constants.py, assets.py

---

## Data Flow

```
main.py
  ↓
  ├─→ Initialize pygame
  ├─→ Load assets (assets.py)
  ├─→ Create Game instance (game.py)
  ├─→ Create UI instance (ui.py)
  └─→ Main Loop:
       ├─→ UI: Show level map
       ├─→ UI: Select ship
       ├─→ Game: Reset for level
       ├─→ UI: Show start message
       └─→ Game Loop:
            ├─→ Game: Handle events
            ├─→ Game: Update (entities.py)
            ├─→ Game: Draw
            └─→ UI: Show result messages
```

## Benefits of Modular Structure

### 1. Maintainability
- Each module has a single responsibility
- Easy to locate and fix bugs
- Clear separation of concerns

### 2. Readability
- Smaller files are easier to understand
- Logical grouping of related code
- Clear dependencies

### 3. Reusability
- Entities can be reused in other projects
- Asset loading is independent
- UI components are modular

### 4. Testability
- Each module can be tested independently
- Mock dependencies easily
- Isolated unit tests

### 5. Scalability
- Easy to add new entities
- Simple to add new UI screens
- Straightforward to extend game logic

## Adding New Features

### Adding a New Enemy Type:
1. Add image to `enemy/` folder
2. Load in `assets.py` → `ENEMY_IMAGES`
3. Use in `entities.py` → `Enemy.__init__()`

### Adding a New Level:
1. Add background to `images/` folder
2. Load in `assets.py` → `BACKGROUNDS`
3. Update level count in `game.py` → `next_level()`

### Adding a New Power-Up:
1. Add to `entities.py` → `PowerUpType` enum
2. Add visual in `entities.py` → `PowerUp.__init__()`
3. Add effect in `entities.py` → `Player.activate_power_up()`

### Adding a New UI Screen:
1. Add method to `ui.py` → `UI` class
2. Call from `main.py` main loop
3. Handle window resize events

## Code Metrics

### Before Refactoring:
- **1 file**: main.py (1490 lines)
- **Complexity**: High
- **Maintainability**: Difficult

### After Refactoring:
- **6 files**: 
  - main.py (130 lines)
  - constants.py (20 lines)
  - assets.py (110 lines)
  - entities.py (350 lines)
  - game.py (280 lines)
  - ui.py (380 lines)
- **Total**: ~1270 lines (220 lines saved through better organization)
- **Complexity**: Low per module
- **Maintainability**: Easy

## Import Graph

```
main.py
  ├─→ constants.py
  ├─→ assets.py
  │    └─→ constants.py
  ├─→ entities.py
  │    ├─→ constants.py
  │    └─→ assets.py
  ├─→ game.py
  │    ├─→ constants.py
  │    ├─→ assets.py
  │    └─→ entities.py
  └─→ ui.py
       ├─→ constants.py
       └─→ assets.py
```

## Best Practices Followed

1. **Single Responsibility Principle**: Each module has one clear purpose
2. **DRY (Don't Repeat Yourself)**: Shared code in reusable modules
3. **Clear Naming**: Descriptive file and function names
4. **Documentation**: Docstrings for all classes and functions
5. **Separation of Concerns**: UI, logic, and data are separate
6. **Dependency Management**: Clear import hierarchy

## Future Improvements

Potential enhancements to the structure:
- Add `config.py` for user settings
- Create `utils.py` for helper functions
- Add `levels.py` for level definitions
- Create `audio.py` separate from assets
- Add `particles.py` for visual effects
- Create `ai.py` for enemy AI logic

## Backward Compatibility

The old monolithic `main.py` has been saved as `main_old.py` for reference.
The new modular version maintains 100% feature parity.
