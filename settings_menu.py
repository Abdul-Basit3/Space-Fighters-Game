"""
Settings menu for audio and game controls
"""
import pygame
from constants import *
import assets
from assets import BUTTON_NAV, BUTTON_CLICK

class SettingsMenu:
    """Settings menu for adjusting game settings"""
    
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def show_settings(self, from_pause=False):
        """Display settings menu"""
        running = True
        selected_option = 0
        dragging_music = False
        dragging_sound = False
        
        if from_pause:
            options = ["Music Volume", "Sound Volume", "Mute Music", "Mute Sounds", "Resume Game"]
        else:
            options = ["Music Volume", "Sound Volume", "Mute Music", "Mute Sounds", "Reset Game", "Back"]
        
        while running:
            self.game.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            # Draw background
            scaled_bg = pygame.transform.scale(assets.SPACE_BACKGROUNDS[0], 
                                              (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            # Title
            title = self.font.render("SETTINGS", True, CYAN)
            title_rect = title.get_rect(center=(self.game.screen_width // 2, 50))
            self.game.screen.blit(title, title_rect)
            
            # Draw options
            start_y = 150
            spacing = 70
            option_rects = []
            music_bar_rect = None
            sound_bar_rect = None
            
            for i, option in enumerate(options):
                color = YELLOW if i == selected_option else WHITE
                y_pos = start_y + i * spacing
                
                if option == "Music Volume":
                    # Draw label
                    text = "Music Volume"
                    option_text = self.small_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(self.game.screen_width // 2, y_pos))
                    self.game.screen.blit(option_text, option_rect)
                    
                    # Draw volume bar
                    bar_width = 300
                    bar_height = 20
                    bar_x = (self.game.screen_width - bar_width) // 2
                    bar_y = y_pos + 25
                    
                    # Background bar
                    pygame.draw.rect(self.game.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                    # Volume fill
                    fill_width = int(bar_width * assets.MUSIC_VOLUME)
                    pygame.draw.rect(self.game.screen, CYAN, (bar_x, bar_y, fill_width, bar_height))
                    # Border
                    pygame.draw.rect(self.game.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                    # Percentage
                    percent_text = self.small_font.render(f"{int(assets.MUSIC_VOLUME * 100)}%", True, WHITE)
                    percent_rect = percent_text.get_rect(center=(bar_x + bar_width + 40, bar_y + bar_height // 2))
                    self.game.screen.blit(percent_text, percent_rect)
                    
                    # Store bar rect for mouse interaction
                    music_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                    # Store full selection area - adjusted to fit tightly around content
                    full_rect = pygame.Rect(bar_x - 10, y_pos - 10, bar_width + 70, 60)
                    option_rects.append((full_rect, i, option))
                    
                elif option == "Sound Volume":
                    # Draw label
                    text = "Sound Volume"
                    option_text = self.small_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(self.game.screen_width // 2, y_pos))
                    self.game.screen.blit(option_text, option_rect)
                    
                    # Draw volume bar
                    bar_width = 300
                    bar_height = 20
                    bar_x = (self.game.screen_width - bar_width) // 2
                    bar_y = y_pos + 25
                    
                    # Background bar
                    pygame.draw.rect(self.game.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                    # Volume fill
                    fill_width = int(bar_width * assets.SOUND_VOLUME)
                    pygame.draw.rect(self.game.screen, GREEN, (bar_x, bar_y, fill_width, bar_height))
                    # Border
                    pygame.draw.rect(self.game.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
                    # Percentage
                    percent_text = self.small_font.render(f"{int(assets.SOUND_VOLUME * 100)}%", True, WHITE)
                    percent_rect = percent_text.get_rect(center=(bar_x + bar_width + 40, bar_y + bar_height // 2))
                    self.game.screen.blit(percent_text, percent_rect)
                    
                    # Store bar rect for mouse interaction
                    sound_bar_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
                    # Store full selection area - adjusted to fit tightly around content
                    full_rect = pygame.Rect(bar_x - 10, y_pos - 10, bar_width + 70, 60)
                    option_rects.append((full_rect, i, option))
                    
                elif option == "Mute Music":
                    text = f"Music: {'MUTED' if assets.MUSIC_MUTED else 'ON'}"
                    option_text = self.small_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(self.game.screen_width // 2, y_pos))
                    self.game.screen.blit(option_text, option_rect)
                    option_rects.append((pygame.Rect(option_rect.left - 10, option_rect.top - 5, 
                                                     option_rect.width + 20, option_rect.height + 10), i, option))
                elif option == "Mute Sounds":
                    text = f"Sounds: {'MUTED' if assets.SOUND_MUTED else 'ON'}"
                    option_text = self.small_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(self.game.screen_width // 2, y_pos))
                    self.game.screen.blit(option_text, option_rect)
                    option_rects.append((pygame.Rect(option_rect.left - 10, option_rect.top - 5, 
                                                     option_rect.width + 20, option_rect.height + 10), i, option))
                else:
                    text = option
                    option_text = self.small_font.render(text, True, color)
                    option_rect = option_text.get_rect(center=(self.game.screen_width // 2, y_pos))
                    self.game.screen.blit(option_text, option_rect)
                    option_rects.append((pygame.Rect(option_rect.left - 10, option_rect.top - 5, 
                                                     option_rect.width + 20, option_rect.height + 10), i, option))
                
                # Draw selection indicator
                if i == selected_option:
                    if option in ["Music Volume", "Sound Volume"]:
                        # Calculate bar position
                        bar_width = 300
                        bar_x = (self.game.screen_width - bar_width) // 2
                        # Box covering label, bar, and percentage - tighter fit
                        pygame.draw.rect(self.game.screen, YELLOW, 
                                       (bar_x - 10, y_pos - 10, bar_width + 70, 60), 3)
                    else:
                        pygame.draw.rect(self.game.screen, YELLOW, 
                                       (option_rect.left - 10, option_rect.top - 5, 
                                        option_rect.width + 20, option_rect.height + 10), 3)
            
            # Instructions
            inst_text = self.small_font.render("UP/DOWN: Navigate | LEFT/RIGHT: Adjust | ENTER: Select | CLICK: Adjust Volume", 
                                              True, WHITE)
            inst_rect = inst_text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 50))
            self.game.screen.blit(inst_text, inst_rect)
            
            pygame.display.flip()
            
            # Handle mouse dragging for volume bars
            if dragging_music and music_bar_rect:
                if mouse_pos[0] >= music_bar_rect.left and mouse_pos[0] <= music_bar_rect.right:
                    new_volume = (mouse_pos[0] - music_bar_rect.left) / music_bar_rect.width
                    assets.MUSIC_VOLUME = max(0.0, min(1.0, new_volume))
                    assets.update_sound_volumes()
            
            if dragging_sound and sound_bar_rect:
                if mouse_pos[0] >= sound_bar_rect.left and mouse_pos[0] <= sound_bar_rect.right:
                    new_volume = (mouse_pos[0] - sound_bar_rect.left) / sound_bar_rect.width
                    assets.SOUND_VOLUME = max(0.0, min(1.0, new_volume))
                    assets.update_sound_volumes()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        # Check if clicking on volume bars
                        if music_bar_rect and music_bar_rect.collidepoint(mouse_pos):
                            dragging_music = True
                            # Set volume immediately
                            new_volume = (mouse_pos[0] - music_bar_rect.left) / music_bar_rect.width
                            assets.MUSIC_VOLUME = max(0.0, min(1.0, new_volume))
                            assets.update_sound_volumes()
                        elif sound_bar_rect and sound_bar_rect.collidepoint(mouse_pos):
                            dragging_sound = True
                            # Set volume immediately
                            new_volume = (mouse_pos[0] - sound_bar_rect.left) / sound_bar_rect.width
                            assets.SOUND_VOLUME = max(0.0, min(1.0, new_volume))
                            assets.update_sound_volumes()
                        else:
                            # Check if clicking on any option
                            for rect, idx, opt in option_rects:
                                if rect.collidepoint(mouse_pos):
                                    if idx != selected_option:
                                        if BUTTON_NAV:
                                            BUTTON_NAV.play()
                                        selected_option = idx
                                    else:
                                        # Click on already selected option
                                        if BUTTON_CLICK:
                                            BUTTON_CLICK.play()
                                        if opt == "Mute Music":
                                            assets.MUSIC_MUTED = not assets.MUSIC_MUTED
                                            assets.update_sound_volumes()
                                        elif opt == "Mute Sounds":
                                            assets.SOUND_MUTED = not assets.SOUND_MUTED
                                            assets.update_sound_volumes()
                                        elif opt == "Reset Game":
                                            if self.confirm_reset():
                                                self.game.unlocked_ships = [True, False, False]
                                                self.game.completed_levels = [False] * 5
                                                self.game.highest_level_reached = 1
                                                self.game.saved_bullet_power = 0
                                                self.game.saved_health = 100
                                                self.game.save_game_progress()
                                        elif opt == "Resume Game":
                                            self.game.save_game_progress()
                                            self.game.paused = False
                                            return "resume"
                                        elif opt == "Back":
                                            self.game.save_game_progress()
                                            return "back"
                                    break
                
                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click release
                        dragging_music = False
                        dragging_sound = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if BUTTON_NAV:
                            BUTTON_NAV.play()
                        selected_option = (selected_option - 1) % len(options)
                    elif event.key == pygame.K_DOWN:
                        if BUTTON_NAV:
                            BUTTON_NAV.play()
                        selected_option = (selected_option + 1) % len(options)
                    
                    elif event.key == pygame.K_LEFT:
                        if BUTTON_NAV:
                            BUTTON_NAV.play()
                        if options[selected_option] == "Music Volume":
                            assets.MUSIC_VOLUME = max(0.0, assets.MUSIC_VOLUME - 0.1)
                            assets.update_sound_volumes()
                        elif options[selected_option] == "Sound Volume":
                            assets.SOUND_VOLUME = max(0.0, assets.SOUND_VOLUME - 0.1)
                            assets.update_sound_volumes()
                    
                    elif event.key == pygame.K_RIGHT:
                        if BUTTON_NAV:
                            BUTTON_NAV.play()
                        if options[selected_option] == "Music Volume":
                            assets.MUSIC_VOLUME = min(1.0, assets.MUSIC_VOLUME + 0.1)
                            assets.update_sound_volumes()
                        elif options[selected_option] == "Sound Volume":
                            assets.SOUND_VOLUME = min(1.0, assets.SOUND_VOLUME + 0.1)
                            assets.update_sound_volumes()
                    
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        if options[selected_option] == "Mute Music":
                            assets.MUSIC_MUTED = not assets.MUSIC_MUTED
                            assets.update_sound_volumes()
                        elif options[selected_option] == "Mute Sounds":
                            assets.SOUND_MUTED = not assets.SOUND_MUTED
                            assets.update_sound_volumes()
                        elif options[selected_option] == "Reset Game":
                            if self.confirm_reset():
                                self.game.unlocked_ships = [True, False, False]
                                self.game.completed_levels = [False] * 5
                                self.game.highest_level_reached = 1
                                self.game.saved_bullet_power = 0
                                self.game.saved_health = 100
                                self.game.save_game_progress()
                        elif options[selected_option] == "Resume Game":
                            self.game.save_game_progress()
                            self.game.paused = False
                            return "resume"
                        elif options[selected_option] == "Back":
                            self.game.save_game_progress()
                            return "back"
                    
                    elif event.key == pygame.K_ESCAPE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        self.game.save_game_progress()
                        if from_pause:
                            return "resume"
                        return "back"
        
        return "back"
    
    def confirm_reset(self):
        """Show confirmation dialog for reset"""
        confirming = True
        
        while confirming:
            self.game.clock.tick(FPS)
            
            # Draw background
            scaled_bg = pygame.transform.scale(assets.SPACE_BACKGROUNDS[0], 
                                              (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(220)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            # Confirmation text
            confirm_text = self.font.render("Reset all progress?", True, RED)
            confirm_rect = confirm_text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 - 50))
            self.game.screen.blit(confirm_text, confirm_rect)
            
            yes_text = self.small_font.render("Press Y to confirm", True, GREEN)
            yes_rect = yes_text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 + 20))
            self.game.screen.blit(yes_text, yes_rect)
            
            no_text = self.small_font.render("Press N to cancel", True, WHITE)
            no_rect = no_text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 + 50))
            self.game.screen.blit(no_text, no_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        return True
                    elif event.key == pygame.K_n or event.key == pygame.K_ESCAPE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        return False
        
        return False
