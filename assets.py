"""
Asset loading and management
"""
import pygame

# Initialize pygame and mixer early for asset loading
pygame.init()
pygame.mixer.init()

from constants import INITIAL_WIDTH, INITIAL_HEIGHT, WHITE

def load_image(filename, default_size=None):
    """
    Load an image file and optionally resize it.
    Returns a placeholder surface if loading fails.
    
    Args:
        filename: Path to the image file
        default_size: Tuple (width, height) to resize the image
    """
    try:
        img = pygame.image.load(filename)
        if default_size:
            img = pygame.transform.scale(img, default_size)
        return img
    except Exception as e:
        print(f"Could not load {filename}: {e}")
        # Create placeholder if image not found
        surf = pygame.Surface(default_size if default_size else (50, 50))
        surf.fill(WHITE)
        return surf

def load_sound(filename):
    """
    Load a sound file.
    Returns None if loading fails.
    
    Args:
        filename: Path to the sound file
    """
    try:
        return pygame.mixer.Sound(filename)
    except Exception as e:
        print(f"Could not load {filename}: {e}")
        return None

# Load Game Assets

# Game icon
GAME_ICON = load_image("assets/images/player/game_icon.png", (128, 128))

# Background images - will be scaled dynamically
SPACE_BACKGROUNDS = [
    load_image("assets/images/player/space1.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT)),
    load_image("assets/images/player/space2.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT)),
    load_image("assets/images/player/space3.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT))
]

# Planet images for each level
PLANET_IMAGES = [
    load_image("assets/images/levels/planet-1.png", (150, 150)),
    load_image("assets/images/levels/planet-2.png", (150, 150)),
    load_image("assets/images/levels/planet-3.png", (150, 150)),
    load_image("assets/images/levels/planet-4.png", (150, 150)),
    load_image("assets/images/levels/planet-5.png", (150, 150))
]

# Player ship options
PLAYER_SHIPS = [
    load_image("assets/images/player/ship1.png", (70, 56)),
    load_image("assets/images/player/ship2.png", (70, 56)),
    load_image("assets/images/player/blue_ship.png", (70, 56))
]

# Health bar image (optional)
LIFE_BAR_IMG = load_image("assets/images/player/life_bar.png", (200, 20))

# Bullet types (upgraded through power-ups)
BULLET_IMAGES = [
    load_image("assets/images/player/bullet_1.png", (8, 20)),
    load_image("assets/images/player/bullet_2.png", (8, 20)),
    load_image("assets/images/player/bullet_3.png", (8, 20)),
    load_image("assets/images/player/bullet_4.png", (8, 20))
]

# Blue laser for blue_ship
BLUE_LASER = load_image("assets/images/player/blue_laser.png", (10, 25))

# Enemy ship types by level
ENEMY_L1_IMAGES = [
    load_image("assets/images/enemy/enemy_L1 (1).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L1 (2).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L1 (3).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L1 (4).png", (40, 40))
]

ENEMY_L2_IMAGES = [
    load_image("assets/images/enemy/enemy_L2 (1).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L2 (2).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L2 (3).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L2 (4).png", (40, 40))
]

ENEMY_L3_IMAGES = [
    load_image("assets/images/enemy/enemy_L3 (1).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L3 (2).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L3 (3).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L3 (4).png", (40, 40))
]

ENEMY_L4_IMAGES = [
    load_image("assets/images/enemy/enemy_L4 (1).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L4 (2).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L4 (3).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L4 (4).png", (40, 40))
]

ENEMY_L5_IMAGES = [
    load_image("assets/images/enemy/enemy_L5 (1).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L5 (2).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L5 (3).png", (40, 40)),
    load_image("assets/images/enemy/enemy_L5 (4).png", (40, 40))
]

# Boss images by level
BOSS_IMAGES = [
    load_image("assets/images/enemy/boss_L1.png", (80, 80)),
    load_image("assets/images/enemy/boss_L2.png", (80, 80)),
    load_image("assets/images/enemy/boss_L3.png", (80, 80)),
    load_image("assets/images/enemy/boss_L4.png", (80, 80)),
    load_image("assets/images/enemy/boss_L5_ship.png", (120, 100))
]

# Explosion animations
ENEMY_EXPLOSION = load_image("assets/images/enemy/enemy_explosion.png", (60, 60))
PLAYER_EXPLOSION = load_image("assets/images/player/player_explosion.png", (60, 60))

# Load Sound Effects
BACKGROUND_SOUND = load_sound("assets/sounds/background_sound.wav")
EXPLOSION_1 = load_sound("assets/sounds/explosion_1.wav")  # Minor enemies
EXPLOSION_2 = load_sound("assets/sounds/explosion_2.wav")  # Boss explosion
GAME_OVER_SOUND = load_sound("assets/sounds/game_over.wav")
LOOSE_SOUND = load_sound("assets/sounds/loose.wav")
SHIP1_SHOOT = load_sound("assets/sounds/ship1_shoot.wav")  # Ship1
SHIP2_SHOOT = load_sound("assets/sounds/ship2_shoot.wav")  # Ship2
LASER_SHOOTING = load_sound("assets/sounds/laser_shooting.wav")  # Blue ship laser
BOSS_SHOOT = load_sound("assets/sounds/boss_shoot.wav")
MISSION_COMPLETE = load_sound("assets/sounds/mission_complete.wav")
WIN_SOUND = load_sound("assets/sounds/Win.mp3")
BUTTON_NAV = load_sound("assets/sounds/button_nav.wav")
BUTTON_CLICK = load_sound("assets/sounds/button_click.wav")

# Global volume settings
MUSIC_VOLUME = 0.3
SOUND_VOLUME = 0.5
MUSIC_MUTED = False
SOUND_MUTED = False

def initialize_sounds():
    """Set sound volumes and start background music"""
    # Set sound volumes to prevent audio clipping
    if EXPLOSION_1:
        EXPLOSION_1.set_volume(0.4 * SOUND_VOLUME)
    if EXPLOSION_2:
        EXPLOSION_2.set_volume(0.5 * SOUND_VOLUME)
    if GAME_OVER_SOUND:
        GAME_OVER_SOUND.set_volume(0.6 * SOUND_VOLUME)
    if LOOSE_SOUND:
        LOOSE_SOUND.set_volume(0.5 * SOUND_VOLUME)
    if SHIP1_SHOOT:
        SHIP1_SHOOT.set_volume(0.2 * SOUND_VOLUME)
    if SHIP2_SHOOT:
        SHIP2_SHOOT.set_volume(0.2 * SOUND_VOLUME)
    if LASER_SHOOTING:
        LASER_SHOOTING.set_volume(0.3 * SOUND_VOLUME)
    if BOSS_SHOOT:
        BOSS_SHOOT.set_volume(0.3 * SOUND_VOLUME)
    if MISSION_COMPLETE:
        MISSION_COMPLETE.set_volume(0.6 * SOUND_VOLUME)
    if WIN_SOUND:
        WIN_SOUND.set_volume(0.7 * SOUND_VOLUME)
    if BUTTON_NAV:
        BUTTON_NAV.set_volume(0.3 * SOUND_VOLUME)
    if BUTTON_CLICK:
        BUTTON_CLICK.set_volume(0.4 * SOUND_VOLUME)
    
    # Play background music on loop
    if BACKGROUND_SOUND and not MUSIC_MUTED:
        BACKGROUND_SOUND.set_volume(MUSIC_VOLUME)
        BACKGROUND_SOUND.play(-1)

def update_sound_volumes():
    """Update all sound volumes based on global settings"""
    if EXPLOSION_1:
        EXPLOSION_1.set_volume(0.4 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if EXPLOSION_2:
        EXPLOSION_2.set_volume(0.5 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if GAME_OVER_SOUND:
        GAME_OVER_SOUND.set_volume(0.6 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if LOOSE_SOUND:
        LOOSE_SOUND.set_volume(0.5 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if SHIP1_SHOOT:
        SHIP1_SHOOT.set_volume(0.2 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if SHIP2_SHOOT:
        SHIP2_SHOOT.set_volume(0.2 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if LASER_SHOOTING:
        LASER_SHOOTING.set_volume(0.3 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if BOSS_SHOOT:
        BOSS_SHOOT.set_volume(0.3 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if MISSION_COMPLETE:
        MISSION_COMPLETE.set_volume(0.6 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if WIN_SOUND:
        WIN_SOUND.set_volume(0.7 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if BUTTON_NAV:
        BUTTON_NAV.set_volume(0.3 * SOUND_VOLUME if not SOUND_MUTED else 0)
    if BUTTON_CLICK:
        BUTTON_CLICK.set_volume(0.4 * SOUND_VOLUME if not SOUND_MUTED else 0)
    
    if BACKGROUND_SOUND:
        BACKGROUND_SOUND.set_volume(MUSIC_VOLUME if not MUSIC_MUTED else 0)
