import os
import pygame


class Worker(pygame.sprite.Sprite):
    def __init__(self, pos, group, base_path=''):
        super().__init__(group)
        self.image = pygame.image.load(os.path.join(base_path, 'graphics/player.png')).convert_alpha()
        self.rect = self.image.get_rect(center=pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5  # default 5

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0

    def move(self, direction):

        if direction == 'down':
            self.direction.y = 1
        if direction == 'up':
            self.direction.y = -1
        if direction == 'right':
            self.direction.x = 1
        if direction == 'left':
            self.direction.x = -1
        if direction == 'stop':
            self.direction.y = 0
            self.direction.x = 0

    def update(self):
        # self.input()
        if self.direction != 1:
            self.rect.center += self.direction * self.speed
