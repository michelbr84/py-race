
import pygame
from pygame.locals import *
from src.core.settings import COLOR_BG, COLOR_TEXT

class PauseMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        
        self.layout_ui()
        
    def layout_ui(self):
        center_w = self.screen.get_width() // 2
        center_h = self.screen.get_height() // 2
        
        self.btn_resume = pygame.Rect(center_w - 100, center_h - 30, 200, 50)
        self.btn_menu = pygame.Rect(center_w - 100, center_h + 40, 200, 50)
        self.btn_quit = pygame.Rect(center_w - 100, center_h + 110, 200, 50)
        
    def run(self):
        # We need to capture the current screen to use as background if we want "overlay" effect.
        # But for simplicity, we'll just fill a semi-transparent surface or simple color.
        
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        running = True
        while running:
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "QUIT"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "RESUME" # Toggle back
                if event.type == MOUSEBUTTONDOWN:
                    if self.btn_resume.collidepoint(event.pos):
                        return "RESUME"
                    if self.btn_menu.collidepoint(event.pos):
                        return "MENU"
                    if self.btn_quit.collidepoint(event.pos):
                        return "QUIT"
            
            # Draw UI on top of existing screen (which we blitted only once? No, need to re-blit if we clear?)
            # Actually, standard Pygame loop clears screen.
            # So let's just draw a solid Pause Screen for stability.
            self.screen.fill((50, 50, 50)) 
            
            cx = self.screen.get_width() // 2
            cy = self.screen.get_height() // 2

            title = self.font.render("PAUSED", True, COLOR_TEXT)
            self.screen.blit(title, title.get_rect(center=(cx, cy - 100)))
            
            self.draw_btn(self.btn_resume, "RESUME", (0, 100, 0))
            self.draw_btn(self.btn_menu, "MAIN MENU", (50, 50, 100))
            self.draw_btn(self.btn_quit, "QUIT", (100, 0, 0))
            
            pygame.display.flip()
            pygame.time.Clock().tick(30)
            
        return "QUIT"

    def draw_btn(self, rect, text, bg_color):
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        txt = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(txt, txt.get_rect(center=rect.center))
