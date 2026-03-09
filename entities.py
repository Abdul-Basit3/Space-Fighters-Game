"""
Game entities: Player, Enemy, Boss, Bullets, PowerUps
"""
import pygame
import random
import math
from enum import Enum
from constants import *
from assets import (PLAYER_SHIPS, BULLET_IMAGES, BLUE_LASER, 
                    ENEMY_L1_IMAGES, ENEMY_L2_IMAGES, ENEMY_L3_IMAGES, ENEMY_L4_IMAGES, ENEMY_L5_IMAGES,
                    BOSS_IMAGES, ENEMY_EXPLOSION, PLAYER_EXPLOSION,
                    SHIP1_SHOOT, SHIP2_SHOOT, LASER_SHOOTING, BOSS_SHOOT, EXPLOSION_1, EXPLOSION_2,
                    GAME_OVER_SOUND, LOOSE_SOUND, SOUND_MUTED)

class PowerUpType(Enum):
    """Defines the types of power-ups available in the game"""
    BULLET_POWER = 1  # Increase bullet power level
    HEALTH = 2        # Health restoration
    SHIELD = 3        # Shield protection

class Player(pygame.sprite.Sprite):
    """
    Player spaceship class.
    Handles player movement, shooting, health, and power-ups.
    Supports both keyboard and mouse controls.
    """
    def __init__(self, ship_choice=0, bullet_power=0, health=100):
        """
        Initialize the player.
        
        Args:
            ship_choice: Index of the ship image to use (0-2)
            bullet_power: Starting bullet power level (0-3)
            health: Starting health
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
        self.health = health
        self.max_health = 100
        
        # Shooting system
        self.shoot_delay = 250 if ship_choice != 2 else 200  # Blue ship shoots faster
        self.last_shot = pygame.time.get_ticks()
        
        # Power-up system
        self.power_up = None
        self.power_up_timer = 0
        self.shield_active = False
        self.bullet_level = bullet_power  # 0=bullet_1, 1=bullet_2, 2=bullet_3, 3=bullet_4
        
        # Explosion animation
        self.exploding = False
        self.explosion_timer = 0
        
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
        Create bullets based on current weapon level and ship type.
        
        Returns:
            list: List of Bullet objects created
        """
        now = pygame.time.get_ticks()
        
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullets = []
            
            # Play appropriate shooting sound
            if not SOUND_MUTED:
                if self.ship_choice == 2:  # Blue ship uses laser sound
                    if LASER_SHOOTING:
                        LASER_SHOOTING.play()
                elif self.ship_choice == 1:  # Ship2 uses ship2_shoot
                    if SHIP2_SHOOT:
                        SHIP2_SHOOT.play()
                else:  # Ship1 uses ship1_shoot
                    if SHIP1_SHOOT:
                        SHIP1_SHOOT.play()
            
            # Create bullets based on power level
            if self.bullet_level == 3:  # bullet_4 - quad shot
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx - 20, self.rect.top, -1, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx + 20, self.rect.top, 1, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx, self.rect.top - 10, 0, self.bullet_level, self.ship_choice))
            elif self.bullet_level == 2:  # bullet_3 - triple shot spread
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx - 15, self.rect.top, -2, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx + 15, self.rect.top, 2, self.bullet_level, self.ship_choice))
            elif self.bullet_level == 1:  # bullet_2 - double shot
                bullets.append(Bullet(self.rect.centerx - 10, self.rect.top, 0, self.bullet_level, self.ship_choice))
                bullets.append(Bullet(self.rect.centerx + 10, self.rect.top, 0, self.bullet_level, self.ship_choice))
            else:  # bullet_1 - single shot
                bullets.append(Bullet(self.rect.centerx, self.rect.top, 0, self.bullet_level, self.ship_choice))
            
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
        
        if power_type == PowerUpType.BULLET_POWER:
            # Increase bullet power level (max 3)
            self.bullet_level = min(self.bullet_level + 1, 3)
        elif power_type == PowerUpType.HEALTH:
            # Restore health
            self.health = min(self.health + 30, self.max_health)
        elif power_type == PowerUpType.SHIELD:
            self.shield_active = True
            self.health = min(self.health + 20, self.max_health)
    
    def take_damage(self, damage):
        """
        Take damage and reduce bullet power if hit
        
        Args:
            damage: Amount of damage to take
        """
        if not self.shield_active:
            self.health -= damage
            # Reduce bullet power when hit
            if self.bullet_level > 0 and damage >= 10:
                self.bullet_level = max(0, self.bullet_level - 1)
    
    def start_explosion(self):
        """Start player explosion animation"""
        self.exploding = True
        self.explosion_timer = 30  # Frames for explosion animation
        if not SOUND_MUTED:
            if GAME_OVER_SOUND:
                GAME_OVER_SOUND.play()
            # Play loose sound after game over sound
            pygame.time.set_timer(pygame.USEREVENT + 1, 1500, 1)  # Play after 1.5 seconds

class Enemy(pygame.sprite.Sprite):
    """
    Enemy spaceship class with progressive AI.
    """
    def __init__(self, x, y, level, enemy_type=0):
        super().__init__()
        self.level = level
        self.enemy_type = enemy_type
        
        # Select enemy image based on level
        if level == 1:
            self.image = ENEMY_L1_IMAGES[enemy_type % len(ENEMY_L1_IMAGES)]
        elif level == 2:
            self.image = ENEMY_L2_IMAGES[enemy_type % len(ENEMY_L2_IMAGES)]
        elif level == 3:
            self.image = ENEMY_L3_IMAGES[enemy_type % len(ENEMY_L3_IMAGES)]
        elif level == 4:
            self.image = ENEMY_L4_IMAGES[enemy_type % len(ENEMY_L4_IMAGES)]
        else:  # level 5
            self.image = ENEMY_L5_IMAGES[enemy_type % len(ENEMY_L5_IMAGES)]
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speed = 1 + level * 0.3
        self.health = 1 + level // 2
        self.shoot_delay = max(1500 - level * 100, 800)
        self.last_shot = pygame.time.get_ticks()
        
        # Explosion animation
        self.exploding = False
        self.explosion_timer = 0
        
    def update(self, player_pos, screen_height=600):
        """Update enemy position with AI tracking"""
        if self.exploding:
            self.explosion_timer -= 1
            if self.explosion_timer <= 0:
                self.kill()
            return
        
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
        if self.exploding:
            return None
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if not SOUND_MUTED and BOSS_SHOOT:
                BOSS_SHOOT.play()
            return EnemyBullet(self.rect.centerx, self.rect.bottom)
        return None
    
    def start_explosion(self):
        """Start enemy explosion animation"""
        self.exploding = True
        self.explosion_timer = 20
        self.image = ENEMY_EXPLOSION
        if not SOUND_MUTED and EXPLOSION_1:
            EXPLOSION_1.play()

class Boss(pygame.sprite.Sprite):
    """Boss enemy class with enhanced abilities"""
    def __init__(self, level=1):
        super().__init__()
        self.level = level
        self.image = BOSS_IMAGES[min(level - 1, len(BOSS_IMAGES) - 1)]
        self.rect = self.image.get_rect()
        self.rect.centerx = INITIAL_WIDTH // 2
        self.rect.y = -100
        
        self.is_final_boss = (level == 5)
        self.speed = 1
        self.health = 30 + (level * 10)
        self.max_health = self.health
        self.shoot_delay = 500 if self.is_final_boss else 800
        self.last_shot = pygame.time.get_ticks()
        self.direction = 1
        self.moving_down = True
        
        # Explosion animation
        self.exploding = False
        self.explosion_timer = 0
        
    def update(self, player_pos, screen_width=800):
        """Update boss position with movement pattern"""
        if self.exploding:
            self.explosion_timer -= 1
            if self.explosion_timer <= 0:
                self.kill()
            return
        
        if self.moving_down and self.rect.y < 50:
            self.rect.y += self.speed
        else:
            self.moving_down = False
            self.rect.x += self.speed * 2 * self.direction
            
            if self.rect.right >= screen_width or self.rect.left <= 0:
                self.direction *= -1
    
    def shoot(self):
        """Boss shooting pattern"""
        if self.exploding:
            return []
        
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if not SOUND_MUTED and BOSS_SHOOT:
                BOSS_SHOOT.play()
            
            bullets = []
            if self.is_final_boss:
                # Final boss shoots 5 bullets
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx - 30, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx + 30, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx - 60, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx + 60, self.rect.bottom))
            elif self.level >= 3:
                # Level 3+ bosses shoot 3 bullets
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx - 30, self.rect.bottom))
                bullets.append(EnemyBullet(self.rect.centerx + 30, self.rect.bottom))
            else:
                # Early bosses shoot 1 bullet
                bullets.append(EnemyBullet(self.rect.centerx, self.rect.bottom))
            
            return bullets
        return []
    
    def start_explosion(self):
        """Start boss explosion animation"""
        self.exploding = True
        self.explosion_timer = 40
        self.image = pygame.transform.scale(ENEMY_EXPLOSION, (self.rect.width, self.rect.height))
        if not SOUND_MUTED and EXPLOSION_2:
            EXPLOSION_2.play()

class Bullet(pygame.sprite.Sprite):
    """Player bullet class"""
    def __init__(self, x, y, offset_x=0, bullet_level=0, ship_choice=0):
        super().__init__()
        self.bullet_level = bullet_level
        self.ship_choice = ship_choice
        
        # Blue ship uses laser
        if ship_choice == 2:
            self.image = BLUE_LASER
        else:
            self.image = BULLET_IMAGES[min(bullet_level, len(BULLET_IMAGES) - 1)]
        
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
        
        if self.type == PowerUpType.BULLET_POWER:
            self.image.fill(YELLOW)
            pygame.draw.rect(self.image, ORANGE, (5, 5, 10, 10))
            self.name = "BULLET+"
        elif self.type == PowerUpType.HEALTH:
            self.image.fill(RED)
            pygame.draw.circle(self.image, WHITE, (10, 10), 8)
            self.name = "HEALTH"
        else:  # SHIELD
            self.image.fill(GREEN)
            pygame.draw.circle(self.image, WHITE, (10, 10), 8)
            self.name = "SHIELD"
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 2
        
    def update(self):
        """Update power-up position"""
        self.rect.y += self.speed
        if self.rect.top > 2000:
            self.kill()
