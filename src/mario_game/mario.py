import pygame
import random


def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pygame.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return


class Mario(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Mario, self).__init__()
        self.my_image = pygame.image.load("mario_game/images/Custom Edited - Mario Customs - Mario Dexters Laboratory Robot Rampage-Style.png")
        self.back_color = (147, 187, 236)
        self.frame_images = []
        self.screen = screen

        for i in range(0, 5):
            image_one = clip(self.my_image, (17 * i) + 1, 0 + 1, 16, 24)
            scaled_image = pygame.transform.scale(image_one, (75, 100))
            scaled_image.set_colorkey(self.back_color)
            self.frame_images.append(scaled_image)

        self.my_image_6_1 = clip(self.my_image, (17 * 0) + 1, 24 * 5 + 1 * 5 + 1, 16, 24)
        self.my_image_6_1 = pygame.transform.scale(self.my_image_6_1, (75, 100))
        self.my_image_6_1.set_colorkey(self.back_color)

        self.move_left = True
        self.move_right = False
        self.stop = False

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
        self.default_rect_top = self.screen.get_height() - 300
        self.rect.move_ip(0, self.default_rect_top)
        self.rect.top = int(self.window_height * 0.85) - int(self.frame_height / 2)

        self.in_cloud = False

        self.background_index = 0

        self.stat_font = pygame.font.Font(None, 32)
        self.stat_message = '0'
        self.stat_text = self.stat_font.render(str(self.rect.left), True, (255, 255, 255))
        self.stat_number_rect = self.stat_text.get_rect()

    def set_screen(self, screen):
        self.screen = screen
        self.window_height = screen.get_height()
        self.window_width = screen.get_width()

    def animate_state(self, clock):
        # обновление состояния
        time_delta = clock.tick(60) / 1000.0
        self.animation_timer += time_delta
        if self.animation_timer >= 1.0 / self.animation_speed:
            self.current_frame_index = (self.current_frame_index + 1) % self.animation_length
            self.animation_timer -= 1.0 / self.animation_speed

    def update(self):
        if self.stop:
            return

        self.current_frame = self.frame_images[self.current_frame_index]
        self.surf = self.current_frame

        if self.move_left:
            self.rect.left += 2  # сдвигаем кадр вправо
        if self.move_right:
            self.rect.left -= 2  # сдвигаем кадр влево

        if self.move_left:
            if self.rect.left > self.window_width:
                #self.move_left = False
                #self.move_right = True
                self.rect.left = 0
                self.background_index += 1

        self.stat_message = str(self.rect.left) + '/' + str(self.rect.top)
        self.stat_text = self.stat_font.render(self.stat_message, True, (255, 255, 255))
        self.stat_number_rect = self.stat_text.get_rect()
        self.stat_number_rect.move_ip(self.rect.left + 5, self.rect.top - 30)

        # if self.move_right:
        #     if self.frame_position[0] < 0:
        #         self.move_left = True
        #         self.move_right = False
