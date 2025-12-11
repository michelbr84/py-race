
import pygame
from pygame.locals import *
from src.core.settings import COLOR_BG, COLOR_TEXT, LEVEL_PROFILES
from src.ui.settings_menu import SettingsMenu

class StartMenu:
    def __init__(self, screen, config_manager, score_manager):
        self.screen = screen
        self.config_manager = config_manager
        self.score_manager = score_manager
        
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.seed_input = str(pygame.time.get_ticks())
        self.input_active = False
        self.running = True
        self.selected_profile = "Custom"
        
        # Sounds
        from src.core.loader import load_sound
        self.snd_start = load_sound('start.mp3')
        
        self.layout_ui()
        
    def layout_ui(self):
        center_w = self.screen.get_width() // 2
        center_h = self.screen.get_height() // 2
        
        self.input_rect = pygame.Rect(center_w - 100, center_h - 25, 200, 50)
        
        # Level Select Rects
        self.btn_level = pygame.Rect(center_w - 100, center_h - 100, 200, 40)
        
        self.start_button = pygame.Rect(center_w - 75, center_h + 50, 150, 50)
        self.settings_button = pygame.Rect(center_w - 75, center_h + 120, 150, 40)
        
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            self.screen.fill(COLOR_BG)
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return None
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return None
                    
                    if self.selected_profile == "Custom" and self.input_active:
                        if event.key == K_RETURN:
                            self.snd_start.play()
                            self.running = False
                        elif event.key == K_BACKSPACE:
                            self.seed_input = self.seed_input[:-1]
                        else:
                            if len(self.seed_input) < 10:
                                self.seed_input += event.unicode
                                
                if event.type == MOUSEBUTTONDOWN:
                    # Input focus
                    if self.input_rect.collidepoint(event.pos) and self.selected_profile == "Custom":
                        self.input_active = True
                    else:
                        self.input_active = False
                        
                    # Play
                    if self.start_button.collidepoint(event.pos):
                        self.snd_start.play()
                        self.running = False
                        
                    # Settings
                    if self.settings_button.collidepoint(event.pos):
                        settings = SettingsMenu(self.screen, self.config_manager)
                        restart = settings.run()
                        if restart == "QUIT": return None
                        if restart: # Resolution changed
                            return "RESTART"
                        self.layout_ui() # Re-layout in case something else changed
                        
                    # Level Select Cycle
                    if self.btn_level.collidepoint(event.pos):
                        keys = list(LEVEL_PROFILES.keys())
                        curr_idx = keys.index(self.selected_profile)
                        next_idx = (curr_idx + 1) % len(keys)
                        self.selected_profile = keys[next_idx]
                        
                        # Set seed if profile is not custom
                        if LEVEL_PROFILES[self.selected_profile]:
                            self.seed_input = LEVEL_PROFILES[self.selected_profile]
                        
            # Render
            cx = self.screen.get_width() // 2
            
            # Title
            title = self.font.render("Race of Math", True, COLOR_TEXT)
            self.screen.blit(title, title.get_rect(center=(cx, 60)))
            
            # High Score
            hs_val = self.score_manager.get_high_score()
            hs_surf = self.small_font.render(f"High Score: {hs_val}", True, (255, 215, 0))
            self.screen.blit(hs_surf, hs_surf.get_rect(center=(cx, 100)))

            # Level Select
            pygame.draw.rect(self.screen, (60, 60, 60), self.btn_level)
            pygame.draw.rect(self.screen, COLOR_TEXT, self.btn_level, 2)
            lbl = self.small_font.render(f"Mode: {self.selected_profile}", True, (255, 255, 255))
            self.screen.blit(lbl, lbl.get_rect(center=self.btn_level.center))
            
            # Input Box
            if self.selected_profile == "Custom":
                color_input = (50, 50, 50) if not self.input_active else (80, 80, 80)
                pygame.draw.rect(self.screen, color_input, self.input_rect)
                pygame.draw.rect(self.screen, COLOR_TEXT, self.input_rect, 2)
                txt = self.small_font.render(self.seed_input, True, (255, 255, 255))
                self.screen.blit(txt, txt.get_rect(center=self.input_rect.center))
            else:
                # Show fixed seed dimmed
                txt = self.small_font.render(f"Seed: {self.seed_input}", True, (100, 100, 100))
                self.screen.blit(txt, txt.get_rect(center=self.input_rect.center))
            
            # Buttons
            self.draw_btn(self.start_button, "PLAY", (0, 100, 0))
            self.draw_btn(self.settings_button, "SETTINGS", (50, 50, 100))
            
            pygame.display.flip()
            clock.tick(30)
            
        return self.seed_input

    def draw_btn(self, rect, text, bg_color):
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        txt = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(txt, txt.get_rect(center=rect.center))
