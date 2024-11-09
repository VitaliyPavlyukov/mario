import os
import pygame


class Gold(pygame.sprite.Sprite):
    def __init__(self, pos, group, base_path=''):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join(base_path, 'graphics/gold.png')).convert_alpha()
        self.transform()
        self.rect = self.image.get_rect(topleft=pos)
        self.name = 'Золото'
        self.size = 1
        self.done = 0
        self.visible = False

    def transform(self):
        self.image = pygame.transform.scale(self.image, (50, 50))

    def update(self):
        pass
