"""
Space Fighters - A Space Shooter Game
Main entry point

Developed with Python and Pygame
Features:
- 5 progressive levels with unique backgrounds and planets
- Boss battles and final boss
- Multiple ship selection (unlockable)
- Power-ups and upgrades
- Progressive enemy AI
- Save/load progress
- Pause functionality
- Settings menu with audio controls
- Fully responsive window
"""

import pygame
from constants import FPS
from assets import initialize_sounds, BUTTON_NAV, BUTTON_CLICK, WIN_SOUND
from game import Game
from ui import UI
from settings_menu import SettingsMenu

def main():
    """Main game loop"""
    # Initialize Pygame
    pygame.init()
    pygame.mixer.init()
    
    # Set window icon
    try:
        icon = pygame.image.load("assets/images/player/game_icon.png")
        pygame.display.set_icon(icon)
    except:
        pass  # If icon not found, continue without it
    
    # Initialize sounds
    initialize_sounds()
    
    # Create game instance
    game = Game()
    ui = UI(game)
    settings_menu = SettingsMenu(game)
    
    running = True
    
    # Show splash screen
    if not ui.show_splash_screen():
        pygame.quit()
        return
    
    # Main game loop - allows replaying levels
    while running:
        # Show main menu
        menu_choice = ui.show_main_menu()
        
        if menu_choice == "quit":
            game.save_game_progress()
            pygame.quit()
            return
        elif menu_choice == "settings":
            settings_menu.show_settings()
            continue
        elif menu_choice != "play":
            continue
        
        # Show level map to select level
        selected_level = ui.show_level_map()
        if selected_level is None:
            continue
        
        # Show ship selection
        game.ship_choice = ui.select_ship()
        if game.ship_choice is None:
            continue
        
        # Reset game for selected level
        game.reset_game(selected_level)
        
        # Start level
        game._last_message = (f"LEVEL {selected_level}", "Press SPACE to start", False)
        ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
        result = ui.wait_for_key()
        if result == "quit":
            continue
        
        # Play the level
        level_result = play_level(game, ui, settings_menu)
        
        if level_result == "quit":
            running = False
    
    game.save_game_progress()
    pygame.quit()

def play_level(game, ui, settings_menu):
    """Play a single level"""
    level_running = True
    
    while level_running:
        game.clock.tick(FPS)
        
        event_result = game.handle_events()
        if not event_result:
            return "quit"
        elif event_result == "show_pause_menu":
            # Show pause menu
            pause_result = show_pause_menu(game, ui, settings_menu)
            if pause_result == "quit":
                return "quit"
            elif pause_result == "main_menu":
                return "continue"
            # Otherwise resume game
            continue
        
        status = game.update()
        game.draw()
        
        if status == "boss_defeated":
            game._last_message = ("BOSS DEFEATED!", f"Score: {game.score}", False)
            ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
            result = ui.wait_for_key()
            
            if result == "quit":
                return "continue"
            
            # Level complete - advance
            next_result = game.next_level()
            
            if next_result == "game_complete":
                # All levels complete - show victory with restart option
                game._last_message = ("VICTORY!", f"All Levels Complete! Score: {game.score}", True)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key(allow_restart=True)
                
                # Stop win sound when user makes a choice
                if WIN_SOUND:
                    WIN_SOUND.stop()
                
                if result == "restart":
                    # Reset entire game
                    game.unlocked_ships = [True, False, False]
                    game.completed_levels = [False] * 5
                    game.highest_level_reached = 1
                    game.saved_bullet_power = 0
                    game.saved_health = 100
                    game.save_game_progress()
                return "continue"
            else:
                # Show level complete message and continue to next level
                game._last_message = (f"LEVEL {game.level - 1} COMPLETE!", 
                                f"Score: {game.score}", False)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key()
                
                if result == "quit":
                    return "continue"
                
                # Continue to next level automatically
                game._last_message = (f"LEVEL {game.level}", "Press SPACE to start", False)
                ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
                result = ui.wait_for_key()
                
                if result == "quit":
                    return "continue"
                
                # Reset game for next level with saved stats
                game.reset_game(game.level)
                # Continue playing the next level
                continue
                
        elif status == "final_boss_defeated":
            game._last_message = ("FINAL BOSS DEFEATED!", f"YOU WIN! Score: {game.score}", True)
            ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
            result = ui.wait_for_key(allow_restart=True)
            
            # Stop win sound when user makes a choice
            if WIN_SOUND:
                WIN_SOUND.stop()
            
            if result == "restart":
                # Reset entire game
                game.unlocked_ships = [True, False, False]
                game.completed_levels = [False] * 5
                game.highest_level_reached = 1
                game.saved_bullet_power = 0
                game.saved_health = 100
                game.save_game_progress()
            return "continue"
                    
        elif status == "time_up":
            game._last_message = ("TIME'S UP!", f"Final Score: {game.score}", True)
            ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
            result = ui.wait_for_key(allow_restart=True)
            return "continue"
            
        elif status == "game_over":
            game._last_message = ("GAME OVER", f"Final Score: {game.score}", True)
            ui.show_message(game._last_message[0], game._last_message[1], game._last_message[2])
            result = ui.wait_for_key(allow_restart=True)
            return "continue"
    
    return "continue"

def show_pause_menu(game, ui, settings_menu):
    """Show pause menu with options"""
    selected = 0
    options = ["Resume", "Settings", "Main Menu", "Quit"]
    
    # Capture the current game screen once to prevent blinking
    game_snapshot = game.screen.copy()
    
    while True:
        game.clock.tick(FPS)
        
        # Draw the captured game state (no animation updates)
        game.screen.blit(game_snapshot, (0, 0))
        
        # Draw pause overlay
        overlay = pygame.Surface((game.screen_width, game.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        game.screen.blit(overlay, (0, 0))
        
        # Title
        pause_text = game.font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(game.screen_width // 2, 100))
        game.screen.blit(pause_text, pause_rect)
        
        # Options
        start_y = 250
        spacing = 60
        
        for i, option in enumerate(options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            text = game.small_font.render(option, True, color)
            rect = text.get_rect(center=(game.screen_width // 2, start_y + i * spacing))
            game.screen.blit(text, rect)
            
            if i == selected:
                pygame.draw.rect(game.screen, (255, 255, 0), 
                               (rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10), 2)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.VIDEORESIZE:
                game.handle_window_resize(event.w, event.h)
                # Recapture the screen after resize
                game.draw()
                game_snapshot = game.screen.copy()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if BUTTON_NAV:
                        BUTTON_NAV.play()
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    if BUTTON_NAV:
                        BUTTON_NAV.play()
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if BUTTON_CLICK:
                        BUTTON_CLICK.play()
                    if options[selected] == "Resume":
                        game.paused = False
                        return "resume"
                    elif options[selected] == "Settings":
                        result = settings_menu.show_settings(from_pause=True)
                        if result == "resume":
                            game.paused = False
                            return "resume"
                        # If settings returns "back", recapture screen and continue showing pause menu
                        game.draw()
                        game_snapshot = game.screen.copy()
                    elif options[selected] == "Main Menu":
                        game.paused = False
                        return "main_menu"
                    elif options[selected] == "Quit":
                        return "quit"
                elif event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
                    if BUTTON_CLICK:
                        BUTTON_CLICK.play()
                    game.paused = False
                    return "resume"

if __name__ == "__main__":
    main()
