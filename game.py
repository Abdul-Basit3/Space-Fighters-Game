"""
Main game class and logic
"""
import pygame
import random
from constants import *
from assets import BACKGROUNDS, EXPLOSION_1, EXPLOSION_2, GAME_OVER_SOUND
from entities import Player, Enemy, Boss, PowerUp

class Game:
    """
    Main game class that handles all game logic, rendering, and state management.
    Fully responsive to window size changes.
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
        
        # Progression system
        self.unlocked_ships = [True, False, False]
        self.completed_levels = [False, False, False]
        self.highest_level_reached = 1
        
        self.reset_game()
        
    def reset_game(self, level=1):
        """Reset game state for a new game or level"""
        self.level = level
        self.score = 0
        self.enemies_destroyed = 0
        self.enemies_needed = 15 + (level - 1) * 10
        self.time_limit = 90
        self.start_time = pygame.time.get_ticks()
        
        self.boss_active = False
        self.boss = None
        self.final_boss_defeated = False
        
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        
        self.player = Player(self.ship_choice if hasattr(self, 'ship_choice') else 0)
        self.all_sprites.add(self.player)
        
        self.spawn_timer = 0
        self.spawn_delay = 40
        
    def spawn_enemy(self):
        """Spawn a new enemy at a random position"""
        x = random.randint(40, max(80, self.screen_width - 40))
        y = random.randint(-100, -40)
        enemy_type = random.randint(0, 2)
        enemy = Enemy(x, y, self.level, enemy_type)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)
        
    def spawn_boss(self, is_final=False):
        """Spawn a boss enemy"""
        self.boss = Boss(is_final)
        self.boss.rect.centerx = self.screen_width // 2
        self.boss_active = True
        self.all_sprites.add(self.boss)
        
    def next_level(self):
        """Advance to the next level and unlock rewards"""
        if self.level <= 3:
            self.completed_levels[self.level - 1] = True
        
        if self.level == 1:
            self.unlocked_ships[1] = True
        elif self.level == 2:
            self.unlocked_ships[2] = True
        
        self.level += 1
        
        if self.level > self.highest_level_reached:
            self.highest_level_reached = self.level
        
        if self.level > 3:
            return True
        
        self.enemies_destroyed = 0
        self.enemies_needed = 15 + (self.level - 1) * 10
        self.time_limit = 90
        self.start_time = pygame.time.get_ticks()
        self.boss_active = False
        self.boss = None
        return False
        
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
                return False
            
            if event.type == pygame.VIDEORESIZE:
                self.handle_window_resize(event.w, event.h)
            
            # Mouse shooting
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    new_bullets = self.player.shoot()
                    for bullet in new_bullets:
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)
        
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
                        self.boss.kill()
                        self.boss_active = False
                        if EXPLOSION_2:
                            EXPLOSION_2.play()
                        
                        if self.boss.is_final_boss:
                            self.final_boss_defeated = True
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
                            enemy.kill()
                            if EXPLOSION_1:
                                EXPLOSION_1.play()
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
                self.spawn_boss(is_final=(self.level == 3))
        
        # Enemy bullet collisions with player
        hit_bullets = pygame.sprite.spritecollide(self.player, self.enemy_bullets, True)
        if hit_bullets and not self.player.shield_active:
            self.player.health -= len(hit_bullets) * 10
        
        # Enemy collisions with player
        hit_enemies = pygame.sprite.spritecollide(self.player, self.enemies, True)
        if hit_enemies and not self.player.shield_active:
            self.player.health -= len(hit_enemies) * 20
        
        # Power-up collection
        hit_power_ups = pygame.sprite.spritecollide(self.player, self.power_ups, True)
        for power_up in hit_power_ups:
            self.player.activate_power_up(power_up.type)
            self.score += 50
        
        # Check time
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = self.time_limit - elapsed_time
        
        # Check win/lose conditions
        if remaining_time <= 0 and not self.boss_active:
            return "time_up"
        elif self.player.health <= 0:
            if GAME_OVER_SOUND:
                GAME_OVER_SOUND.play()
            return "game_over"
        
        return "playing"
        
    def draw(self):
        """Draw all game elements with proper scaling for current window size"""
        bg_index = min(self.level - 1, 2)
        scaled_bg = pygame.transform.scale(BACKGROUNDS[bg_index], (self.screen_width, self.screen_height))
        self.screen.blit(scaled_bg, (0, 0))
        
        self.all_sprites.draw(self.screen)
        
        # Draw shield effect
        if self.player.shield_active:
            pygame.draw.circle(self.screen, GREEN, self.player.rect.center, 35, 3)
        
        # Draw boss health bar
        if self.boss_active and self.boss:
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
            enemies_text = self.small_font.render(f"Kills: {self.enemies_destroyed}/{self.enemies_needed}", True, WHITE)
            self.screen.blit(enemies_text, (10, 90))
        
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000
        remaining_time = max(0, self.time_limit - elapsed_time)
        time_text = self.small_font.render(f"Time: {int(remaining_time)}s", True, WHITE)
        self.screen.blit(time_text, (self.screen_width - 120, 10))
        
        # Health bar
        health_bar_x = 10
        health_bar_y = self.screen_height - 35
        health_width = min(200, self.screen_width - 20)
        health_height = 20
        
        pygame.draw.rect(self.screen, RED, (health_bar_x, health_bar_y, health_width, health_height))
        current_health_width = health_width * (self.player.health / self.player.max_health)
        pygame.draw.rect(self.screen, GREEN, (health_bar_x, health_bar_y, current_health_width, health_height))
        pygame.draw.rect(self.screen, WHITE, (health_bar_x, health_bar_y, health_width, health_height), 2)
        
        health_text = self.small_font.render(f"HP: {max(0, int(self.player.health))}", True, WHITE)
        self.screen.blit(health_text, (health_bar_x + 5, health_bar_y + 2))
        
        # Power-up indicator
        if self.player.power_up:
            power_text = self.small_font.render(f"Power: {self.player.power_up.name}", True, YELLOW)
            self.screen.blit(power_text, (self.screen_width - 200, 40))
        
        pygame.display.flip()
