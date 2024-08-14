import pygame
import random
from pygame.locals import (
    K_DOWN,
    K_ESCAPE,
    K_LEFT,
    K_RIGHT,
    K_UP,
    KEYDOWN,
    QUIT,
    RLEACCEL,
)

class Cloud(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Cloud, self).__init__()
        self.window_height = screen.get_height()
        self.window_width = screen.get_width()
        self.surf = pygame.image.load("images\\cloud.png").convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(self.window_width + 20, self.window_width + 100),
                random.randint(0, self.window_height),
            )
        )

    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()