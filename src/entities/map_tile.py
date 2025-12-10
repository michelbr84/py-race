
import pygame
from src.core.settings import *

class MapTile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, rot):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()

        if rot != 0:
            self.image = pygame.transform.rotate(self.image, rot * 90)

        self.x = x
        self.y = y

    # Realign the map
    def update(self, cam_x, cam_y):
        self.rect.topleft = self.x - cam_x, self.y - cam_y
