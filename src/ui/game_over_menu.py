
import pygame
from pygame.locals import *
from src.core.settings import COLOR_BG, COLOR_TEXT

class GameOverMenu:
    def __init__(self, screen, score, high_score_reached):
        self.screen = screen
        self.score = score
        self.high_score_reached = high_score_reached
        
        self.font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 32)
        
        self.running = True
        self.result = None # "RESTART", "MENU", "QUIT"
        
        self.layout_ui()
        
    def layout_ui(self):
        center_w = self.screen.get_width() // 2
        center_h = self.screen.get_height() // 2
        
        self.btn_restart = pygame.Rect(center_w - 100, center_h + 20, 200, 50)
        self.btn_menu = pygame.Rect(center_w - 100, center_h + 90, 200, 50)
        self.btn_quit = pygame.Rect(center_w - 100, center_h + 160, 200, 50)
        
    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            # Semi-transparent background over the game?
            # Or just solid fill. Let's do solid fill for simplicity or overlay if we can.
            # Since main loop stops rendering game, we need to redraw or just fill.
            self.screen.fill((50, 0, 0)) # Dark red tint
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "QUIT"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return "MENU" 
                if event.type == MOUSEBUTTONDOWN:
                    if self.btn_restart.collidepoint(event.pos):
                        return "RESTART"
                    if self.btn_menu.collidepoint(event.pos):
                        return "MENU"
                    if self.btn_quit.collidepoint(event.pos):
                        return "QUIT"

            cx = self.screen.get_width() // 2
            cy = self.screen.get_height() // 2

            # Title
            title = self.font.render("GAME OVER", True, (255, 50, 50))
            self.screen.blit(title, title.get_rect(center=(cx, cy - 100)))
            
            # Score
            score_txt = self.small_font.render(f"Final Score: {self.score}", True, (255, 255, 255))
            self.screen.blit(score_txt, score_txt.get_rect(center=(cx, cy - 40)))
            
            if self.high_score_reached:
                hs_txt = self.small_font.render("NEW HIGH SCORE!", True, (255, 215, 0))
                self.screen.blit(hs_txt, hs_txt.get_rect(center=(cx, cy - 10)))
            
            # Buttons
            self.draw_btn(self.btn_restart, "PLAY AGAIN", (0, 100, 0))
            self.draw_btn(self.btn_menu, "MAIN MENU", (50, 50, 100))
            self.draw_btn(self.btn_quit, "QUIT", (100, 0, 0))
            
            pygame.display.flip()
            clock.tick(30)
            
        return "QUIT"

    def draw_btn(self, rect, text, bg_color):
        pygame.draw.rect(self.screen, bg_color, rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        txt = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(txt, txt.get_rect(center=rect.center))
