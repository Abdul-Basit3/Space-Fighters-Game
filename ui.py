"""
UI screens and menus
"""
import pygame
import math
from constants import *
from assets import BACKGROUNDS, PLAYER_SHIPS

class UI:
    """Handles all UI screens and menus"""
    
    def __init__(self, game):
        """Initialize UI with reference to game"""
        self.game = game
        
    def show_splash_screen(self):
        """Display the game splash screen with title and animation"""
        splash_duration = 3000
        start_time = pygame.time.get_ticks()
        
        title_font = pygame.font.Font(None, 80)
        subtitle_font = pygame.font.Font(None, 36)
        
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
            
            scaled_bg = pygame.transform.scale(BACKGROUNDS[0], (self.game.screen_width, self.game.screen_height))
            self.game.screen.blit(scaled_bg, (0, 0))
            
            overlay = pygame.Surface((self.game.screen_width, self.game.screen_height))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.game.screen.blit(overlay, (0, 0))
            
            if progress < 0.5:
                alpha = int(255 * (progress * 2))
            else:
                alpha = 255
            
            title_text = "SPACE FIGHTERS"
            
            # Glow layers
            for offset in range(3, 0, -1):
                glow_surf = title_font.render(title_text, True, CYAN)
                glow_surf.set_alpha(alpha // (offset + 1))
                glow_rect = glow_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 - 50))
                glow_rect.inflate_ip(offset * 4, offset * 4)
                self.game.screen.blit(glow_surf, glow_rect)
            
            title_surf = title_font.render(title_text, True, WHITE)
            title_surf.set_alpha(alpha)
            title_rect = title_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 - 50))
            self.game.screen.blit(title_surf, title_rect)
            
            if progress > 0.3:
                subtitle_alpha = int(255 * ((progress - 0.3) / 0.7))
                subtitle_surf = subtitle_font.render("Prepare for Battle", True, YELLOW)
                subtitle_surf.set_alpha(subtitle_alpha)
                subtitle_rect = subtitle_surf.get_rect(center=(self.game.screen_width // 2, self.game.screen_height // 2 + 30))
                self.game.screen.blit(subtitle_surf, subtitle_rect)
            
            if progress > 0.5:
                skip_alpha = int(128 + 127 * math.sin(progress * math.pi * 8))
                skip_surf = self.game.small_font.render("Press any key to continue", True, WHITE)
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
                        waiting = False
                    elif allow_restart:
                        if event.key == pygame.K_r:
                            return "restart"
                        elif event.key == pygame.K_q:
                            return "quit"
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
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
        selected_level = min(self.game.highest_level_reached, 3)
        
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
            
            level_positions = [
                (self.game.screen_width // 4, self.game.screen_height // 2),
                (self.game.screen_width // 2, self.game.screen_height // 2),
                (3 * self.game.screen_width // 4, self.game.screen_height // 2)
            ]
            
            level_rects = []
            for i in range(3):
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
                
                pygame.draw.circle(self.game.screen, color, (x, y), 50, 5 if not is_selected else 8)
                
                level_text = self.game.font.render(str(level_num), True, color)
                level_rect = level_text.get_rect(center=(x, y))
                self.game.screen.blit(level_text, level_rect)
                
                click_rect = pygame.Rect(x - 50, y - 50, 100, 100)
                level_rects.append((click_rect, level_num, is_accessible))
                
                if is_completed:
                    status = self.game.small_font.render("COMPLETED", True, GREEN)
                elif not is_accessible:
                    status = self.game.small_font.render("LOCKED", True, (150, 150, 150))
                else:
                    status = self.game.small_font.render("AVAILABLE", True, WHITE)
                
                status_rect = status.get_rect(center=(x, y + 70))
                self.game.screen.blit(status, status_rect)
                
                if i < 2:
                    next_x, next_y = level_positions[i + 1]
                    line_color = GREEN if self.game.completed_levels[i] else (100, 100, 100)
                    pygame.draw.line(self.game.screen, line_color, (x + 50, y), (next_x - 50, next_y), 3)
            
            inst1 = self.game.small_font.render("Use LEFT/RIGHT arrows or CLICK to select level", True, YELLOW)
            inst1_rect = inst1.get_rect(center=(self.game.screen_width // 2, self.game.screen_height - 80))
            self.game.screen.blit(inst1, inst1_rect)
            
            inst2 = self.game.small_font.render("Press SPACE or CLICK to start level", True, YELLOW)
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
                                selected_level = i
                                break
                    elif event.key == pygame.K_RIGHT:
                        for i in range(selected_level + 1, 4):
                            if i <= self.game.highest_level_reached:
                                selected_level = i
                                break
                    elif event.key == pygame.K_SPACE:
                        selecting = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, level_num, is_accessible in level_rects:
                            if rect.collidepoint(mouse_pos) and is_accessible:
                                if level_num == selected_level:
                                    selecting = False
                                else:
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
                        unlock_text = self.game.small_font.render("Complete Level 2", True, RED)
                    unlock_rect = unlock_text.get_rect(center=(x, y + 85))
                    self.game.screen.blit(unlock_text, unlock_rect)
                    
                    pygame.draw.rect(self.game.screen, RED, (x - 10, y - 15, 20, 15), 2)
                    pygame.draw.circle(self.game.screen, RED, (x, y - 15), 8, 2)
            
            instructions = self.game.small_font.render("Use LEFT/RIGHT arrows or CLICK to select, SPACE/CLICK to confirm", True, YELLOW)
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
                                selected = i
                                break
                    elif event.key == pygame.K_RIGHT:
                        for i in range(selected + 1, 3):
                            if self.game.unlocked_ships[i]:
                                selected = i
                                break
                    elif event.key == pygame.K_SPACE:
                        if self.game.unlocked_ships[selected]:
                            selecting = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        for rect, ship_num, is_unlocked in ship_rects:
                            if rect.collidepoint(mouse_pos) and is_unlocked:
                                if ship_num == selected:
                                    selecting = False
                                else:
                                    selected = ship_num
        
        pygame.event.clear()
        return selected
