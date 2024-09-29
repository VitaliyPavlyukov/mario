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
from book import Book


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

    def __init__(self, screen):
        self.running = False
        self.screen = screen

        self.number_rects = []
        self.screen_width = 0
        self.screen_height = 0
        self.line_step_width = 0
        self.line_step_height = 0
        self.backgrounds = []
        self.photo = None
        self.sound_collision = None

        # pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
        # pygame.init()
        self.sound_collision = pygame.mixer.Sound("sounds/Collision.ogg")

        self.window_size = (1600, 800)
        pygame.display.set_caption("Марио")
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        color = (216, 233, 243)
        self.screen.fill(color)

        self.clock = pygame.time.Clock()

        # Загрузки объектов
        self.default(self.screen)
        self.get_backgrounds()
        self.load_photo()

        # Инициализация объектов
        self.ADDCLOUD = pygame.USEREVENT + 2
        pygame.time.set_timer(self.ADDCLOUD, 1000)

        self.clouds = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()

        self.player = Player()
        self.mario = Mario(self.screen)
        self.owl = Owl(self.screen)
        self.owl2 = Owl2(self.screen)
        self.statistic = Statistic()
        self.book = Book()
        self.book.set_page(0)
        self.circles = []

        self.button_start = Button(text='Старт')
        self.button_start.set_init_pos(100, 720)
        self.button_jump = Button(text='Прыжок')
        self.button_jump.set_init_pos(200, 720)
        self.button_stop = Button(text='Стоп')
        self.button_stop.set_init_pos(300, 720)
        self.button_book_show = Button(text='Книга')
        self.button_book_show.set_init_pos(400, 720)

        self.button_book_right = Button(text='-->')
        self.button_book_right.set_init_pos(self.book.rect.left + (self.book.width / 2),
                                            self.book.rect.top + self.book.height + 5)
        self.button_book_page_num = Button(text='1', width=25, height=25)
        self.button_book_page_num.set_init_pos(self.book.rect.left + (self.book.width / 2) - 25,
                                               self.book.rect.top + self.book.height + 5)
        self.button_book_left = Button(text='<--')
        self.button_book_left.set_init_pos(self.book.rect.left + (self.book.width / 2) - 100,
                                           self.book.rect.top + self.book.height + 5)
        self.button_book_exit = Button(text='X', width=25, height=25)
        self.button_book_exit.set_init_pos(self.book.rect.right - self.button_book_exit.width - 1,
                                           self.book.rect.top + 1)

    def set_running(self, value):
        self.running = value

        if self.running:
            pygame.mixer.music.load('sounds/track_09.mp3')
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.5)
        else:
            pygame.mixer.music.stop()

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

    def run(self, events):

        if not self.running:
            return

        mouse = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.QUIT:
                self.set_running(False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_running(False)

            if event.type == pygame.VIDEORESIZE:
                os.environ['SDL_VIDEO_WINDOW_POS'] = ''  # Clears the default window location
                width, height = event.dict['size']
                self.screen = pygame.display.set_mode(event.dict['size'], pygame.RESIZABLE)
                self.default(self.screen)
                self.mario.set_screen(self.screen)

            self.button_start.update_event(event, mouse)
            self.button_jump.update_event(event, mouse)
            self.button_stop.update_event(event, mouse)
            self.button_book_show.update_event(event, mouse)
            self.button_book_exit.update_event(event, mouse)
            self.button_book_left.update_event(event, mouse)
            self.button_book_right.update_event(event, mouse)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.mario.rect.top -= 200

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

            if event.type == self.ADDCLOUD:
                new_cloud = Cloud(self.screen)
                self.clouds.add(new_cloud)
                self.all_sprites.add(new_cloud)

        if self.button_start.state == 'clicked':
            self.mario.stop = False
            self.mario.rect.top = 0
            self.mario.rect.left = 0
            self.button_start.state = 'normal'

        if self.button_jump.state == 'clicked':
            self.mario.stop = False
            self.mario.rect.top -= 200
            self.button_jump.state = 'normal'

        if self.button_stop.state == 'clicked':
            if self.mario.stop:
                self.mario.stop = False
            else:
                self.mario.stop = True
            self.button_stop.state = 'normal'

        if self.button_book_show.state == 'clicked':
            self.book.show = True
            self.button_book_show.state = 'normal'

        if self.button_book_exit.state == 'clicked':
            self.book.show = False
            self.button_book_exit.state = 'normal'

        if self.button_book_right.state == 'clicked':
            self.book.set_page(self.book.current_page_index + 1)
            self.button_book_right.state = 'normal'
            self.button_book_page_num.set_text(str(self.book.current_page_index + 1))

        if self.button_book_left.state == 'clicked':
            self.book.set_page(self.book.current_page_index - 1)
            self.button_book_left.state = 'normal'
            self.button_book_page_num.set_text(str(self.book.current_page_index + 1))

        self.clouds.update()
        self.mario.animate_state(self.clock)
        self.mario.update()

        if self.mario.background_index > len(self.backgrounds) - 1:
            self.mario.background_index = 0

        self.screen.blit(self.backgrounds[self.mario.background_index], (0, 0))

        for entity in self.all_sprites:
            self.screen.blit(entity.surf, entity.rect)

        # выводим кадры, обновляем экран
        if not self.mario.stop:
            if self.mario.move_left:
                if pygame.sprite.spritecollideany(self.mario, self.clouds):
                    if not self.mario.in_cloud:
                        self.statistic.cloud_count += 1
                        self.statistic.set_cloud(self.statistic.cloud_count)
                        self.mario.in_cloud = True
                        self.sound_collision.play()

                    self.mario.rect.top -= 5
                    self.screen.blit(self.mario.my_image_6_1, self.mario.rect)
                else:
                    if self.mario.rect.top == self.mario.default_rect_top:
                        self.mario.in_cloud = False

                    if self.mario.rect.top < self.mario.default_rect_top:
                        self.mario.rect.top += 5
                    else:
                        self.mario.rect.top = self.mario.default_rect_top
                    self.screen.blit(self.mario.current_frame, self.mario.rect)
                    self.sound_collision.stop()

            elif self.mario.move_right:
                self.mario_surf = pygame.transform.flip(self.mario.current_frame, True, False)
                back_color = (147, 187, 236)
                self.mario_surf.set_colorkey(back_color)

                if pygame.sprite.spritecollideany(self.mario, self.clouds):
                    self.screen.blit(self.mario.my_image_6_1, self.mario.rect)
                else:
                    self.screen.blit(self.mario_surf, self.mario.rect)
        else:
            self.screen.blit(self.mario.surf, self.mario.rect)

        self.screen.blit(self.mario.stat_text, self.mario.stat_number_rect)

        self.owl2.animate_state(self.clock)
        self.owl2.update()
        self.screen.blit(self.owl2.current_frame, self.owl2.rect)

        self.screen.blit(self.statistic.surf, self.statistic.rect)
        self.screen.blit(self.statistic.text, self.statistic.place)

        self.screen.blit(self.button_start.surf, self.button_start.rect)
        self.screen.blit(self.button_start.surf_text, self.button_start.rect_text)
        self.screen.blit(self.button_jump.surf, self.button_jump.rect)
        self.screen.blit(self.button_jump.surf_text, self.button_jump.rect_text)
        self.screen.blit(self.button_stop.surf, self.button_stop.rect)
        self.screen.blit(self.button_stop.surf_text, self.button_stop.rect_text)
        self.screen.blit(self.button_book_show.surf, self.button_book_show.rect)
        self.screen.blit(self.button_book_show.surf_text, self.button_book_show.rect_text)

        for text, number_rect in self.number_rects:
            self.screen.blit(text, number_rect)

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

        if self.book.show:
            self.screen.blit(self.book.surf, self.book.rect)
            # self.screen.blit(book.surf_text, book.rect_text)
            for i, line in enumerate(self.book.current_page.lines):
                font = pygame.font.Font(None, 24)
                surf_text = font.render(line, True, (0, 0, 0))
                self.screen.blit(surf_text, (self.book.rect.left + 50, self.book.rect.top + 100 + (50 * i)))

            self.screen.blit(self.button_book_right.surf, self.button_book_right.rect)
            self.screen.blit(self.button_book_right.surf_text, self.button_book_right.rect_text)

            self.screen.blit(self.button_book_page_num.surf, self.button_book_page_num.rect)
            self.screen.blit(self.button_book_page_num.surf_text, self.button_book_page_num.rect_text)

            self.screen.blit(self.button_book_left.surf, self.button_book_left.rect)
            self.screen.blit(self.button_book_left.surf_text, self.button_book_left.rect_text)

            self.screen.blit(self.button_book_exit.surf, self.button_book_exit.rect)
            self.screen.blit(self.button_book_exit.surf_text, self.button_book_exit.rect_text)

        #pygame.display.flip()

        #pygame.quit()


def main():
    pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
    pygame.init()
    window_size = (1600, 800)
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    game = MarioGame(screen)
    game.set_running(True)

    running = True
    while running:
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        game.run(events)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
