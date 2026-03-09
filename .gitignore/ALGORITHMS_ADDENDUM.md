# Game Algorithms - Addendum to Comprehensive Report

## Overview

This document provides detailed algorithms and logic flows for all major systems in Space Fighters. It complements the **COMPREHENSIVE_GAME_REPORT.md** by providing step-by-step algorithmic breakdowns.

## Document Reference

**Full Algorithms Document**: `GAME_ALGORITHMS.md`

This addendum serves as a bridge between the comprehensive report and the detailed algorithms document.

---

## Algorithm Categories

### 1. Main Game Loop Algorithm
**Location**: GAME_ALGORITHMS.md - Section 1

**Purpose**: Controls the overall game flow from startup to shutdown

**Key Components**:
- Pygame initialization
- Splash screen display
- Main menu loop
- Level selection and gameplay
- Save/load integration
- Quit handling

**Complexity**: O(n) where n is game session duration

---

### 2. Level Gameplay Algorithm
**Location**: GAME_ALGORITHMS.md - Section 2

**Purpose**: Manages individual level gameplay at 60 FPS

**Key Components**:
- Event handling (keyboard, mouse, window)
- Pause menu integration
- Game state updates
- Collision detection
- Enemy spawning
- Boss battle transitions
- Win/lose condition checking

**Complexity**: O(n×m) where n is sprites, m is collision checks per frame

**Frame Rate**: 60 FPS (16.67ms per frame)

---

### 3. Collision Detection Algorithm
**Location**: GAME_ALGORITHMS.md - Section 3

**Purpose**: Detects and handles all entity collisions

**Method**: AABB (Axis-Aligned Bounding Box)

**Collision Pairs**:
- Player bullets ↔ Enemies
- Player bullets ↔ Boss
- Player bullets ↔ Asteroids
- Enemy bullets ↔ Player
- Enemies ↔ Player
- Asteroids ↔ Player
- Power-ups ↔ Player

**Optimization**: Sprite grouping, early exit, spatial partitioning

**Complexity**: O(n×m) optimized with grouping

---

### 4. Enemy Spawning Algorithm
**Location**: GAME_ALGORITHMS.md - Section 4

**Purpose**: Controls enemy and asteroid spawning

**Regular Levels**:
- Spawn delay: 40 frames (0.67 seconds)
- Max concurrent: 5 + level
- Position: Random top of screen
- Type: 4 variants per level

**Bonus Mission**:
- Spawn delay: 20 frames (0.33 seconds)
- Max concurrent: 10 asteroids
- Faster spawn rate for action

**Complexity**: O(1) per spawn check

---

### 5. Boss Battle Algorithm
**Location**: GAME_ALGORITHMS.md - Section 5

**Purpose**: Manages boss behavior and combat

**Boss Phases**:
1. Entry (descend from top)
2. Horizontal movement (back and forth)
3. Shooting patterns (1, 3, or 5 bullets)
4. Defeat (explosion and rewards)

**Movement Pattern**: Sinusoidal horizontal with edge reversal

**Shooting Patterns**:
- Level 1-2: Single bullet
- Level 3-4: Triple spread
- Level 5: Five-bullet pattern

**Complexity**: O(1) per frame update

---

### 6. Power-Up System Algorithm
**Location**: GAME_ALGORITHMS.md - Section 6

**Purpose**: Manages power-up drops and effects

**Drop System**:
- Regular: 20% chance on enemy kill
- Bonus: 40% chance on asteroid destroy
- Random type selection

**Power-Up Types**:
1. **Bullet Power**: Increases bullet level (+1, max 3)
2. **Health**: Restores 30 HP
3. **Shield**: 5-second invincibility + 20 HP

**Timer System**: 300 frames (5 seconds) for active effects

**Complexity**: O(1) per power-up check

---

### 7. Bullet System Algorithm
**Location**: GAME_ALGORITHMS.md - Section 7

**Purpose**: Controls bullet creation and behavior

**Shooting Patterns**:
- Level 0: Single (1 bullet)
- Level 1: Double (2 bullets)
- Level 2: Triple spread (3 bullets)
- Level 3: Quad (4 bullets)

**Bullet Properties**:
- Speed: -10 pixels/frame (player), +5 (enemy)
- Damage: 1 + bullet_level
- Offset: For spread patterns

**Ship-Specific**:
- Ship 1: 250ms delay, ship_shoot.wav
- Ship 2: 250ms delay, player_shoot.wav
- Blue Ship: 200ms delay, laser_shooting.wav

**Complexity**: O(n) where n is active bullets

---

### 8. Player Movement Algorithm
**Location**: GAME_ALGORITHMS.md - Section 8

**Purpose**: Handles player ship movement

**Input Methods**:
1. **Keyboard**: WASD or Arrow keys (5 pixels/frame)
2. **Mouse**: Right/Middle button drag (10 pixels/frame max)

**Priority**: Keyboard overrides mouse

**Boundary Checking**: Clamps to screen dimensions

**Complexity**: O(1) per frame

---

### 9. Score Calculation Algorithm
**Location**: GAME_ALGORITHMS.md - Section 9

**Purpose**: Tracks and calculates player score

**Point Values**:
- Enemy kill: 10 × level
- Boss kill: 500
- Asteroid destroy: 20
- Power-up collect: 50

**Formula Examples**:
```
Level 1 Total = (15 × 10) + 500 + (3 × 50) = 800
Level 5 Total = (55 × 50) + 500 + (11 × 50) = 3,800
Bonus Total = (30 × 20) + (12 × 50) = 1,200
```

**Complexity**: O(1) per scoring event

---

### 10. Save/Load Algorithm
**Location**: GAME_ALGORITHMS.md - Section 10

**Purpose**: Persists game progress

**Save Format**: JSON

**Saved Data**:
- Progress (levels, ships, bonus)
- Player state (health, bullet power)
- Audio settings (volumes, mutes)

**Triggers**:
- Level complete
- Bonus complete
- Settings change
- Game quit

**Error Handling**: Graceful fallback to defaults

**Complexity**: O(1) for save/load operations

---

### 11. Audio Management Algorithm
**Location**: GAME_ALGORITHMS.md - Section 11

**Purpose**: Controls all audio playback

**Volume System**:
- Music: 0-100% (0.0-1.0 internally)
- Sound: 0-100% (0.0-1.0 internally)
- Independent mute controls

**Sound Categories**:
- Background music (looping)
- Ship shooting (per ship type)
- Enemy/boss shooting
- Explosions (2 types)
- Mission sounds (complete, victory, defeat)

**Update Frequency**: Real-time on settings change

**Complexity**: O(n) where n is number of sounds

---

### 12. UI Navigation Algorithm
**Location**: GAME_ALGORITHMS.md - Section 12

**Purpose**: Manages menu navigation

**Navigation Methods**:
- Arrow keys (up/down/left/right)
- Enter/Space (select)
- ESC (back)
- Mouse click (direct selection)

**Menu Types**:
- Main menu (3 options)
- Level map (5 levels)
- Ship selection (3 ships)
- Settings (6 options)
- Pause menu (4 options)

**Visual Feedback**: Yellow highlight, selection boxes

**Complexity**: O(n) where n is menu options

---

## Algorithm Integration

### How Algorithms Work Together

```
Main Loop
    ↓
Level Gameplay ←→ Collision Detection
    ↓                    ↓
Enemy Spawning      Power-Up System
    ↓                    ↓
Boss Battle         Bullet System
    ↓                    ↓
Score Calculation   Player Movement
    ↓                    ↓
Save/Load ←→ Audio Management ←→ UI Navigation
```

### Data Flow

```
User Input → Event Handling → Game State Update → 
Collision Detection → Score Update → Audio Feedback → 
Visual Rendering → Save Progress
```

### Performance Considerations

**Frame Budget**: 16.67ms per frame (60 FPS)

**Time Allocation**:
- Event handling: ~1ms
- Game state update: ~5ms
- Collision detection: ~3ms
- Rendering: ~5ms
- Audio: ~1ms
- Overhead: ~1.67ms

**Optimization Techniques**:
1. Sprite grouping for efficient collision checks
2. Early exit on collision detection
3. Limit concurrent entities
4. Efficient rendering with dirty rectangles
5. Cached calculations where possible

---

## Algorithm Complexity Summary

| Algorithm | Time Complexity | Space Complexity |
|-----------|----------------|------------------|
| Main Loop | O(n) | O(1) |
| Level Gameplay | O(n×m) | O(n) |
| Collision Detection | O(n×m) | O(1) |
| Enemy Spawning | O(1) | O(n) |
| Boss Battle | O(1) | O(1) |
| Power-Up System | O(1) | O(n) |
| Bullet System | O(n) | O(n) |
| Player Movement | O(1) | O(1) |
| Score Calculation | O(1) | O(1) |
| Save/Load | O(1) | O(1) |
| Audio Management | O(n) | O(n) |
| UI Navigation | O(n) | O(1) |

**Legend**:
- n = number of entities/sprites
- m = number of collision checks

---

## Pseudocode Conventions

Throughout the algorithms document, the following conventions are used:

**Control Structures**:
```
IF condition THEN
    action
ELSE
    alternative
END IF

WHILE condition DO
    action
END WHILE

FOR each item in collection
    action
END FOR
```

**Functions**:
```
FUNCTION name(parameters)
    actions
    RETURN value
END FUNCTION
```

**Comments**:
```
// Single line comment
/* Multi-line
   comment */
```

---

## Testing Algorithms

### Unit Testing Approach

Each algorithm can be tested independently:

1. **Main Loop**: Test state transitions
2. **Collision Detection**: Test all collision pairs
3. **Spawning**: Test spawn rates and limits
4. **Boss Battle**: Test movement and shooting
5. **Power-Ups**: Test drop rates and effects
6. **Bullets**: Test patterns and damage
7. **Movement**: Test boundary checking
8. **Score**: Test calculation formulas
9. **Save/Load**: Test data persistence
10. **Audio**: Test volume and mute
11. **UI**: Test navigation paths

### Integration Testing

Test algorithm interactions:
- Collision → Score → Audio
- Spawning → Collision → Power-Up
- Movement → Collision → Damage
- Save → Load → Verify

---

## Future Algorithm Enhancements

Potential improvements:

1. **AI Enhancement**: More sophisticated enemy patterns
2. **Pathfinding**: Smart enemy movement
3. **Particle Systems**: Better visual effects
4. **Network Code**: Multiplayer support
5. **Procedural Generation**: Random level layouts
6. **Achievement System**: Track player accomplishments
7. **Replay System**: Record and playback gameplay

---

## Conclusion

The algorithms in Space Fighters are designed to be:

✓ **Efficient**: Optimized for 60 FPS
✓ **Maintainable**: Clear and documented
✓ **Scalable**: Easy to extend
✓ **Robust**: Error handling included
✓ **Testable**: Modular design

For complete algorithmic details with flowcharts and pseudocode, refer to **GAME_ALGORITHMS.md**.

---

**Document Version**: 1.0
**Related Documents**: 
- COMPREHENSIVE_GAME_REPORT.md
- GAME_ALGORITHMS.md
- README.md
