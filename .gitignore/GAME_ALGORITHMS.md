# Space Fighters - Game Algorithms & Logic Flow

## Table of Contents
1. [Main Game Loop Algorithm](#main-game-loop-algorithm)
2. [Level Gameplay Algorithm](#level-gameplay-algorithm)
3. [Collision Detection Algorithm](#collision-detection-algorithm)
4. [Enemy Spawning Algorithm](#enemy-spawning-algorithm)
5. [Boss Battle Algorithm](#boss-battle-algorithm)
6. [Power-Up System Algorithm](#power-up-system-algorithm)
7. [Bullet System Algorithm](#bullet-system-algorithm)
8. [Player Movement Algorithm](#player-movement-algorithm)
9. [Score Calculation Algorithm](#score-calculation-algorithm)
10. [Save/Load Algorithm](#saveload-algorithm)
11. [Audio Management Algorithm](#audio-management-algorithm)
12. [UI Navigation Algorithm](#ui-navigation-algorithm)

---

## Main Game Loop Algorithm

### High-Level Flow
```
START
│
├─ Initialize Pygame
├─ Initialize Audio System
├─ Load Saved Progress
│
├─ SHOW SPLASH SCREEN
│   ├─ Display animated title
│   ├─ Wait 3 seconds or key press
│   └─ Fade in/out effects
│
└─ MAIN GAME LOOP (while running)
    │
    ├─ SHOW MAIN MENU
    │   ├─ Display options: Play, Settings, Quit
    │   ├─ Handle user selection
    │   └─ Branch based on choice
    │
    ├─ IF Settings Selected
    │   ├─ Show settings menu
    │   ├─ Adjust volumes
    │   ├─ Save settings
    │   └─ Return to main menu
    │
    ├─ IF Play Selected
    │   │
    │   ├─ SHOW LEVEL MAP
    │   │   ├─ Display all 5 levels
    │   │   ├─ Show completion status
    │   │   ├─ Allow level selection
    │   │   └─ Return selected level
    │   │
    │   ├─ CHECK BONUS MISSION
    │   │   ├─ IF Level 4 complete AND bonus not done
    │   │   │   ├─ Show bonus prompt
    │   │   │   ├─ IF user accepts
    │   │   │   │   ├─ Play bonus mission
    │   │   │   │   └─ Mark as completed
    │   │   │   └─ ELSE skip
    │   │   └─ Continue
    │   │
    │   ├─ SHOW SHIP SELECTION
    │   │   ├─ Display available ships
    │   │   ├─ Show locked ships
    │   │   ├─ Allow ship selection
    │   │   └─ Return selected ship
    │   │
    │   ├─ RESET GAME STATE
    │   │   ├─ Set level number
    │   │   ├─ Reset score to 0
    │   │   ├─ Create player with saved stats
    │   │   ├─ Clear all sprite groups
    │   │   └─ Set time limit
    │   │
    │   ├─ SHOW START MESSAGE
    │   │   ├─ Display "LEVEL X"
    │   │   ├─ Wait for SPACE key
    │   │   └─ Begin level
    │   │
    │   ├─ PLAY LEVEL (see Level Gameplay Algorithm)
    │   │
    │   ├─ HANDLE LEVEL RESULT
    │   │   ├─ IF boss defeated
    │   │   │   ├─ Show victory message
    │   │   │   ├─ Unlock next level/ship
    │   │   │   ├─ Save progress
    │   │   │   └─ Return to level map
    │   │   │
    │   │   ├─ IF final boss defeated
    │   │   │   ├─ Show victory screen
    │   │   │   ├─ Offer restart option
    │   │   │   └─ IF restart: reset all progress
    │   │   │
    │   │   ├─ IF time up
    │   │   │   ├─ Show time up message
    │   │   │   └─ Return to level map
    │   │   │
    │   │   └─ IF game over
    │   │       ├─ Show game over message
    │   │       ├─ Offer restart option
    │   │       └─ Return to level map
    │   │
    │   └─ LOOP back to level map
    │
    └─ IF Quit Selected
        ├─ Save progress
        └─ EXIT
```

### Pseudocode
```python
def main():
    initialize_pygame()
    initialize_audio()
    
    game = Game()  # Loads saved progress
    ui = UI(game)
    settings_menu = SettingsMenu(game)
    
    if not show_splash_screen():
        quit()
    
    running = True
    while running:
        menu_choice = show_main_menu()
        
        if menu_choice == "quit":
            save_progress()
            quit()
        
        elif menu_choice == "settings":
            settings_menu.show_settings()
            continue
        
        elif menu_choice == "play":
            selected_level = show_level_map()
            if selected_level is None:
                continue
            
            # Check for bonus mission
            if should_show_bonus_mission():
                if user_accepts_bonus():
                    play_bonus_mission()
                    continue
            
            selected_ship = show_ship_selection()
            if selected_ship is None:
                continue
            
            reset_game(selected_level, selected_ship)
            show_start_message()
            
            result = play_level()
            handle_level_result(result)
    
    save_progress()
    quit()
```


---

## Level Gameplay Algorithm

### Core Game Loop
```
LEVEL START
│
├─ Initialize level variables
│   ├─ enemies_destroyed = 0
│   ├─ enemies_needed = 15 + (level - 1) × 10
│   ├─ time_limit = 90 seconds
│   ├─ start_time = current_time
│   ├─ boss_active = False
│   └─ spawn_timer = 0
│
└─ GAME LOOP (60 FPS)
    │
    ├─ HANDLE EVENTS
    │   ├─ Check for quit
    │   ├─ Check for pause (ESC/P)
    │   ├─ Check for window resize
    │   ├─ Handle keyboard input (WASD/Arrows)
    │   └─ Handle mouse input (click/drag)
    │
    ├─ IF PAUSED
    │   ├─ Show pause menu
    │   ├─ Wait for resume/settings/quit
    │   └─ Continue or exit
    │
    ├─ UPDATE GAME STATE
    │   │
    │   ├─ Update player position
    │   ├─ Update all bullets
    │   ├─ Update power-ups
    │   │
    │   ├─ IF boss_active
    │   │   ├─ Update boss position
    │   │   ├─ Boss shoots bullets
    │   │   ├─ Check bullet-boss collisions
    │   │   └─ IF boss health <= 0
    │   │       ├─ Play explosion
    │   │       ├─ Add score
    │   │       └─ RETURN "boss_defeated"
    │   │
    │   ├─ ELSE (enemy phase)
    │   │   ├─ Update all enemies
    │   │   ├─ Enemies shoot bullets
    │   │   │
    │   │   ├─ SPAWN ENEMIES
    │   │   │   ├─ spawn_timer++
    │   │   │   ├─ IF spawn_timer >= spawn_delay
    │   │   │   │   ├─ IF enemy_count < max_enemies
    │   │   │   │   │   ├─ Create new enemy
    │   │   │   │   │   └─ spawn_timer = 0
    │   │   │   │   └─ ENDIF
    │   │   │   └─ ENDIF
    │   │   │
    │   │   ├─ CHECK BULLET COLLISIONS
    │   │   │   ├─ FOR each player bullet
    │   │   │   │   ├─ Check collision with enemies
    │   │   │   │   ├─ IF hit
    │   │   │   │   │   ├─ Reduce enemy health
    │   │   │   │   │   ├─ IF enemy health <= 0
    │   │   │   │   │   │   ├─ Kill enemy
    │   │   │   │   │   │   ├─ Play explosion
    │   │   │   │   │   │   ├─ Add score
    │   │   │   │   │   │   ├─ enemies_destroyed++
    │   │   │   │   │   │   └─ Maybe spawn power-up (20%)
    │   │   │   │   │   └─ ENDIF
    │   │   │   │   └─ ENDIF
    │   │   │   └─ ENDFOR
    │   │   │
    │   │   └─ CHECK BOSS SPAWN
    │   │       ├─ IF enemies_destroyed >= enemies_needed
    │   │       │   ├─ Clear remaining enemies
    │   │       │   ├─ Spawn boss
    │   │       │   └─ boss_active = True
    │   │       └─ ENDIF
    │   │
    │   ├─ CHECK ENEMY BULLET COLLISIONS
    │   │   ├─ FOR each enemy bullet
    │   │   │   ├─ IF collides with player
    │   │   │   │   ├─ IF not shielded
    │   │   │   │   │   ├─ player.take_damage(10)
    │   │   │   │   │   └─ Reduce bullet power
    │   │   │   │   └─ ENDIF
    │   │   │   │   └─ Remove bullet
    │   │   │   └─ ENDIF
    │   │   └─ ENDFOR
    │   │
    │   ├─ CHECK ENEMY COLLISIONS
    │   │   ├─ FOR each enemy
    │   │   │   ├─ IF collides with player
    │   │   │   │   ├─ IF not shielded
    │   │   │   │   │   ├─ player.take_damage(20)
    │   │   │   │   │   └─ Reduce bullet power
    │   │   │   │   └─ ENDIF
    │   │   │   │   └─ Kill enemy
    │   │   │   └─ ENDIF
    │   │   └─ ENDFOR
    │   │
    │   ├─ CHECK POWER-UP COLLISIONS
    │   │   ├─ FOR each power-up
    │   │   │   ├─ IF collides with player
    │   │   │   │   ├─ Activate power-up effect
    │   │   │   │   ├─ Add score (50 points)
    │   │   │   │   └─ Remove power-up
    │   │   │   └─ ENDIF
    │   │   └─ ENDFOR
    │   │
    │   ├─ CHECK TIME LIMIT
    │   │   ├─ elapsed_time = (current_time - start_time) / 1000
    │   │   ├─ remaining_time = time_limit - elapsed_time
    │   │   ├─ IF remaining_time <= 0 AND not boss_active
    │   │   │   └─ RETURN "time_up"
    │   │   └─ ENDIF
    │   │
    │   └─ CHECK PLAYER HEALTH
    │       ├─ IF player.health <= 0
    │       │   ├─ Play death animation
    │       │   ├─ Play game over sound
    │       │   └─ RETURN "game_over"
    │       └─ ENDIF
    │
    ├─ DRAW EVERYTHING
    │   ├─ Draw background
    │   ├─ Draw planet (if regular level)
    │   ├─ Draw all sprites
    │   ├─ Draw HUD
    │   ├─ Draw health bar
    │   ├─ Draw boss health bar (if active)
    │   └─ Update display
    │
    └─ CONTROL FRAME RATE (60 FPS)
```

### Pseudocode
```python
def play_level(game, ui, settings_menu):
    level_running = True
    
    while level_running:
        clock.tick(60)  # 60 FPS
        
        # Handle events
        event_result = handle_events()
        if event_result == "quit":
            return "quit"
        elif event_result == "show_pause_menu":
            pause_result = show_pause_menu()
            if pause_result == "quit":
                return "quit"
            elif pause_result == "main_menu":
                return "continue"
            continue  # Resume
        
        # Update game state
        status = update_game_state()
        
        # Draw everything
        draw_game()
        
        # Check game status
        if status == "boss_defeated":
            show_victory_message()
            unlock_rewards()
            save_progress()
            return "continue"
        
        elif status == "final_boss_defeated":
            show_final_victory()
            offer_restart()
            return "continue"
        
        elif status == "time_up":
            show_time_up_message()
            return "continue"
        
        elif status == "game_over":
            show_game_over_message()
            offer_restart()
            return "continue"
```


---

## Collision Detection Algorithm

### Rectangle-Based Collision (AABB)
```
COLLISION DETECTION
│
├─ FOR each collision pair
│   │
│   ├─ Get rect1 (x1, y1, width1, height1)
│   ├─ Get rect2 (x2, y2, width2, height2)
│   │
│   ├─ CHECK OVERLAP
│   │   ├─ IF x1 < x2 + width2 AND
│   │   │    x1 + width1 > x2 AND
│   │   │    y1 < y2 + height2 AND
│   │   │    y1 + height1 > y2
│   │   │   └─ COLLISION DETECTED
│   │   └─ ELSE
│   │       └─ NO COLLISION
│   │
│   └─ IF collision detected
│       └─ Handle collision effects
│
└─ ENDFOR
```

### Player Bullets vs Enemies
```
FOR each bullet in player_bullets:
    hits = check_collision(bullet, enemies_group)
    
    IF hits:
        bullet.kill()
        
        FOR each enemy in hits:
            enemy.health -= bullet.damage
            
            IF enemy.health <= 0:
                enemy.start_explosion()
                play_sound(EXPLOSION_1)
                score += 10 × level
                enemies_destroyed += 1
                
                IF random() < 0.2:  # 20% chance
                    spawn_power_up(enemy.position)
```

### Enemy Bullets vs Player
```
hits = check_collision(player, enemy_bullets_group, remove=True)

IF hits AND not player.shield_active:
    damage = len(hits) × 10
    player.take_damage(damage)
    
    IF damage >= 10:
        player.bullet_level = max(0, player.bullet_level - 1)
```

### Enemies vs Player
```
hits = check_collision(player, enemies_group, remove=False)

IF hits AND not player.shield_active:
    FOR each enemy in hits:
        enemy.start_explosion()
        player.take_damage(20)
        player.bullet_level = max(0, player.bullet_level - 1)
```

### Power-Ups vs Player
```
hits = check_collision(player, power_ups_group, remove=True)

FOR each power_up in hits:
    player.activate_power_up(power_up.type)
    score += 50
```

### Optimization Techniques
```
1. Spatial Partitioning
   - Only check nearby objects
   - Use sprite groups for categorization
   
2. Early Exit
   - Remove dead sprites immediately
   - Skip checks for inactive objects
   
3. Limit Checks
   - Only check relevant pairs
   - Don't check bullet vs bullet
   
4. Bounding Box
   - Use simple rectangles
   - More complex shapes only if needed
```

---

## Enemy Spawning Algorithm

### Regular Level Spawning
```
ENEMY SPAWNING
│
├─ INITIALIZE
│   ├─ spawn_timer = 0
│   ├─ spawn_delay = 40 frames (0.67 seconds)
│   ├─ max_concurrent = 5 + level
│   └─ enemies_needed = 15 + (level - 1) × 10
│
└─ EACH FRAME
    │
    ├─ spawn_timer++
    │
    ├─ IF spawn_timer >= spawn_delay
    │   │
    │   ├─ IF current_enemy_count < max_concurrent
    │   │   │
    │   │   ├─ GENERATE POSITION
    │   │   │   ├─ x = random(40, screen_width - 40)
    │   │   │   └─ y = random(-100, -40)
    │   │   │
    │   │   ├─ SELECT ENEMY TYPE
    │   │   │   └─ type = random(0, 3)  # 4 variants
    │   │   │
    │   │   ├─ CREATE ENEMY
    │   │   │   ├─ enemy = Enemy(x, y, level, type)
    │   │   │   ├─ Set enemy properties based on level
    │   │   │   │   ├─ speed = 1 + level × 0.3
    │   │   │   │   ├─ health = 1 + level ÷ 2
    │   │   │   │   └─ shoot_delay = max(1500 - level × 100, 800)
    │   │   │   └─ Add to enemies group
    │   │   │
    │   │   └─ spawn_timer = 0
    │   │
    │   └─ ENDIF
    │
    └─ ENDIF
```

### Bonus Mission Spawning (Asteroids)
```
ASTEROID SPAWNING
│
├─ INITIALIZE
│   ├─ spawn_timer = 0
│   ├─ spawn_delay = 20 frames (0.33 seconds)
│   └─ max_concurrent = 10
│
└─ EACH FRAME
    │
    ├─ spawn_timer++
    │
    ├─ IF spawn_timer >= spawn_delay
    │   │
    │   ├─ IF current_asteroid_count < max_concurrent
    │   │   │
    │   │   ├─ GENERATE POSITION
    │   │   │   ├─ x = random(40, screen_width - 40)
    │   │   │   └─ y = random(-100, -40)
    │   │   │
    │   │   ├─ CREATE ASTEROID
    │   │   │   ├─ asteroid = Asteroid(x, y)
    │   │   │   ├─ speed = random(2.0, 5.0)
    │   │   │   ├─ rotation_speed = random(-5, 5)
    │   │   │   ├─ health = 2
    │   │   │   └─ Add to asteroids group
    │   │   │
    │   │   └─ spawn_timer = 0
    │   │
    │   └─ ENDIF
    │
    └─ ENDIF
```

### Spawn Rate Calculation
```
Regular Level:
- Spawn delay: 40 frames
- At 60 FPS: 40/60 = 0.67 seconds per spawn
- Per minute: 60/0.67 ≈ 90 spawns
- 90 seconds: ~134 potential spawns
- Limited by max concurrent (5 + level)

Bonus Mission:
- Spawn delay: 20 frames
- At 60 FPS: 20/60 = 0.33 seconds per spawn
- Per minute: 60/0.33 ≈ 180 spawns
- 60 seconds: ~180 potential spawns
- Limited by max concurrent (10)
```

---

## Boss Battle Algorithm

### Boss Spawn Trigger
```
CHECK BOSS SPAWN
│
├─ IF enemies_destroyed >= enemies_needed
│   │
│   ├─ CLEAR REMAINING ENEMIES
│   │   └─ FOR each enemy: enemy.kill()
│   │
│   ├─ CREATE BOSS
│   │   ├─ boss = Boss(level)
│   │   ├─ boss.position = (screen_width/2, -100)
│   │   ├─ boss.health = 30 + level × 10
│   │   ├─ boss.shoot_delay = 500 if level==5 else 800
│   │   └─ Add to sprites
│   │
│   └─ boss_active = True
│
└─ ENDIF
```

### Boss Movement Pattern
```
BOSS UPDATE (each frame)
│
├─ IF moving_down AND y < 50
│   ├─ y += speed (1 pixel/frame)
│   └─ Continue descent
│
├─ ELSE
│   ├─ moving_down = False
│   ├─ x += speed × 2 × direction
│   │
│   ├─ IF x >= screen_width OR x <= 0
│   │   └─ direction *= -1  # Reverse
│   │
│   └─ Move horizontally
│
└─ ENDIF
```

### Boss Shooting Pattern
```
BOSS SHOOT
│
├─ current_time = get_time()
│
├─ IF current_time - last_shot > shoot_delay
│   │
│   ├─ last_shot = current_time
│   ├─ Play boss_shoot sound
│   │
│   ├─ CREATE BULLETS based on level
│   │   │
│   │   ├─ IF level == 5 (final boss)
│   │   │   ├─ Create 5 bullets
│   │   │   ├─ Positions: center, ±30, ±60
│   │   │   └─ Spread pattern
│   │   │
│   │   ├─ ELSE IF level >= 3
│   │   │   ├─ Create 3 bullets
│   │   │   ├─ Positions: center, ±30
│   │   │   └─ Triple shot
│   │   │
│   │   └─ ELSE
│   │       ├─ Create 1 bullet
│   │       └─ Single shot
│   │
│   └─ Add bullets to enemy_bullets group
│
└─ ENDIF
```

### Boss Defeat
```
CHECK BOSS DEFEAT
│
├─ FOR each player bullet
│   │
│   ├─ IF collides with boss
│   │   │
│   │   ├─ bullet.kill()
│   │   ├─ boss.health -= bullet.damage
│   │   │
│   │   ├─ IF boss.health <= 0
│   │   │   │
│   │   │   ├─ boss.start_explosion()
│   │   │   ├─ Play explosion_2 sound
│   │   │   ├─ boss_active = False
│   │   │   ├─ score += 500
│   │   │   │
│   │   │   ├─ IF level == 5
│   │   │   │   ├─ Play Win.mp3
│   │   │   │   └─ RETURN "final_boss_defeated"
│   │   │   │
│   │   │   └─ ELSE
│   │   │       ├─ Play mission_complete.wav
│   │   │       └─ RETURN "boss_defeated"
│   │   │
│   │   └─ ENDIF
│   │
│   └─ ENDIF
│
└─ ENDFOR
```


---

## Power-Up System Algorithm

### Power-Up Drop
```
POWER-UP DROP
│
├─ WHEN enemy killed
│   │
│   ├─ roll = random(0, 1)
│   │
│   ├─ drop_rate = 0.4 if bonus_mission else 0.2
│   │
│   ├─ IF roll < drop_rate
│   │   │
│   │   ├─ SELECT TYPE
│   │   │   └─ type = random_choice([BULLET_POWER, HEALTH, SHIELD])
│   │   │
│   │   ├─ CREATE POWER-UP
│   │   │   ├─ power_up = PowerUp(enemy.x, enemy.y)
│   │   │   ├─ power_up.type = type
│   │   │   ├─ power_up.speed = 2
│   │   │   └─ Add to power_ups group
│   │   │
│   │   └─ ENDIF
│   │
│   └─ ENDIF
│
└─ END
```

### Power-Up Collection
```
POWER-UP COLLECTION
│
├─ hits = check_collision(player, power_ups, remove=True)
│
├─ FOR each power_up in hits
│   │
│   ├─ score += 50
│   │
│   ├─ ACTIVATE EFFECT based on type
│   │   │
│   │   ├─ IF BULLET_POWER
│   │   │   ├─ player.bullet_level = min(player.bullet_level + 1, 3)
│   │   │   ├─ player.power_up = BULLET_POWER
│   │   │   └─ player.power_up_timer = 300 frames
│   │   │
│   │   ├─ ELSE IF HEALTH
│   │   │   ├─ player.health = min(player.health + 30, 100)
│   │   │   ├─ player.power_up = HEALTH
│   │   │   └─ player.power_up_timer = 300 frames
│   │   │
│   │   └─ ELSE IF SHIELD
│   │       ├─ player.shield_active = True
│   │       ├─ player.health = min(player.health + 20, 100)
│   │       ├─ player.power_up = SHIELD
│   │       └─ player.power_up_timer = 300 frames
│   │
│   └─ ENDFOR
│
└─ END
```

### Power-Up Timer Update
```
POWER-UP TIMER UPDATE (each frame)
│
├─ IF player.power_up_timer > 0
│   │
│   ├─ player.power_up_timer -= 1
│   │
│   ├─ IF player.power_up_timer <= 0
│   │   │
│   │   ├─ player.power_up = None
│   │   │
│   │   ├─ IF was SHIELD
│   │   │   └─ player.shield_active = False
│   │   │
│   │   └─ ENDIF
│   │
│   └─ ENDIF
│
└─ ENDIF
```

### Bullet Power Loss on Damage
```
DAMAGE TAKEN
│
├─ player.health -= damage
│
├─ IF damage >= 10 AND not shield_active
│   │
│   ├─ player.bullet_level = max(0, player.bullet_level - 1)
│   │
│   └─ Update bullet pattern
│
└─ ENDIF
```

---

## Bullet System Algorithm

### Player Shooting
```
PLAYER SHOOT
│
├─ current_time = get_time()
│
├─ IF current_time - last_shot > shoot_delay
│   │
│   ├─ last_shot = current_time
│   ├─ bullets = []
│   │
│   ├─ PLAY SOUND based on ship
│   │   ├─ IF ship == 0: play ship_shoot.wav
│   │   ├─ IF ship == 1: play player_shoot.wav
│   │   └─ IF ship == 2: play laser_shooting.wav
│   │
│   ├─ CREATE BULLETS based on bullet_level
│   │   │
│   │   ├─ IF bullet_level == 3  # Quad shot
│   │   │   ├─ bullets.add(Bullet(center_x, top, 0, 3, ship))
│   │   │   ├─ bullets.add(Bullet(center_x - 20, top, -1, 3, ship))
│   │   │   ├─ bullets.add(Bullet(center_x + 20, top, 1, 3, ship))
│   │   │   └─ bullets.add(Bullet(center_x, top - 10, 0, 3, ship))
│   │   │
│   │   ├─ ELSE IF bullet_level == 2  # Triple spread
│   │   │   ├─ bullets.add(Bullet(center_x, top, 0, 2, ship))
│   │   │   ├─ bullets.add(Bullet(center_x - 15, top, -2, 2, ship))
│   │   │   └─ bullets.add(Bullet(center_x + 15, top, 2, 2, ship))
│   │   │
│   │   ├─ ELSE IF bullet_level == 1  # Double shot
│   │   │   ├─ bullets.add(Bullet(center_x - 10, top, 0, 1, ship))
│   │   │   └─ bullets.add(Bullet(center_x + 10, top, 0, 1, ship))
│   │   │
│   │   └─ ELSE  # Single shot
│   │       └─ bullets.add(Bullet(center_x, top, 0, 0, ship))
│   │
│   └─ RETURN bullets
│
└─ ELSE
    └─ RETURN []
```

### Bullet Update
```
BULLET UPDATE (each frame)
│
├─ FOR each bullet
│   │
│   ├─ UPDATE POSITION
│   │   ├─ y += speed  # -10 for player, +5 for enemy
│   │   └─ x += offset_x  # For spread patterns
│   │
│   ├─ CHECK BOUNDS
│   │   ├─ IF y < -50 OR y > screen_height + 50
│   │   │   └─ bullet.kill()
│   │   └─ ENDIF
│   │
│   └─ ENDFOR
│
└─ END
```

### Bullet Properties
```
BULLET CREATION
│
├─ Bullet(x, y, offset_x, bullet_level, ship_choice)
│   │
│   ├─ SET IMAGE
│   │   ├─ IF ship_choice == 2  # Blue ship
│   │   │   └─ image = blue_laser.png
│   │   └─ ELSE
│   │       └─ image = bullet_[level+1].png
│   │
│   ├─ SET PROPERTIES
│   │   ├─ speed = -10  # Upward
│   │   ├─ damage = 1 + bullet_level
│   │   └─ offset_x = offset_x
│   │
│   └─ POSITION
│       ├─ rect.centerx = x
│       └─ rect.bottom = y
│
└─ END
```

---

## Player Movement Algorithm

### Keyboard Movement
```
KEYBOARD MOVEMENT (each frame)
│
├─ keys = get_pressed_keys()
│
├─ IF keys[LEFT] OR keys[A]
│   └─ player.x -= speed
│
├─ IF keys[RIGHT] OR keys[D]
│   └─ player.x += speed
│
├─ IF keys[UP] OR keys[W]
│   └─ player.y -= speed
│
├─ IF keys[DOWN] OR keys[S]
│   └─ player.y += speed
│
├─ CLAMP TO SCREEN
│   ├─ player.x = clamp(player.x, 0, screen_width)
│   └─ player.y = clamp(player.y, 0, screen_height)
│
└─ END
```

### Mouse Movement
```
MOUSE MOVEMENT (each frame)
│
├─ mouse_buttons = get_mouse_buttons()
│
├─ IF mouse_buttons[RIGHT] OR mouse_buttons[MIDDLE]
│   │
│   ├─ mouse_pos = get_mouse_position()
│   ├─ target_x = mouse_pos.x
│   ├─ target_y = mouse_pos.y
│   │
│   ├─ CALCULATE DIRECTION
│   │   ├─ dx = target_x - player.x
│   │   ├─ dy = target_y - player.y
│   │   └─ distance = sqrt(dx² + dy²)
│   │
│   ├─ IF distance > 5
│   │   │
│   │   ├─ NORMALIZE AND MOVE
│   │   │   ├─ move_speed = min(speed × 2, distance)
│   │   │   ├─ player.x += (dx / distance) × move_speed
│   │   │   └─ player.y += (dy / distance) × move_speed
│   │   │
│   │   └─ ENDIF
│   │
│   └─ CLAMP TO SCREEN
│       ├─ player.x = clamp(player.x, 0, screen_width)
│       └─ player.y = clamp(player.y, 0, screen_height)
│
└─ ENDIF
```

### Combined Movement
```
MOVEMENT PRIORITY
│
├─ keyboard_moving = check_keyboard_input()
│
├─ IF keyboard_moving
│   └─ Use keyboard movement
│
├─ ELSE
│   └─ Check and use mouse movement
│
└─ END
```


---

## Score Calculation Algorithm

### Score Tracking
```
SCORE SYSTEM
│
├─ INITIALIZE
│   └─ score = 0
│
├─ ENEMY KILLED
│   ├─ points = 10 × current_level
│   └─ score += points
│
├─ BOSS KILLED
│   ├─ points = 500
│   └─ score += points
│
├─ ASTEROID DESTROYED
│   ├─ points = 20
│   └─ score += points
│
├─ POWER-UP COLLECTED
│   ├─ points = 50
│   └─ score += points
│
└─ DISPLAY
    └─ Update HUD with current score
```

### Score Calculation Examples
```
LEVEL 1 EXAMPLE
│
├─ 15 enemies × 10 points = 150
├─ 1 boss × 500 points = 500
├─ 3 power-ups × 50 points = 150
└─ Total: 800 points

LEVEL 5 EXAMPLE
│
├─ 55 enemies × 50 points = 2,750
├─ 1 boss × 500 points = 500
├─ 11 power-ups × 50 points = 550
└─ Total: 3,800 points

BONUS MISSION EXAMPLE
│
├─ 30 asteroids × 20 points = 600
├─ 12 power-ups × 50 points = 600
└─ Total: 1,200 points
```

---

## Save/Load Algorithm

### Save Process
```
SAVE GAME
│
├─ COLLECT DATA
│   ├─ data = {
│   │   'highest_level': highest_level_reached,
│   │   'completed_levels': [bool, bool, bool, bool, bool],
│   │   'unlocked_ships': [bool, bool, bool],
│   │   'bullet_power': player.bullet_level,
│   │   'player_health': player.health,
│   │   'bonus_completed': bonus_completed,
│   │   'music_volume': MUSIC_VOLUME,
│   │   'sound_volume': SOUND_VOLUME,
│   │   'music_muted': MUSIC_MUTED,
│   │   'sound_muted': SOUND_MUTED
│   │   }
│   │
│   └─ CONVERT TO JSON
│       └─ json_data = json.dumps(data, indent=4)
│
├─ WRITE TO FILE
│   ├─ TRY
│   │   ├─ open('game_save.json', 'w')
│   │   ├─ write(json_data)
│   │   ├─ close()
│   │   └─ RETURN success
│   │
│   └─ CATCH error
│       ├─ print(error)
│       └─ RETURN failure
│
└─ END
```

### Load Process
```
LOAD GAME
│
├─ CHECK FILE EXISTS
│   ├─ IF 'game_save.json' exists
│   │   │
│   │   ├─ TRY
│   │   │   ├─ open('game_save.json', 'r')
│   │   │   ├─ json_data = read()
│   │   │   ├─ data = json.parse(json_data)
│   │   │   ├─ close()
│   │   │   └─ RETURN data
│   │   │
│   │   └─ CATCH error
│   │       ├─ print(error)
│   │       └─ RETURN None
│   │
│   └─ ELSE
│       └─ RETURN None
│
├─ IF data is None
│   └─ data = get_default_progress()
│
├─ APPLY DATA TO GAME
│   ├─ highest_level_reached = data['highest_level']
│   ├─ completed_levels = data['completed_levels']
│   ├─ unlocked_ships = data['unlocked_ships']
│   ├─ saved_bullet_power = data['bullet_power']
│   ├─ saved_health = data['player_health']
│   ├─ bonus_completed = data['bonus_completed']
│   ├─ MUSIC_VOLUME = data['music_volume']
│   ├─ SOUND_VOLUME = data['sound_volume']
│   ├─ MUSIC_MUTED = data['music_muted']
│   └─ SOUND_MUTED = data['sound_muted']
│
└─ END
```

### Auto-Save Triggers
```
AUTO-SAVE TRIGGERS
│
├─ AFTER LEVEL COMPLETE
│   └─ save_progress()
│
├─ AFTER BONUS MISSION
│   └─ save_progress()
│
├─ SETTINGS MENU EXIT
│   └─ save_progress()
│
├─ GAME QUIT
│   └─ save_progress()
│
└─ GAME RESET
    └─ save_progress()
```

---

## Audio Management Algorithm

### Volume Control
```
VOLUME ADJUSTMENT
│
├─ WHEN LEFT key pressed
│   ├─ IF adjusting music
│   │   ├─ MUSIC_VOLUME = max(0.0, MUSIC_VOLUME - 0.1)
│   │   └─ update_sound_volumes()
│   │
│   └─ IF adjusting sound
│       ├─ SOUND_VOLUME = max(0.0, SOUND_VOLUME - 0.1)
│       └─ update_sound_volumes()
│
├─ WHEN RIGHT key pressed
│   ├─ IF adjusting music
│   │   ├─ MUSIC_VOLUME = min(1.0, MUSIC_VOLUME + 0.1)
│   │   └─ update_sound_volumes()
│   │
│   └─ IF adjusting sound
│       ├─ SOUND_VOLUME = min(1.0, SOUND_VOLUME + 0.1)
│       └─ update_sound_volumes()
│
└─ END
```

### Sound Volume Update
```
UPDATE SOUND VOLUMES
│
├─ FOR each sound effect
│   │
│   ├─ CALCULATE VOLUME
│   │   ├─ IF SOUND_MUTED
│   │   │   └─ volume = 0
│   │   └─ ELSE
│   │       └─ volume = base_volume × SOUND_VOLUME
│   │
│   └─ sound.set_volume(volume)
│
├─ UPDATE MUSIC
│   ├─ IF MUSIC_MUTED
│   │   └─ volume = 0
│   └─ ELSE
│       └─ volume = MUSIC_VOLUME
│   │
│   └─ BACKGROUND_SOUND.set_volume(volume)
│
└─ END
```

### Sound Playback
```
PLAY SOUND
│
├─ IF sound exists AND not SOUND_MUTED
│   │
│   ├─ CHECK SOUND TYPE
│   │   ├─ IF ship shooting
│   │   │   └─ Play appropriate ship sound
│   │   │
│   │   ├─ IF enemy/boss shooting
│   │   │   └─ Play boss_shoot.wav
│   │   │
│   │   ├─ IF enemy explosion
│   │   │   └─ Play explosion_1.wav
│   │   │
│   │   ├─ IF boss explosion
│   │   │   └─ Play explosion_2.wav
│   │   │
│   │   ├─ IF level complete
│   │   │   └─ Play mission_complete.wav
│   │   │
│   │   ├─ IF final victory
│   │   │   └─ Play Win.mp3
│   │   │
│   │   └─ IF game over
│   │       ├─ Play game_over.wav
│   │       └─ Schedule loose.wav (1.5s delay)
│   │
│   └─ sound.play()
│
└─ END
```

---

## UI Navigation Algorithm

### Menu Navigation
```
MENU NAVIGATION
│
├─ INITIALIZE
│   ├─ selected_option = 0
│   ├─ options = [list of menu items]
│   └─ menu_running = True
│
└─ WHILE menu_running
    │
    ├─ DRAW MENU
    │   ├─ Draw background
    │   ├─ Draw title
    │   ├─ FOR each option
    │   │   ├─ IF option == selected_option
    │   │   │   ├─ color = YELLOW
    │   │   │   └─ Draw selection box
    │   │   └─ ELSE
    │   │       └─ color = WHITE
    │   │   └─ Draw option text
    │   └─ Update display
    │
    ├─ HANDLE INPUT
    │   │
    │   ├─ FOR each event
    │   │   │
    │   │   ├─ IF QUIT
    │   │   │   └─ RETURN "quit"
    │   │   │
    │   │   ├─ IF KEY_DOWN
    │   │   │   ├─ IF UP
    │   │   │   │   └─ selected_option = (selected_option - 1) % len(options)
    │   │   │   │
    │   │   │   ├─ IF DOWN
    │   │   │   │   └─ selected_option = (selected_option + 1) % len(options)
    │   │   │   │
    │   │   │   ├─ IF ENTER or SPACE
    │   │   │   │   ├─ menu_running = False
    │   │   │   │   └─ RETURN options[selected_option]
    │   │   │   │
    │   │   │   └─ IF ESC
    │   │   │       └─ RETURN "back"
    │   │   │
    │   │   └─ IF MOUSE_CLICK
    │   │       ├─ FOR each option
    │   │       │   ├─ IF click in option rect
    │   │       │   │   ├─ IF option == selected_option
    │   │       │   │   │   ├─ menu_running = False
    │   │       │   │   │   └─ RETURN option
    │   │       │   │   └─ ELSE
    │   │       │   │       └─ selected_option = option_index
    │   │       │   └─ ENDIF
    │   │       └─ ENDFOR
    │   │
    │   └─ ENDFOR
    │
    └─ CONTROL FRAME RATE (60 FPS)
```

### Level Map Navigation
```
LEVEL MAP NAVIGATION
│
├─ INITIALIZE
│   ├─ selected_level = min(highest_level_reached, 5)
│   └─ selecting = True
│
└─ WHILE selecting
    │
    ├─ DRAW LEVEL MAP
    │   ├─ Draw background
    │   ├─ Draw title
    │   ├─ FOR each level (1-5)
    │   │   ├─ Determine status (completed/available/locked)
    │   │   ├─ Determine color
    │   │   ├─ Draw level circle
    │   │   ├─ Draw level number
    │   │   ├─ Draw status label
    │   │   └─ IF not last level
    │   │       └─ Draw connection line
    │   └─ Update display
    │
    ├─ HANDLE INPUT
    │   │
    │   ├─ IF LEFT key
    │   │   └─ Move to previous accessible level
    │   │
    │   ├─ IF RIGHT key
    │   │   └─ Move to next accessible level
    │   │
    │   ├─ IF UP key
    │   │   └─ Move up in layout (if applicable)
    │   │
    │   ├─ IF DOWN key
    │   │   └─ Move down in layout (if applicable)
    │   │
    │   ├─ IF SPACE or ENTER
    │   │   ├─ selecting = False
    │   │   └─ RETURN selected_level
    │   │
    │   ├─ IF ESC
    │   │   └─ RETURN None
    │   │
    │   └─ IF MOUSE_CLICK
    │       ├─ FOR each level
    │       │   ├─ IF click in level circle AND accessible
    │       │   │   ├─ IF level == selected_level
    │       │   │   │   ├─ selecting = False
    │       │   │   │   └─ RETURN selected_level
    │       │   │   └─ ELSE
    │       │   │       └─ selected_level = level
    │       │   └─ ENDIF
    │       └─ ENDFOR
    │
    └─ CONTROL FRAME RATE
```

---

## Conclusion

These algorithms represent the core logic and flow of Space Fighters. Each algorithm is designed to be:

1. **Efficient**: Optimized for 60 FPS gameplay
2. **Maintainable**: Clear structure and logic
3. **Scalable**: Easy to extend with new features
4. **Robust**: Error handling and edge cases covered

The game uses event-driven programming, sprite-based collision detection, and state machines to create a smooth, responsive gaming experience.

**Key Algorithm Characteristics**:
- Frame-rate independent timing
- Efficient collision detection
- Progressive difficulty scaling
- Persistent save system
- Responsive UI navigation
- Dynamic audio management

These algorithms work together to create a complete, polished gaming experience with professional-grade features and smooth gameplay.
