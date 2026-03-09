"""
Save system for game progress
"""
import json
import os

SAVE_FILE = "game_save.json"

def save_progress(data):
    """
    Save game progress to file
    
    Args:
        data: Dictionary containing game progress data
    """
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving progress: {e}")
        return False

def load_progress():
    """
    Load game progress from file
    
    Returns:
        Dictionary containing game progress or None if no save exists
    """
    if not os.path.exists(SAVE_FILE):
        return None
    
    try:
        with open(SAVE_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading progress: {e}")
        return None

def get_default_progress():
    """Get default progress data"""
    return {
        'highest_level': 1,
        'completed_levels': [False] * 5,
        'unlocked_ships': [True, False, False],
        'bullet_power': 0,
        'player_health': 100,
        'music_volume': 0.3,
        'sound_volume': 0.5,
        'music_muted': False,
        'sound_muted': False
    }
