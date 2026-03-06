"""
Game entities: Player, Enemy, Boss, Bullets, PowerUps
"""
import pygame
import random
import math
from enum import Enum
from constants import *
from assets import PLAYER_SHIPS, BULLET_IMAGES, ENEMY_IMAGES, BOSS_IMG, BOSS_SHIP_IMG
from assets import PLAYER_SHOOT, SPACE_SHOOT, BOSS_SHOOT

class PowerUpType(Enum):
    """Defines the types of power-ups available in the game"""
    BULLET_2 = 1  # Enhanced double-shot bullets
    BULLET_3 = 2  # Super triple-shot bullets with increased damage
    SHIELD = 3    # Shield protection and health restoration

class Player(pygame.sprite.Sprite):
    """
    Player spaceship class.
    Handles player movement, shooting, health, and power-ups.
    Supports both keyboard and mouse controls.
    """
    def __init__(self, ship_choice=0):
        """
        Initialize the player.
        
        Args:
            ship_choice: Index of the ship image to use (0-2)
        """
        super().__init__()
        self.ship_choice = ship_choice
        self.image = PLAYER_SHIPS[ship_choice]
        self.rect = self.image.get_rect()
        self.rect.centerx = INITIAL_WIDTH // 2
        self.rect.bottom = INITIAL_HEIGHT - 20
        
        # Movement properties
        self.speed = 5
        
        # Health system
        self.health = 100
        self.max_health = 100
        
        # Shooting system
        self.shoot_delay = 250  # Milliseconds between shots
        self.last_shot = pygame.time.get_ticks()
        
        # Power-up system
        self.power_up = None
        self.power_up_timer = 0
        self.shield_active = False
        self.bullet_level = 0  # 0=bullet_1, 1=bullet_2, 2=bullet_3
        
    def update(self, screen_width=INITIAL_WIDTH, screen_height=INITIAL_HEIGHT):
        """
        Update player position based on keyboard and mouse input.
        
        Args:
            screen_width: Current screen width for bounds checking
            screen_height: Current screen height for bounds checking
        """
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        
        # Keyboard movement (WASD or Arrow keys)
        keyboard_moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
            keyboard_moving = True
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
            keyboard_moving = True
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
            keyboard_moving = True
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed
            keyboard_moving = True
        
        # Mouse dragging - right button or middle button to drag player
        if (mouse_buttons[1] or mouse_buttons[2]) and not keyboard_moving:
            target_x = mouse_pos[0]
            target_y = mouse_pos[1]
            
            dx = target_x - self.rect.centerx
            dy = target_y - self.rect.centery
            distance = math.sqrt(dx**2 + dy**2)
            
            if distance > 5:
                move_speed = min(self.speed * 2, distance)
                self.rect.x += (dx / distance) * move_speed
                self.rect.y += (dy / distance) * move_speed
        
        # Keep player within current screen bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, screen_width, screen_height))
        
        # Update power-up timer
        if self.power_up_timer > 0:
            self.power_up_timer -= 1
        else:
            self.power_up = None
            self.shield_active = False
            
    def shoot(self):
        """
        Create bullets based on current weapon level.
        
        Returns:
            list: List of Bullet objects created
        """
        now = pygame.time.get_ticks()
        
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []
            
            if PLAYER_SHOOT:
                PLAYER_SHOOT.play()
            
            if self.bullet_level == 2:  # bullet_3 - triple shot spread
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0, self.bullet_level))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top, -2, self.bullet_level))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top, 2, self.bullet_level))
            elif self.bullet_level == 1:  # bullet_2 - double shot
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top, 0, self.bullet_level))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top, 0, self.bullet_level))
            else:  # bullet_1 - single shot
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0, self.bullet_level))
            
            return bullets
        return []
    
    def activate_power_up(self, power_type):
        """
        Activate a power-up effect on the player.
        
        Args:
            power_type: PowerUpType enum value indicating which power-up to activate
        """
        self.power_up = power_type
        self.power_up_timer = 300  # Duration in frames (5 seconds at 60 FPS)
        
        if power_type == PowerUpType.BULLET_2:
            self.bullet_level = 1
        elif power_type == PowerUpType.BULLET_3:
            self.bullet_level = 2
        elif power_type == PowerUpType.SHIELD:
            self.shield_active = True
            self.health = min(self.health + 30, self.max_health)

class Enemy(pygame.sprite.Sprite):
    """
    Enemy spaceship class with progressive AI.
    """
    def __init__(self, x, y, level, enemy_type=0):
        super().__init__()
        self.level = level
        self.enemy_type = enemy_type
        self.image = ENEMY_IMAGES[enemy_type % 3]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 1 + level * 0.3
        self.health = 1 + level // 2
        self.shoot_delay = max(1500 - level * 100, 800)
        self.last_shot = pygame.time.get_ticks()
        
    def update(self, player_pos, screen_height=600):
        """Update enemy position with AI tracking"""
        self.rect.y += self.speed
        
        # Simple AI: move horizontally towards player
        if self.rect.centerx < player_pos[0]:
            self.rect.x += self.speed * 0.5
        elif self.rect.centerx > player_pos[0]:
            self.rect.x -= self.speed * 0.5
        
        if self.rect.top > screen_height:
            self.kill()
    
    def shoot(self):
        """Attempt to shoot a bullet"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if SPACE_SHOOT:
                SPACE_SHOOT.play()
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None

class Boss(pygame.sprite.Sprite):
    """Boss enemy class with enhanced abilities"""
    def __init__(self, is_final_boss=False):
        super().__init__()
        self.is_final_boss = is_final_boss
        self.image = BOSS_SHIP_IMG if is_final_boss else BOSS_IMG
        self.rect = self.image.get_rect()
        self.rect.centerx = INITIAL_WIDTH // 2
        self.rect.y = -100
        
        self.speed = 1
        self.health = 50 if is_final_boss else 30
        self.max_health = self.health
        self.shoot_delay = 500 if is_final_boss else 800
        self.last_shot = pygame.time.get_ticks()
        self.direction = 1
        self.moving_down = True
        
    def update(self, player_pos, screen_width=800):
        """Update boss position with movement pattern"""
        if self.moving_down and self.rect.y < 50:
            self.rect.y += self.speed
        else:
            self.moving_down = False
            self.rect.x += self.speed * 2 * self.direction
            
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1
    
    def shoot(self):
        """Boss shooting pattern"""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if BOSS_SHOOT:
                BOSS_SHOOT.play()
            
            bullets = []
            if self.is_final_boss:
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx - 30, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx + 30, self.rect.bottom))
            else:
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
            
            return bullets
        return []

class Bullet(pygame.sprite.Sprite):
    """Player bullet class"""
    def __init__(self, x, y, offset_x=0, bullet_level=0):
        super().__init__()
        self.bullet_level = bullet_level
        self.image = BULLET_IMAGES[bullet_level]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10
        self.offset_x = offset_x
        self.damage = 1 + bullet_level
        
    def update(self):
        """Update bullet position"""
        self.rect.y += self.speed
        self.rect.x += self.offset_x
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """Enemy bullet class"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((6, 12))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = 5
        
    def update(self):
        """Update bullet position"""
        self.rect.y += self.speed
        if self.rect.top > 2000:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    """Power-up collectible class"""
    def __init__(self, x, y):
        super().__init__()
        self.type = random.choice(list(PowerUpType))
        self.image = pygame.Surface((20, 20))
        
        if self.type == PowerUpType.BULLET_2:
            self.image.fill(YELLOW)
            pygame.draw.rect(self.image, ORANGE, (5, 5, 10, 10))
        elif self.type == PowerUpType.BULLET_3:
            self.image.fill(PURPLE)
            pygame.draw.rect(self.image, YELLOW, (5, 5, 10, 10))
        else:  # SHIELD
            self.image.fill(GREEN)
            pygame.draw.circle(self.image, WHITE, (10, 10), 8)
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        
    def update(self):
        """Update power-up position"""
        self.rect.y += self.speed
        if self.rect.top > 2000:
            self.kill()
