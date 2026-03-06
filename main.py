"""
Space Fighters - A Space Shooter Game
Main entry point

Developed with Python and Pygame
Features:
- 3 progressive levels with unique backgrounds
- Boss battles and final boss
- Multiple ship selection
- Power-ups and upgrades
- Progressive enemy AI
- Fully responsive window
"""

import pygame
from constants import FPS
from assets import initialize_sounds
from game import Game
from ui import UI

def main():
    """Main game loop"""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Initialize sounds
    initialize_sounds()
    
    # Create game instance
    game = Game()
    ui = UI(game)
    
    running = True
    
    # Show splash screen
    if not ui.show_splash_screen():
        pygame.quit()
        return
    
    # Main game loop - allows replaying levels
    while running:
        # Show level map to select level
        selected_level = ui.show_level_map()
        if selected_level is None:
            pygame.quit()
            return
        
        # Show ship selection
        game.ship_choice = ui.select_ship()
        if game.ship_choice is None:
            pygame.quit()
            return
        
        # Reset game for selected level
        game.reset_game(selected_level)
        
        # Start level
        game._last_message = (f"LEVEL {selected_level}", "Press SPACE to start", False)
        ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
        result = ui.wait_for_key()
        if result == "quit":
            pygame.quit()
            return
        
        # Play the level
        level_running = True
        while level_running:
            game.clock.tick(FPS)
            
            if not game.handle_events():
                running = False
                level_running = False
                continue
            
            status = game.update()
            game.draw()
            
            if status == "boss_defeated":
                game._last_message = ("BOSS DEFEATED!", f"Score: {game.score}", False)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key()
                if result == "quit":
                    running = False
                    level_running = False
                else:
                    # Level complete - unlock next level
                    if game.next_level():
                        # All levels complete
                        game._last_message = ("VICTORY!", f"All Levels Complete! Score: {game.score}", True)
                        ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                        result = ui.wait_for_key(allow_restart=True)
                        if result == "restart":
                            level_running = False
                        else:
                            running = False
                            level_running = False
                    else:
                        # Show level complete message and return to map
                        game._last_message = (f"LEVEL {game.level - 1} COMPLETE!", 
                                        f"Ship {game.level} Unlocked! Score: {game.score}", False)
                        ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                        ui.wait_for_key()
                        level_running = False
                    
            elif status == "final_boss_defeated":
                game._last_message = ("FINAL BOSS DEFEATED!", f"YOU WIN! Score: {game.score}", True)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key(allow_restart=True)
                if result == "restart":
                    level_running = False
                else:
                    running = False
                    level_running = False
                        
            elif status == "time_up":
                game._last_message = ("TIME'S UP!", f"Final Score: {game.score}", True)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key(allow_restart=True)
                if result == "restart":
                    level_running = False
                else:
                    running = False
                    level_running = False
                
            elif status == "game_over":
                game._last_message = ("GAME OVER", f"Final Score: {game.score}", True)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key(allow_restart=True)
                if result == "restart":
                    level_running = False
                else:
                    running = False
                    level_running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
