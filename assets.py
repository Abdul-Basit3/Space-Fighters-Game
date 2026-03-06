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

# Background images for each level - will be scaled dynamically
BACKGROUNDS = [
    load_image("assets/images/player/space1.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT)),
    load_image("assets/images/player/space2.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT)),
    load_image("assets/images/player/space3.jpg", (INITIAL_WIDTH, INITIAL_HEIGHT))
]

# Player ship options
PLAYER_SHIPS = [
    load_image("assets/images/player/ship1.png", (50, 40)),
    load_image("assets/images/player/ship2.png", (50, 40)),
    load_image("assets/images/player/ship3.png", (50, 40))
]

# Health bar image (optional)
LIFE_BAR_IMG = load_image("assets/images/player/life_bar.png", (200, 20))

# Bullet types (upgraded through power-ups)
BULLET_IMAGES = [
    load_image("assets/images/player/bullet_1.png", (8, 20)),
    load_image("assets/images/player/bullet_2.png", (8, 20)),
    load_image("assets/images/player/bullet_3.png", (8, 20))
]

# Enemy ship types
ENEMY_IMAGES = [
    load_image("assets/images/enemy/enemy_1.png", (40, 40)),
    load_image("assets/images/enemy/enemy_2.png", (40, 40)),
    load_image("assets/images/enemy/enemy_3.png", (40, 40))
]

# Boss images
BOSS_IMG = load_image("assets/images/enemy/boss.png", (80, 80))
BOSS_SHIP_IMG = load_image("assets/images/enemy/boss_ship.png", (120, 100))

# Load Sound Effects
BACKGROUND_SOUND = load_sound("assets/sounds/background_sound.wav")
EXPLOSION_1 = load_sound("assets/sounds/explosion_1.wav")
EXPLOSION_2 = load_sound("assets/sounds/explosion_2.wav")
GAME_OVER_SOUND = load_sound("assets/sounds/game_over.wav")
SPACE_SHOOT = load_sound("assets/sounds/space_shoot.wav")
PLAYER_SHOOT = load_sound("assets/sounds/player_shoot.wav")
BOSS_SHOOT = load_sound("assets/sounds/boss_shoot.wav")

def initialize_sounds():
    """Set sound volumes and start background music"""
    # Set sound volumes to prevent audio clipping
    if EXPLOSION_1:
        EXPLOSION_1.set_volume(0.4)
    if EXPLOSION_2:
        EXPLOSION_2.set_volume(0.5)
    if GAME_OVER_SOUND:
        GAME_OVER_SOUND.set_volume(0.6)
    if SPACE_SHOOT:
        SPACE_SHOOT.set_volume(0.2)
    if PLAYER_SHOOT:
        PLAYER_SHOOT.set_volume(0.2)
    if BOSS_SHOOT:
        BOSS_SHOOT.set_volume(0.3)
    
    # Play background music on loop
    if BACKGROUND_SOUND:
        BACKGROUND_SOUND.set_volume(0.3)  # Set volume to 30%
        BACKGROUND_SOUND.play(-1)  # Loop forever
