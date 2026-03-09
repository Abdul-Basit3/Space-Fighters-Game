"""
Main game class and logic with pause and settings
"""
import pygame
import random
from constants import *
from assets import (SPACE_BACKGROUNDS, PLANET_IMAGES, 
                    MISSION_COMPLETE, WIN_SOUND, LOOSE_SOUND,
                    MUSIC_VOLUME, SOUND_VOLUME, MUSIC_MUTED, SOUND_MUTED,
                    update_sound_volumes, BACKGROUND_SOUND)
from entities import Player, Enemy, Boss, PowerUp, PowerUpType
from save_system import save_progress, load_progress, get_default_progress
import assets

class Game:
    """
    Main game class that handles all game logic, rendering, and state management.
    """
    def __init__(self):
        """Initialize the game with responsive window"""
        self.screen = pygame.display.set_mode(
            (INITIAL_WIDTH, INITIAL_HEIGHT), 
            pygame.RESIZABLE | pygame.SHOWN
        )
        pygame.display.set_caption("Space Fighters")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Track current window size
        self.screen_width = INITIAL_WIDTH
        self.screen_height = INITIAL_HEIGHT
        
        # Load saved progress
        self.load_game_progress()
        
        # Game state
        self.paused = False
        
        self.reset_game()
        
    def load_game_progress(self):
        """Load saved game progress"""
        progress = load_progress()
        if progress is None:
            progress = get_default_progress()
        
        self.unlocked_ships = progress.get('unlocked_ships', [True, False, False])
        self.completed_levels = progress.get('completed_levels', [False] * 5)
        self.highest_level_reached = progress.get('highest_level', 1)
        self.saved_bullet_power = progress.get('bullet_power', 0)
        self.saved_health = progress.get('player_health', 100)
        
        # Load audio settings
        assets.MUSIC_VOLUME = progress.get('music_volume', 0.3)
        assets.SOUND_VOLUME = progress.get('sound_volume', 0.5)
        assets.MUSIC_MUTED = progress.get('music_muted', False)
        assets.SOUND_MUTED = progress.get('sound_muted', False)
        update_sound_volumes()
        
    def save_game_progress(self):
        """Save current game progress"""
        progress = {
            'highest_level': self.highest_level_reached,
            'completed_levels': self.completed_levels,
            'unlocked_ships': self.unlocked_ships,
            'bullet_power': self.player.bullet_level if hasattr(self, 'player') else 0,
            'player_health': int(self.player.health) if hasattr(self, 'player') else 100,
            'music_volume': assets.MUSIC_VOLUME,
            'sound_volume': assets.SOUND_VOLUME,
            'music_muted': assets.MUSIC_MUTED,
            'sound_muted': assets.SOUND_MUTED
        }
        save_progress(progress)
        
    def reset_game(self, level=1):
        """Reset game state for a new game or level"""
        self.level = level
        self.score = 0
        self.paused = False
        
        self.enemies_destroyed = 0
        self.enemies_needed = 20 + (level - 1) * 5  # Increased enemy requirements
        self.time_limit = 45 + (level * 5)  # Tight time limits for intense gameplay
        
        self.start_time = pygame.time.get_ticks()
        
        self.boss_active = False
        self.boss = None
        self.final_boss_defeated = False
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        
        # Create player with saved stats (only use saved stats if continuing from previous level)
        ship_choice = self.ship_choice if hasattr(self, 'ship_choice') else 0
        
        # For level 1 or when selecting from map, start fresh
        if level == 1 or not hasattr(self, 'continuing_game'):
            bullet_power = 0
            health = 100
        else:
            # Use saved stats when continuing through levels
            bullet_power = self.saved_bullet_power if hasattr(self, 'saved_bullet_power') else 0
            health = self.saved_health if hasattr(self, 'saved_health') else 100
        
        self.player = Player(ship_choice, bullet_power, health)
        self.all_sprites.add(self.player)
        
        # Reset continuing flag
        self.continuing_game = False
        
        self.spawn_timer = 0
        self.spawn_delay = 40
        
    def spawn_enemy(self):
        """Spawn a new enemy at a random position"""
        x = random.randint(40, max(80, self.screen_width - 40))
        y = random.randint(-100, -40)
        enemy_type = random.randint(0, 3)
        enemy = Enemy(x, y, self.level, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
    
    def spawn_boss(self):
        """Spawn a boss enemy"""
        self.boss = Boss(self.level)
        self.boss.rect.centerx = self.screen_width // 2
        self.boss_active = True
        self.all_sprites.add(self.boss)
        
    def next_level(self):
        """Advance to the next level and unlock rewards"""
        # Mark current level as completed
        if self.level <= MAX_LEVELS:
            self.completed_levels[self.level - 1] = True
        
        # Save current player stats for next level
        if hasattr(self, 'player'):
            self.saved_bullet_power = self.player.bullet_level
            self.saved_health = int(self.player.health)
        
        # Unlock ships based on completed level
        if self.level == 1:
            self.unlocked_ships[1] = True  # Ship 2 unlocked after completing level 1
        elif self.level == 3:
            self.unlocked_ships[2] = True  # Blue ship unlocked after completing level 3
        
        # Save progress after completing level
        self.save_game_progress()
        
        # Play mission complete sound
        if not assets.SOUND_MUTED and MISSION_COMPLETE:
            MISSION_COMPLETE.play()
        
        self.level += 1
        
        if self.level > self.highest_level_reached:
            self.highest_level_reached = self.level
        
        self.continuing_game = True  # Flag to use saved stats
        
        if self.level > MAX_LEVELS:
            return "game_complete"
        
        return "next_level"

    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        return self.paused
        
    def handle_window_resize(self, new_width, new_height):
        """Handle window resize events and update all game elements"""
        self.screen = pygame.display.set_mode(
            (new_width, new_height), 
            pygame.RESIZABLE | pygame.SHOWN
        )
        
        self.screen_width = new_width
        self.screen_height = new_height
        
        if hasattr(self, 'player') and self.player:
            self.player.rect.clamp_ip(pygame.Rect(0, 0, new_width, new_height))
    
    def handle_events(self):
        """Handle user input events including window events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.save_game_progress()
                return False
            
            if event.type == pygame.VIDEORESIZE:
                self.handle_window_resize(event.w, event.h)
            
            # Pause game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    paused = self.toggle_pause()
                    if paused:
                        return "show_pause_menu"
                    return True
            
            # Play loose sound after game over
            if event.type == pygame.USEREVENT + 1:
                if not assets.SOUND_MUTED and LOOSE_SOUND:
                    LOOSE_SOUND.play()
            
            # Mouse shooting
            if not self.paused:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        new_bullets = self.player.shoot()
                        for bullet in new_bullets:
                            self.bullets.add(bullet)
                            self.all_sprites.add(bullet)
        
        if self.paused:
            return True
        
        # Auto-shoot with spacebar or holding left mouse button
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
        if keys[pygame.K_SPACE] or mouse_buttons[0]:
            new_bullets = self.player.shoot()
            for bullet in new_bullets:
                self.bullets.add(bullet)
                self.all_sprites.add(bullet)
        
        return True
        
    def update(self):
        """Update all game objects with current screen dimensions"""
        if self.paused:
            return "paused"
        
        self.player.update(self.screen_width, self.screen_height)
        self.bullets.update()
        self.enemy_bullets.update()
        self.power_ups.update()
        
        # Update boss if active
        if self.boss_active and self.boss:
            self.boss.update(self.player.rect.center, self.screen_width)
            
            boss_bullets = self.boss.shoot()
            for bullet in boss_bullets:
                self.enemy_bullets.add(bullet)
                self.all_sprites.add(bullet)
            
            # Bullet collisions with boss
            for bullet in self.bullets:
                if pygame.sprite.collide_rect(bullet, self.boss):
                    bullet.kill()
                    self.boss.health -= bullet.damage
                    if self.boss.health <= 0:
                        self.boss.start_explosion()
                        self.boss_active = False
                        
                        if self.boss.is_final_boss:
                            self.final_boss_defeated = True
                            # Play win sound for final boss
                            if not assets.SOUND_MUTED and WIN_SOUND:
                                WIN_SOUND.play()
                            return "final_boss_defeated"
                        else:
                            self.score += 500
                            return "boss_defeated"
        else:
            # Update enemies
            for enemy in self.enemies:
                enemy.update(self.player.rect.center, self.screen_height)
                
                enemy_bullet = enemy.shoot()
                if enemy_bullet:
                    self.enemy_bullets.add(enemy_bullet)
                    self.all_sprites.add(enemy_bullet)
            
            # Spawn enemies
            self.spawn_timer += 1
            if self.spawn_timer >= self.spawn_delay and len(self.enemies) < 5 + self.level:
                self.spawn_enemy()
                self.spawn_timer = 0
            
            # Bullet collisions with enemies
            for bullet in self.bullets:
                hit_enemies = pygame.sprite.spritecollide(bullet, self.enemies, False)
                if hit_enemies:
                    bullet.kill()
                    for enemy in hit_enemies:
                        enemy.health -= bullet.damage
                        if enemy.health <= 0:
                            enemy.start_explosion()
                            self.score += 10 * self.level
                            self.enemies_destroyed += 1
                            
                            if random.random() < 0.2:
                                power_up = PowerUp(enemy.rect.centerx, enemy.rect.centery)
                                self.power_ups.add(power_up)
                                self.all_sprites.add(power_up)
            
            # Check if boss should spawn
            if self.enemies_destroyed >= self.enemies_needed and not self.boss_active:
                for enemy in self.enemies:
                    enemy.kill()
                self.spawn_boss()
        
        # Enemy bullet collisions with player
        hit_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hit_bullets and not self.player.shield_active:
            self.player.take_damage(len(hit_bullets) * 10)
        
        # Enemy collisions with player
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hit_enemies and not self.player.shield_active:
            for enemy in hit_enemies:
                enemy.start_explosion()
                self.player.take_damage(20)
        
        # Power-up collection
        hit_power_ups = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for power_up in hit_power_ups:
            self.player.activate_power_up(power_up.type)
            # Only Bullet Power gives score points
            if power_up.type == PowerUpType.BULLET_POWER:
                self.score += 50
        
        # Check time
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = self.time_limit - elapsed_time
        
        # Check win/lose conditions
        if remaining_time <= 0 and not self.boss_active:
            return "time_up"
        elif self.player.health <= 0:
            self.player.start_explosion()
            return "game_over"
        
        return "playing"

    def draw(self):
        """Draw all game elements with proper scaling for current window size"""
        # Rotate through space backgrounds
        bg_index = (self.level - 1) % len(SPACE_BACKGROUNDS)
        scaled_bg = pygame.transform.scale(SPACE_BACKGROUNDS[bg_index], (self.screen_width, self.screen_height))
        
        self.screen.blit(scaled_bg, (0, 0))
        
        # Draw planet in center for regular missions
        if self.level <= len(PLANET_IMAGES):
            planet = PLANET_IMAGES[self.level - 1]
            planet_rect = planet.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(planet, planet_rect)
        
        self.all_sprites.draw(self.screen)
        
        # Draw shield effect
        if self.player.shield_active:
            pygame.draw.circle(self.screen, GREEN, self.player.rect.center, 35, 3)
        
        # Draw boss health bar
        if self.boss_active and self.boss and not self.boss.exploding:
            boss_health_width = min(300, self.screen_width - 100)
            boss_health_x = (self.screen_width - boss_health_width) // 2
            pygame.draw.rect(self.screen, RED, (boss_health_x, 10, boss_health_width, 15))
            pygame.draw.rect(self.screen, YELLOW, (boss_health_x, 10, int(boss_health_width * (self.boss.health / self.boss.max_health)), 15))
            pygame.draw.rect(self.screen, WHITE, (boss_health_x, 10, boss_health_width, 15), 2)
            boss_text = self.small_font.render("BOSS", True, WHITE)
            self.screen.blit(boss_text, (boss_health_x + boss_health_width // 2 - 25, 30))
        
        # HUD
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (10, 10))
        
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 50))
        
        if not self.boss_active:
            target_text = self.small_font.render(f"Kills: {self.enemies_destroyed}/{self.enemies_needed}", True, WHITE)
            self.screen.blit(target_text, (10, 90))
        
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(0, self.time_limit - elapsed_time)
        time_text = self.small_font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        self.screen.blit(time_text, (self.screen_width - 120, 10))
        
        # Bullet power indicator
        bullet_power_text = self.small_font.render(f"Bullet Power: {self.player.bullet_level + 1}", True, CYAN)
        self.screen.blit(bullet_power_text, (self.screen_width - 180, 40))
        
        # Health bar
        health_bar_x = 10
        health_bar_y = self.screen_height - 35
        health_width = min(200, self.screen_width - 20)
        health_height = 20
        
        pygame.draw.rect(self.screen, RED, (health_bar_x, health_bar_y, health_width, health_height))
        current_health_width = health_width * (max(0, self.player.health) / self.player.max_health)
        pygame.draw.rect(self.screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_height))
        pygame.draw.rect(self.screen, WHITE, (health_bar_x, health_bar_y, health_width, health_height), 2)
        
        health_text = self.small_font.render(f"HP: {max(0, int(self.player.health))}", True, WHITE)
        self.screen.blit(health_text, (health_bar_x + 5, health_bar_y + 2))
        
        # Power-up indicator
        if self.player.power_up and self.player.power_up_timer > 0:
            power_text = self.small_font.render(f"Power: {self.player.power_up.name}", True, YELLOW)
            self.screen.blit(power_text, (self.screen_width - 200, 70))
        
        # Note: Pause menu is now handled in main.py
        
        pygame.display.flip()
