import os
import pygame
import datetime


class Worker(pygame.sprite.Sprite):
    def __init__(self, pos, group, type, base_path=''):
        super().__init__(group)

        self.type = type
        self.base_path = base_path
        self.image = None
        self.image_index = 0
        self.rect = None

        self.images = []
        self.get_images(self.type, self.base_path, pos)
        self.image_change_prev_time = datetime.datetime.now()

        self.direction = pygame.math.Vector2()
        self.speed = 5  # default 5

        self.tree_selected = None
        self.gold_selected = None
        self.mouse_selected = False

        self.wait_seconds = 2
        self.prev_time = datetime.datetime.now()
        self.paused = False

    def get_images(self, type, base_path, pos):
        if type:
            if type == 'GoldMiner':
                for i in range(0, 5):
                    p_image = pygame.image.load(os.path.join(base_path, 'graphics/gold-miner.png')).convert_alpha()
                    p_image = self.clip(p_image, 150 + (i * 200), 0, 210, 350)
                    p_image = pygame.transform.scale(p_image, (80, 130))
                    p_image.set_colorkey((255, 255, 255))
                    self.images.append(p_image)
                self.image = self.images[0]
            else:
                self.image = pygame.image.load(os.path.join(base_path, 'graphics/player.png')).convert_alpha()
        else:
            self.image = pygame.image.load(os.path.join(base_path, 'graphics/player.png')).convert_alpha()

        self.rect = self.image.get_rect(center=pos)

    def has_pause(self):
        if self.paused:
            now = datetime.datetime.now()
            if (now - self.prev_time).total_seconds() >= self.wait_seconds:
                self.prev_time = now
                self.paused = False

        return self.paused

    def set_pause(self):
        self.paused = True
        self.prev_time = datetime.datetime.now()

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
        self.direction.x = 0
        self.direction.y = 0

        if len(self.images) > 0:
            now = datetime.datetime.now()
            if self.set_image_pause():
                if self.image_index < len(self.images):
                    self.image = self.images[self.image_index]
                    self.image_index += 1
                else:
                    self.image = self.images[0]
                    self.image_index = 0

    def set_image_pause(self):
        now = datetime.datetime.now()
        if (now - self.image_change_prev_time).total_seconds()*1000 >= 100:
            self.image_change_prev_time = now
            return True
        return False

    def clip(self, surface, x, y, x_size, y_size):  # Get a part of the image
        handle_surface = surface.copy()  # Sprite that will get process later
        clipRect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
        handle_surface.set_clip(clipRect)  # Clip or you can call cropped
        image = surface.subsurface(handle_surface.get_clip())  # Get subsurface
        return image.copy()  # Return