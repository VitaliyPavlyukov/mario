import pygame
import random


def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return


class Owl2(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Owl2, self).__init__()
        #self.my_image = pygame.image.load("1687335158_bogatyr-club-p-tri-sovi-foni-pinterest-52.jpg")
        self.back_color = (255, 255, 255)
        self.frame_images = []

        for i in range(0, 10):
            image_loaded = pygame.image.load(f"mario_game/images/ezgif-1-cdd76a59ca-gif-im/frame_0{str(i)}_delay-0.04s.gif")
            #image_one = clip(self.my_image, 1500*i, 100, 1350, 1600)
            scaled_image = pygame.transform.scale(image_loaded, (200, 200))
            scaled_image.set_colorkey(self.back_color)
            scaled_image = pygame.transform.flip(scaled_image, True, False)
            self.frame_images.append(scaled_image)

        self.move_left = True
        self.move_right = False

        # вычисляем позицию для вывода кадров в зависимости от высоты окна
        self.window_height = screen.get_height()
        self.window_width = screen.get_width()
        self.frame_height = self.frame_images[0].get_height()

        # параметры анимации
        self.animation_length = len(self.frame_images)
        self.animation_speed = 15  # кадры в секунду
        self.current_frame_index = 0
        self.animation_timer = 0

        self.current_frame = self.frame_images[self.current_frame_index]

        self.rect = self.current_frame.get_rect()
        self.surf = self.frame_images[self.current_frame_index]
        self.rect.move_ip(200, 500)
        self.rect.top = 200

    def animate_state(self, clock):
        # обновление состояния
        time_delta = clock.tick(60) / 1000.0
        self.animation_timer += time_delta
        if self.animation_timer >= 1.0 / self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % self.animation_length
            self.animation_timer -= 1.0 / self.animation_speed

    def update(self):
        self.current_frame = self.frame_images[self.current_frame_index]
        self.surf = self.current_frame

        if self.move_left:
            self.rect.left += 2  # сдвигаем кадр вправо
        if self.move_right:
            self.rect.left -= 2  # сдвигаем кадр влево

        if self.move_left:
            if self.rect.left > self.window_width:
                self.move_left = False
                self.move_right = True

        if self.move_right:
            if self.rect.left < 0:
                self.move_left = True
                self.move_right = False