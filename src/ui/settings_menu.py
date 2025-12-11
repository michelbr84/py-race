import pygame
from pygame.locals import *
from src.core.settings import COLOR_BG, COLOR_TEXT

class SettingsMenu:
    def __init__(self, screen, config_manager):
        self.screen = screen
        self.config_manager = config_manager
        self.font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 32)
        
        self.running = True
        self.restart_required = False
        
        self.layout_ui()
        
    def layout_ui(self):
        center_w = self.screen.get_width() // 2
        center_h = self.screen.get_height() // 2
        
        # Current Config
        self.current_res = self.config_manager.get("resolution")
        self.current_vol = self.config_manager.get("volume")
        
        # UI Elements
        self.lbl_res = self.small_font.render(f"Resolution: {self.current_res[0]}x{self.current_res[1]}", True, COLOR_TEXT)
        self.btn_res_800 = pygame.Rect(center_w - 200, center_h - 100, 120, 40)
        self.btn_res_1024 = pygame.Rect(center_w - 60, center_h - 100, 120, 40)
        self.btn_res_1280 = pygame.Rect(center_w + 80, center_h - 100, 120, 40)
        
        self.lbl_vol = self.small_font.render(f"Volume: {int(self.current_vol*100)}%", True, COLOR_TEXT)
        self.btn_vol_down = pygame.Rect(center_w - 100, center_h, 50, 40)
        self.btn_vol_up = pygame.Rect(center_w + 50, center_h, 50, 40)
        
        self.btn_back = pygame.Rect(center_w - 75, center_h + 100, 150, 50)
        
        # Restart warning
        self.lbl_restart = self.small_font.render("Restart required for Resolution changes", True, (255, 100, 100))

    def run(self):
        clock = pygame.time.Clock()
        
        while self.running:
            self.screen.fill(COLOR_BG)
            
            # Events
            for event in pygame.event.get():
                if event.type == QUIT:
                    return "QUIT"
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.running = False
                
                if event.type == MOUSEBUTTONDOWN:
                    # Resolution
                    new_res = None
                    if self.btn_res_800.collidepoint(event.pos): new_res = [800, 600]
                    elif self.btn_res_1024.collidepoint(event.pos): new_res = [1024, 768]
                    elif self.btn_res_1280.collidepoint(event.pos): new_res = [1280, 720]
                    
                    if new_res:
                        self.config_manager.save_config("resolution", new_res)
                        self.current_res = new_res
                        self.restart_required = True
                        self.layout_ui() # Refresh labels
                        
                    # Volume
                    new_vol = self.current_vol
                    if self.btn_vol_down.collidepoint(event.pos): new_vol = max(0.0, self.current_vol - 0.1)
                    elif self.btn_vol_up.collidepoint(event.pos): new_vol = min(1.0, self.current_vol + 0.1)
                    
                    if new_vol != self.current_vol:
                        self.current_vol = new_vol
                        self.config_manager.save_config("volume", self.current_vol)
                        if pygame.mixer and pygame.mixer.get_init():
                            # Update all channels? Or just master if possible? Pygame sound volume works per sound obj usually.
                            # For simplicity we assume calling code will check config, but let's try to set it roughly?
                            pass
                        self.layout_ui()
                        
                    # Back
                    if self.btn_back.collidepoint(event.pos):
                        self.running = False

            # Render
            cx = self.screen.get_width() // 2
            
            # Title
            title = self.font.render("Settings", True, COLOR_TEXT)
            self.screen.blit(title, title.get_rect(center=(cx, 50)))
            
            # Resolution
            self.screen.blit(self.lbl_res, (cx - 100, self.btn_res_800.y - 40))
            self.draw_btn(self.btn_res_800, "800x600")
            self.draw_btn(self.btn_res_1024, "1024x768")
            self.draw_btn(self.btn_res_1280, "1280x720")
            
            if self.restart_required:
                self.screen.blit(self.lbl_restart, self.lbl_restart.get_rect(center=(cx, self.btn_res_800.y - 70)))
            
            # Volume
            self.screen.blit(self.lbl_vol, (cx - 60, self.btn_vol_down.y - 40))
            self.draw_btn(self.btn_vol_down, "-")
            self.draw_btn(self.btn_vol_up, "+")
            
            # Back
            self.draw_btn(self.btn_back, "BACK")
            
            pygame.display.flip()
            clock.tick(30)
            
        return self.restart_required

    def draw_btn(self, rect, text):
        pygame.draw.rect(self.screen, (50, 50, 50), rect)
        pygame.draw.rect(self.screen, COLOR_TEXT, rect, 2)
        txt_surf = self.small_font.render(text, True, (255, 255, 255))
        self.screen.blit(txt_surf, txt_surf.get_rect(center=rect.center))
