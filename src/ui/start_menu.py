
import pygame
from pygame.locals import *
from src.core.settings import COLOR_BG, COLOR_TEXT

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.seed_input = str(pygame.time.get_ticks()) # Default random seed-ish
        self.input_active = False
        self.running = True
        
        center_w = self.screen.get_width() // 2
        center_h = self.screen.get_height() // 2
        
        # Rects
        self.input_rect = pygame.Rect(center_w - 100, center_h - 25, 200, 50)
        self.start_button = pygame.Rect(center_w - 75, center_h + 50, 150, 50)
        
        # Sounds
        from src.core.loader import load_sound
        self.snd_start = load_sound('start.mp3')
        
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
                    
                    if self.input_active:
                        if event.key == K_RETURN:
                            self.snd_start.play()
                            self.running = False # Start game
                        elif event.key == K_BACKSPACE:
                            self.seed_input = self.seed_input[:-1]
                        else:
                            # Limit chars
                            if len(self.seed_input) < 10:
                                self.seed_input += event.unicode
                                
                if event.type == MOUSEBUTTONDOWN:
                    if self.input_rect.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
                        
                    if self.start_button.collidepoint(event.pos):
                        self.snd_start.play()
                        self.running = False
            
            # Render Title
            title_surf = self.font.render("Race of Math - Seed Select", True, COLOR_TEXT)
            title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height()//2 - 100))
            self.screen.blit(title_surf, title_rect)
            
            # Render Input
            color_input = (50, 50, 50) if not self.input_active else (80, 80, 80)
            pygame.draw.rect(self.screen, color_input, self.input_rect)
            pygame.draw.rect(self.screen, COLOR_TEXT, self.input_rect, 2)
            
            input_surf = self.small_font.render(self.seed_input, True, (255, 255, 255))
            input_rect = input_surf.get_rect(center=self.input_rect.center)
            self.screen.blit(input_surf, input_rect)
            
            # Render Button
            pygame.draw.rect(self.screen, (0, 100, 0), self.start_button)
            pygame.draw.rect(self.screen, COLOR_TEXT, self.start_button, 2)
            
            btn_surf = self.small_font.render("PLAY", True, (255, 255, 255))
            btn_rect = btn_surf.get_rect(center=self.start_button.center)
            self.screen.blit(btn_surf, btn_rect)
            
            # Instructions
            hint_surf = self.small_font.render("Click box to edit seed. Enter to play.", True, (150, 150, 150))
            hint_rect = hint_surf.get_rect(center=(self.screen.get_width()//2, self.screen.get_height() - 50))
            self.screen.blit(hint_surf, hint_rect)
            
            pygame.display.flip()
            clock.tick(30)
            
        return self.seed_input
