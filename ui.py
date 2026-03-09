"""
UI screens and menus
"""
import pygame
import math
from constants import *
from assets import SPACE_BACKGROUNDS as BACKGROUNDS, PLAYER_SHIPS, BUTTON_NAV, BUTTON_CLICK

class UI:
    """Handles all UI screens and menus"""
    
    def __init__(self, game):
        """Initialize UI with reference to game"""
        self.game = game
    
    def show_main_menu(self):
        """Display main menu"""
        selected = 0
        options = ["Play", "Settings", "Quit"]
        
        while True:
            self.game.clock.tick(FPS)
            
            scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            title = self.game.font.render("SPACE FIGHTERS", True, CYAN)
            title_rect = title.get_rect(center=(self.game.screen_width // 2, 100))
            self.game.screen.blit(title, title_rect)
            
            start_y = 250
            spacing = 60
            
            for i, option in enumerate(options):
                color = YELLOW if i == selected else WHITE
                text = self.game.small_font.render(option, True, color)
                rect = text.get_rect(center=(self.game.screen_width // 2, start_y + i * spacing))
                self.game.screen.blit(text, rect)
                
                if i == selected:
                    pygame.draw.rect(self.game.screen, YELLOW, 
                                   (rect.left - 10, rect.top - 5, rect.width + 20, rect.height + 10), 2)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
                
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
                        return options[selected].lower()
                    elif event.key == pygame.K_ESCAPE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        return "quit"
    
    def show_splash_screen(self):
        """Display the game splash screen with icon and loading bar"""
        splash_duration = 5000  # Increased to 5 seconds for better visibility
        start_time = pygame.time.get_ticks()
        
        title_font = pygame.font.Font(None, 80)
        subtitle_font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Load game icon
        try:
            from assets import GAME_ICON
            icon = GAME_ICON
        except:
            # Create placeholder if icon not found
            icon = pygame.Surface((128, 128))
            icon.fill(CYAN)
        
        while pygame.time.get_ticks() - start_time < splash_duration:
            self.game.clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return True
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
            
            progress = (pygame.time.get_ticks() - start_time) / splash_duration
            
            # Draw background
            scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            # Dark overlay
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            # Calculate alpha for fade-in
            if progress < 0.2:
                alpha = int(255 * (progress / 0.2))
            else:
                alpha = 255
            
            # Draw game icon - centered higher on screen
            icon_y = self.game.screen_height // 2 - 150
            
            # Draw main icon
            icon_copy = icon.copy()
            icon_copy.set_alpha(alpha)
            icon_rect = icon_copy.get_rect(center=(self.game.screen_width // 2, icon_y))
            self.game.screen.blit(icon_copy, icon_rect)
            
            # Draw title - more spacing from icon
            title_text = "SPACE FIGHTERS"
            title_surf = title_font.render(title_text, True, WHITE)
            title_surf.set_alpha(alpha)
            title_rect = title_surf.get_rect(center=(self.game.screen_width // 2, icon_y + 140))
            self.game.screen.blit(title_surf, title_rect)
            
            # Draw subtitle - better spacing
            if progress > 0.15:
                subtitle_alpha = int(255 * min(1.0, (progress - 0.15) / 0.2))
                subtitle_surf = subtitle_font.render("Prepare for Battle", True, YELLOW)
                subtitle_surf.set_alpha(subtitle_alpha)
                subtitle_rect = subtitle_surf.get_rect(center=(self.game.screen_width // 2, icon_y + 190))
                self.game.screen.blit(subtitle_surf, subtitle_rect)
            
            # Draw loading bar - starts at 20% progress, fills slowly
            if progress > 0.2:
                bar_width = 400
                bar_height = 30
                bar_x = (self.game.screen_width - bar_width) // 2
                bar_y = self.game.screen_height - 120
                
                # Loading bar background
                pygame.draw.rect(self.game.screen, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
                
                # Loading bar fill (animated) - slower progression
                # Maps progress 0.2-1.0 to fill 0-100%
                fill_progress = min(1.0, (progress - 0.2) / 0.8)
                fill_width = int(bar_width * fill_progress)
                
                # Gradient effect for loading bar
                for i in range(fill_width):
                    color_intensity = int(100 + 155 * (i / bar_width))
                    color = (0, color_intensity, 255)  # Blue gradient
                    pygame.draw.rect(self.game.screen, color, (bar_x + i, bar_y, 1, bar_height))
                
                # Loading bar border
                pygame.draw.rect(self.game.screen, CYAN, (bar_x, bar_y, bar_width, bar_height), 3)
                
                # Loading percentage
                loading_text = small_font.render(f"Loading... {int(fill_progress * 100)}%", True, WHITE)
                loading_rect = loading_text.get_rect(center=(self.game.screen_width // 2, bar_y + bar_height + 20))
                self.game.screen.blit(loading_text, loading_rect)
            
            # Skip prompt - appears later for better visibility
            if progress > 0.4:
                skip_alpha = int(128 + 127 * math.sin(progress * math.pi * 6))
                skip_surf = small_font.render("Press any key to skip", True, WHITE)
                skip_surf.set_alpha(skip_alpha)
                skip_rect = skip_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 50))
                self.game.screen.blit(skip_surf, skip_rect)
            
            pygame.display.flip()
        
        return True
    
    def show_message(self, message, submessage="", show_restart=False):
        """Display a message screen with options"""
        scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(scaled_bg, (0, 0))
        
        overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        self.game.screen.blit(overlay, (0, 0))
        
        text = self.game.font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 - 50))
        self.game.screen.blit(text, text_rect)
        
        if submessage:
            sub_text = self.game.small_font.render(submessage, True, WHITE)
            sub_rect = sub_text.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 - 10))
            self.game.screen.blit(sub_text, sub_rect)
        
        if show_restart:
            restart_rect = pygame.Rect(self.game.screen_width // 2 - 100, self.game.screen_height // 2 + 20, 200, 40)
            pygame.draw.rect(self.game.screen, GREEN, restart_rect, 2)
            restart_text = self.game.small_font.render("Press R or Click to Restart", True, GREEN)
            restart_text_rect = restart_text.get_rect(center=restart_rect.center)
            self.game.screen.blit(restart_text, restart_text_rect)
            
            quit_rect = pygame.Rect(self.game.screen_width // 2 - 100, self.game.screen_height // 2 + 70, 200, 40)
            pygame.draw.rect(self.game.screen, RED, quit_rect, 2)
            quit_text = self.game.small_font.render("Press Q or Click to Quit", True, RED)
            quit_text_rect = quit_text.get_rect(center=quit_rect.center)
            self.game.screen.blit(quit_text, quit_text_rect)
        else:
            continue_rect = pygame.Rect(self.game.screen_width // 2 - 150, self.game.screen_height // 2 + 20, 300, 50)
            pygame.draw.rect(self.game.screen, YELLOW, continue_rect, 3)
            continue_text = self.game.small_font.render("Press SPACE or Click to Continue", True, YELLOW)
            continue_text_rect = continue_text.get_rect(center=continue_rect.center)
            self.game.screen.blit(continue_text, continue_text_rect)
        
        pygame.display.flip()
        
    def wait_for_key(self, allow_restart=False):
        """Wait for user input (keyboard or mouse)"""
        waiting = True
        
        while waiting:
            self.game.clock.tick(FPS)
            mouse_pos = pygame.mouse.get_pos()
            
            if allow_restart:
                restart_rect = pygame.Rect(self.game.screen_width // 2 - 100, self.game.screen_height // 2 + 20, 200, 40)
                quit_rect = pygame.Rect(self.game.screen_width // 2 - 100, self.game.screen_height // 2 + 70, 200, 40)
            else:
                continue_rect = pygame.Rect(self.game.screen_width // 2 - 150, self.game.screen_height // 2 + 20, 300, 50)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
                    if hasattr(self.game, '_last_message'):
                        self.show_message(self.game._last_message[0], self.game._last_message[1], self.game._last_message[2])
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and not allow_restart:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        waiting = False
                    elif allow_restart:
                        if event.key == pygame.K_r:
                            if BUTTON_CLICK:
                                BUTTON_CLICK.play()
                            return "restart"
                        elif event.key == pygame.K_q:
                            if BUTTON_CLICK:
                                BUTTON_CLICK.play()
                            return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        if allow_restart:
                            if restart_rect.collidepoint(mouse_pos):
                                return "restart"
                            elif quit_rect.collidepoint(mouse_pos):
                                return "quit"
                        else:
                            if continue_rect.collidepoint(mouse_pos):
                                waiting = False
        
        pygame.event.clear()
        return "continue"
        
    def show_level_map(self):
        """Display level map showing completed levels and allowing level selection"""
        selecting = True
        selected_level = min(self.game.highest_level_reached, MAX_LEVELS)
        
        while selecting:
            self.game.clock.tick(FPS)
            
            scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            title = self.game.font.render("LEVEL MAP", True, CYAN)
            title_rect = title.get_rect(center=(self.game.screen_width // 2, 50))
            self.game.screen.blit(title, title_rect)
            
            # Position levels in two rows
            level_positions = [
                (self.game.screen_width // 4, self.game.screen_height // 2 - 50),
                (self.game.screen_width // 2, self.game.screen_height // 2 - 50),
                (3 * self.game.screen_width // 4, self.game.screen_height // 2 - 50),
                (self.game.screen_width // 3, self.game.screen_height // 2 + 80),
                (2 * self.game.screen_width // 3, self.game.screen_height // 2 + 80)
            ]
            
            level_rects = []
            for i in range(MAX_LEVELS):
                x, y = level_positions[i]
                level_num = i + 1
                
                is_accessible = level_num <= self.game.highest_level_reached
                is_completed = self.game.completed_levels[i]
                is_selected = level_num == selected_level
                
                if is_accessible:
                    if is_completed:
                        color = GREEN
                    elif is_selected:
                        color = YELLOW
                    else:
                        color = WHITE
                else:
                    color = (100, 100, 100)
                
                pygame.draw.circle(self.game.screen, color, (x, y), 40, 5 if not is_selected else 8)
                
                level_text = self.game.font.render(str(level_num), True, color)
                level_rect = level_text.get_rect(center=(x, y))
                self.game.screen.blit(level_text, level_rect)
                
                click_rect = pygame.Rect(x - 40, y - 40, 80, 80)
                level_rects.append((click_rect, level_num, is_accessible))
                
                if is_completed:
                    status = self.game.small_font.render("COMPLETED", True, GREEN)
                elif not is_accessible:
                    status = self.game.small_font.render("LOCKED", True, (150, 150, 150))
                else:
                    status = self.game.small_font.render("AVAILABLE", True, WHITE)
                
                status_rect = status.get_rect(center=(x, y + 60))
                self.game.screen.blit(status, status_rect)
                
                # Draw connection lines
                if i < 2:
                    next_x, next_y = level_positions[i + 1]
                    line_color = GREEN if self.game.completed_levels[i] else (100, 100, 100)
                    pygame.draw.line(self.game.screen, line_color, (x + 40, y), (next_x - 40, next_y), 3)
                elif i == 2:
                    next_x, next_y = level_positions[3]
                    line_color = GREEN if self.game.completed_levels[i] else (100, 100, 100)
                    pygame.draw.line(self.game.screen, line_color, (x, y + 40), (next_x, next_y - 40), 3)
                elif i == 3:
                    next_x, next_y = level_positions[4]
                    line_color = GREEN if self.game.completed_levels[i] else (100, 100, 100)
                    pygame.draw.line(self.game.screen, line_color, (x + 40, y), (next_x - 40, next_y), 3)
            
            inst1 = self.game.small_font.render("Use ARROW KEYS or CLICK to select level", True, YELLOW)
            inst1_rect = inst1.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 80))
            self.game.screen.blit(inst1, inst1_rect)
            
            inst2 = self.game.small_font.render("Press SPACE or ENTER to start level | ESC to go back", True, YELLOW)
            inst2_rect = inst2.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 50))
            self.game.screen.blit(inst2, inst2_rect)
            
            pygame.display.flip()
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                    
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for i in range(selected_level - 1, 0, -1):
                            if i <= self.game.highest_level_reached:
                                if BUTTON_NAV:
                                    BUTTON_NAV.play()
                                selected_level = i
                                break
                    elif event.key == pygame.K_RIGHT:
                        for i in range(selected_level + 1, MAX_LEVELS + 1):
                            if i <= self.game.highest_level_reached:
                                if BUTTON_NAV:
                                    BUTTON_NAV.play()
                                selected_level = i
                                break
                    elif event.key == pygame.K_UP:
                        if selected_level > 3:
                            if BUTTON_NAV:
                                BUTTON_NAV.play()
                            selected_level = max(1, selected_level - 2)
                    elif event.key == pygame.K_DOWN:
                        if selected_level <= 3:
                            if BUTTON_NAV:
                                BUTTON_NAV.play()
                            selected_level = min(self.game.highest_level_reached, selected_level + 2)
                    elif event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        selecting = False
                    elif event.key == pygame.K_ESCAPE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, level_num, is_accessible in level_rects:
                            if rect.collidepoint(mouse_pos) and is_accessible:
                                if level_num == selected_level:
                                    if BUTTON_CLICK:
                                        BUTTON_CLICK.play()
                                    selecting = False
                                else:
                                    if BUTTON_NAV:
                                        BUTTON_NAV.play()
                                    selected_level = level_num
        
        pygame.event.clear()
        return selected_level
    
    def select_ship(self):
        """Display ship selection screen with locked/unlocked ships"""
        selecting = True
        selected = 0
        
        for i in range(3):
            if self.game.unlocked_ships[i]:
                selected = i
                break
        
        while selecting:
            self.game.clock.tick(FPS)
            
            scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(200)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            title = self.game.font.render("SELECT YOUR SHIP", True, WHITE)
            title_rect = title.get_rect(center=(self.game.screen_width // 2, 50))
            self.game.screen.blit(title, title_rect)
            
            ship_spacing = min(250, (self.game.screen_width - 100) // 3)
            start_x = (self.game.screen_width - (ship_spacing * 2)) // 2
            
            ship_rects = []
            for i in range(3):
                x = start_x + i * ship_spacing
                y = self.game.screen_height // 2
                
                is_unlocked = self.game.unlocked_ships[i]
                
                ship_img = PLAYER_SHIPS[i].copy()
                
                if not is_unlocked:
                    dark_overlay = pygame.Surface(ship_img.get_size())
                    dark_overlay.fill((0, 0, 0))
                    dark_overlay.set_alpha(180)
                    ship_img.blit(dark_overlay, (0, 0))
                
                ship_rect = ship_img.get_rect(center=(x, y))
                self.game.screen.blit(ship_img, ship_rect)
                
                click_rect = pygame.Rect(x - 50, y - 50, 100, 100)
                ship_rects.append((click_rect, i, is_unlocked))
                
                if i == selected and is_unlocked:
                    pygame.draw.rect(self.game.screen, YELLOW, (x - 40, y - 40, 80, 80), 3)
                
                border_color = WHITE if is_unlocked else (100, 100, 100)
                pygame.draw.rect(self.game.screen, border_color, click_rect, 1)
                
                if is_unlocked:
                    num_text = self.game.small_font.render(f"Ship {i + 1}", True, WHITE)
                else:
                    num_text = self.game.small_font.render(f"Ship {i + 1}", True, (150, 150, 150))
                num_rect = num_text.get_rect(center=(x, y + 60))
                self.game.screen.blit(num_text, num_rect)
                
                if not is_unlocked:
                    if i == 1:
                        unlock_text = self.game.small_font.render("Complete Level 1", True, RED)
                    elif i == 2:
                        unlock_text = self.game.small_font.render("Complete Level 3", True, RED)
                    unlock_rect = unlock_text.get_rect(center=(x, y + 85))
                    self.game.screen.blit(unlock_text, unlock_rect)
                    
                    pygame.draw.rect(self.game.screen, RED, (x - 10, y - 15, 20, 15), 2)
                    pygame.draw.circle(self.game.screen, RED, (x, y - 15), 8, 2)
            
            instructions = self.game.small_font.render("LEFT/RIGHT: Select | SPACE/CLICK: Confirm | ESC: Back to Menu", True, YELLOW)
            inst_rect = instructions.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 50))
            self.game.screen.blit(instructions, inst_rect)
            
            pygame.display.flip()
            
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                
                if event.type == pygame.VIDEORESIZE:
                    self.game.handle_window_resize(event.w, event.h)
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        for i in range(selected - 1, -1, -1):
                            if self.game.unlocked_ships[i]:
                                if BUTTON_NAV:
                                    BUTTON_NAV.play()
                                selected = i
                                break
                    elif event.key == pygame.K_RIGHT:
                        for i in range(selected + 1, 3):
                            if self.game.unlocked_ships[i]:
                                if BUTTON_NAV:
                                    BUTTON_NAV.play()
                                selected = i
                                break
                    elif event.key == pygame.K_SPACE:
                        if self.game.unlocked_ships[selected]:
                            if BUTTON_CLICK:
                                BUTTON_CLICK.play()
                            selecting = False
                    elif event.key == pygame.K_ESCAPE:
                        if BUTTON_CLICK:
                            BUTTON_CLICK.play()
                        return None
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, ship_num, is_unlocked in ship_rects:
                            if rect.collidepoint(mouse_pos) and is_unlocked:
                                if ship_num == selected:
                                    if BUTTON_CLICK:
                                        BUTTON_CLICK.play()
                                    selecting = False
                                else:
                                    if BUTTON_NAV:
                                        BUTTON_NAV.play()
                                    selected = ship_num
        
        pygame.event.clear()
        return selected
