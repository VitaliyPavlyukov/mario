import os
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
from mario import Mario
from owl import Owl
from owl2 import Owl2
from cloud import Cloud
from button import Button
from player import Player
from statistic import Statistic


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
GREEN = (0, 200, 64)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
RED = (225, 0, 50)
GREEN_2 = (0, 225, 0)
BLUE = (0, 0, 225)

# Colours
BUTTON_NORMAL = (255, 100, 100)
BUTTON_HOVER = (100, 255, 100)
BUTTON_CLICKED = (100, 100, 255)


class MarioGame:
    """ Game """

    def __init__(self):
        self.number_rects = []
        self.screen_width = 0
        self.screen_height = 0
        self.line_step_width = 0
        self.line_step_height = 0
        self.backgrounds = []
        self.photo = None

    def default(self, screen):
        """ Базовые значения линейки """
        self.number_rects = []
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()
        self.line_step_width = self.screen_width // 10
        self.line_step_height = self.screen_height // 10

        for i in range(10):
            font = pygame.font.Font(None, 32)
            text = font.render(str(i) + ' (' + str(self.line_step_width * i) + ')', True, WHITE)
            number_rect = text.get_rect()
            number_rect.move_ip(self.line_step_width * i, self.screen_height - 25)
            self.number_rects.append((text, number_rect))

        for i in range(10):
            font = pygame.font.Font(None, 32)
            text = font.render(str(i) + ' (' + str(self.line_step_height * i) + ')', True, WHITE)
            number_rect = text.get_rect()
            number_rect.move_ip(5, self.line_step_height * i)
            self.number_rects.append((text, number_rect))

    def load_photo(self):
        """ Загрузка тестового фото """
        self.photo = pygame.image.load("images\\DSC_2998.jpg")
        self.photo = pygame.transform.scale(self.photo, (500, 300))

    def draw_photo(self, screen):
        """ Отрисовка тестового фото """
        screen.blit(self.photo, (1, 450))

    def draw_one_image(self, screen, frame_images):
        """ Отрисовка тестовой картинки """
        back_color = (147, 187, 236)
        my_images_zero = pygame.transform.scale(frame_images[0], (75, 100))
        my_images_zero.set_colorkey(back_color)
        screen.blit(my_images_zero, (1, 450))

    def draw_rect(self, screen):
        """ Отрисовка тестовой области """
        r1 = pygame.Rect((200, 50, 100, 75))
        pygame.draw.rect(screen, WHITE, (20, 20, 100, 75))
        pygame.draw.rect(screen, LIGHT_BLUE, r1, 8)

    def draw_lines(self, screen):
        """ Отрисовка тестовых линий """
        pygame.draw.line(screen, WHITE, [10, 30], [290, 15], 3)
        pygame.draw.line(screen, WHITE, [10, 50], [290, 35])
        pygame.draw.aaline(screen, WHITE, [10, 70], [290, 55])

        pygame.draw.lines(screen, WHITE, False,
                          [[0, screen.get_height()], [300, 300], [500, 500], [600, 700]], 5)

    def get_backgrounds(self):
        """ Фон """
        self.backgrounds = []
        back_images = [
            "images\\1700119323_pictures-pibig-info-p-multyashnaya-polyanka-pinterest-27.jpg",
            "images\\1683363757_furman-top-p-fon-polyanka-instagram-27.jpg",
            "images\\1684547321_polinka-top-p-multyashnaya-polyanka-kartinka-krasivo-35.jpg",
            "images\\1678084637_bogatyr-club-p-ramka-gribi-foni-oboi-50.jpg"
        ]

        for image in back_images:
            self.backgrounds.append(pygame.transform.scale(
                pygame.image.load(image), (1600, 800)))

    def main(self):
        pygame.init()

        window_size = (1600, 800)
        pygame.display.set_caption("Марио")
        screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
        color = (216, 233, 243)
        screen.fill(color)

        clock = pygame.time.Clock()

        # Загрузки объектов
        self.default(screen)
        self.get_backgrounds()
        self.load_photo()

        # Инициализация объектов
        ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(ADDCLOUD, 1000)

        clouds = pygame.sprite.Group()

        button_start = Button(text='Старт')
        button_start.set_init_pos(100, 720)
        button_jump = Button(text='Прыжок')
        button_jump.set_init_pos(200, 720)
        button_stop = Button(text='Стоп')
        button_stop.set_init_pos(300, 720)

        all_sprites = pygame.sprite.Group()

        player = Player()
        mario = Mario(screen)
        owl = Owl(screen)
        owl2 = Owl2(screen)
        statistic = Statistic()
        circles = []

        # запускаем основной цикл
        running = True
        while running:
            mouse = pygame.mouse.get_pos()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.VIDEORESIZE:
                    os.environ['SDL_VIDEO_WINDOW_POS'] = ''  # Clears the default window location
                    width, height = event.dict['size']
                    screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                    self.default(screen)
                    mario.set_screen(screen)

                button_start.update_event(event, mouse)
                button_jump.update_event(event, mouse)
                button_stop.update_event(event, mouse)

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        mario.rect.top -= 150

                        # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if event.button == 1:
                #         circles.append((RED, event.pos, 20))
                #     elif event.button == 3:
                #         pygame.draw.circle(screen, BLUE, event.pos, 20)
                #         pygame.draw.rect(screen, GREEN,
                #                      (event.pos[0] - 10,
                #                       event.pos[1] - 10, 20, 20))
                #         pygame.display.update()
                #     elif event.button == 2:
                #         screen.fill(WHITE)

                if event.type == ADDCLOUD:
                    new_cloud = Cloud(screen)
                    clouds.add(new_cloud)
                    all_sprites.add(new_cloud)

            if button_start.state == 'clicked':
                mario.stop = False
                mario.rect.top = 0
                mario.rect.left = 0

            if button_jump.state == 'clicked':
                mario.stop = False
                mario.rect.top -= 50

            if button_stop.state == 'clicked':
                if mario.stop:
                    mario.stop = False
                else:
                    mario.stop = True

            clouds.update()
            mario.animate_state(clock)
            mario.update()

            if mario.background_index > len(self.backgrounds) - 1:
                mario.background_index = 0

            screen.blit(self.backgrounds[mario.background_index], (0, 0))

            for entity in all_sprites:
                screen.blit(entity.surf, entity.rect)

            # выводим кадры, обновляем экран
            if not mario.stop:
                if mario.move_left:
                    if pygame.sprite.spritecollideany(mario, clouds):
                        if not mario.in_cloud:
                            statistic.cloud_count += 1
                            statistic.set_cloud(statistic.cloud_count)
                            mario.in_cloud = True

                        mario.rect.top -= 5
                        screen.blit(mario.my_image_6_1, mario.rect)
                    else:
                        if mario.rect.top == mario.default_rect_top:
                            mario.in_cloud = False

                        if mario.rect.top < mario.default_rect_top:
                            mario.rect.top += 5
                        else:
                            mario.rect.top = mario.default_rect_top
                        screen.blit(mario.current_frame, mario.rect)

                elif mario.move_right:
                    mario_surf = pygame.transform.flip(mario.current_frame, True, False)
                    back_color = (147, 187, 236)
                    mario_surf.set_colorkey(back_color)

                    if pygame.sprite.spritecollideany(mario, clouds):
                        screen.blit(mario.my_image_6_1, mario.rect)
                    else:
                        screen.blit(mario_surf, mario.rect)
            else:
                screen.blit(mario.surf, mario.rect)

            screen.blit(mario.stat_text, mario.stat_number_rect)

            owl2.animate_state(clock)
            owl2.update()
            screen.blit(owl2.current_frame, owl2.rect)

            screen.blit(statistic.surf, statistic.rect)
            screen.blit(statistic.text, statistic.place)

            screen.blit(button_start.surf, button_start.rect)
            screen.blit(button_start.surf_text, button_start.rect_text)
            screen.blit(button_jump.surf, button_jump.rect)
            screen.blit(button_jump.surf_text, button_jump.rect_text)
            screen.blit(button_stop.surf, button_stop.rect)
            screen.blit(button_stop.surf_text, button_stop.rect_text)

            for text, number_rect in self.number_rects:
                screen.blit(text, number_rect)

            # for color, left, top in circles:
            #     pygame.draw.circle(screen, color, left, top)

            # тестовые области
            # self.draw_rect(screen)

            # тестовые линии
            # self.draw_lines(screen)

            # тестовая картинка
            # self.draw_one_image(screen, mario.frame_images)

            # тестовое фото
            # self.draw_photo(screen)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = MarioGame()
    game.main()
