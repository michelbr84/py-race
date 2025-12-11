
import pygame
from src.core.settings import COLOR_TEXT

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color=(255, 255, 255), size=24, duration=60):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.Font(None, size)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.timer = duration
        self.speed = 1.0
        
    def update(self, *args):
        # args might be camera offset, we don't strictly need it if we are UI-layer
        # But if we want text attached to world, we need to shift it.
        # Let's assume these are World Coordinates and we shift them?
        # Or UI coordinates?
        # Let's make them World Coordinates so they stay where the event happened.
        
        # Move up
        self.rect.y -= self.speed
        self.timer -= 1
        
        # Fade out? Pygame surfaces support alpha.
        if self.timer < 20:
            alpha = int((self.timer / 20) * 255)
            self.image.set_alpha(alpha)
            
        if self.timer <= 0:
            self.kill()

class TextManager:
    def __init__(self):
        self.group = pygame.sprite.Group()
        
    def add(self, x, y, text, color=(255, 255, 255)):
        self.group.add(FloatingText(x, y, text, color))
        
    def update(self, cam_x, cam_y):
        # Floating texts are world objects but we render them.
        # If we just call update, they move.
        # But for rendering they need to be offset by cam.
        # We can cheat: FloatingText updates its RECT logic. 
        # But we need a custom draw method or use the sprite group draw but modify rects temporarily?
        # Or, easier: We pass cam_x, cam_y to update and they adjust their rect?
        # No, update shouldn't move rect based on camera, update moves world pos.
        # Let's make FloatingText purely UI overlay for now (simpler), or Map-relative?
        # Map-relative is cooler.
        self.group.update()
        
    def draw(self, screen, cam_x, cam_y):
        for sprite in self.group:
            # Calculate Screen Pos
            screen_pos = (sprite.rect.x - cam_x, sprite.rect.y - cam_y)
            screen.blit(sprite.image, screen_pos)
