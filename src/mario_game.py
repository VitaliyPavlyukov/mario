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

pygame.init()

window_size = (1600, 800)
screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
color = (216, 233, 243)
screen.fill(color)
#pygame.display.flip()
pygame.display.set_caption("Марио")
clock = pygame.time.Clock()

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

screen_width = screen.get_width()
screen_height = screen.get_height()
line_step_width = screen_width // 10
line_step_height = screen_height // 10
number_rects = []
r1 = pygame.Rect((200, 50, 100, 75))


def init():
    global number_rects
    number_rects = []
    global screen_width
    global screen_height
    global line_step_width
    global line_step_height

    screen_width = screen.get_width()
    screen_height = screen.get_height()
    line_step_width = screen_width // 10
    line_step_height = screen_height // 10

    for i in range(10):
        font = pygame.font.Font(None, 32)
        text = font.render(str(i) + ' (' + str(line_step_width * i) + ')', True, WHITE)
        number_rect = text.get_rect()
        number_rect.move_ip(line_step_width * i, screen_height - 25)
        number_rects.append((text, number_rect))

    for i in range(10):
        font = pygame.font.Font(None, 32)
        text = font.render(str(i) + ' (' + str(line_step_height * i) + ')', True, WHITE)
        number_rect = text.get_rect()
        number_rect.move_ip(5, line_step_height * i)
        number_rects.append((text, number_rect))


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()


class Statistic(pygame.sprite.Sprite):
    def __init__(self):
        super(Statistic, self).__init__()
        self.surf = pygame.Surface((400, 35))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.move_ip(200, 5)

        self.font = pygame.font.Font(None, 48)
        self.cloud_count = 0
        self.input_text = None
        self.text = self.font.render(self.input_text, True, (0, 100, 0))
        self.place = self.text.get_rect()
        self.place.move_ip(200, 5)
        self.set_cloud(0)

    def set_cloud(self, value):
        self.cloud_count = value
        self.input_text = f'Кол-во облаков: {self.cloud_count}'
        self.text = self.font.render(self.input_text, True, (0, 100, 0))

        #screen.blit(text, place)
        #pygame.display.update()


init()
backgrounds = []
back_images = [
"images\\1700119323_pictures-pibig-info-p-multyashnaya-polyanka-pinterest-27.jpg",
"images\\1683363757_furman-top-p-fon-polyanka-instagram-27.jpg",
"images\\1684547321_polinka-top-p-multyashnaya-polyanka-kartinka-krasivo-35.jpg",
"images\\1678084637_bogatyr-club-p-ramka-gribi-foni-oboi-50.jpg"
]
for image in back_images:
    backgrounds.append(pygame.transform.scale(
        pygame.image.load(image), (1600, 800)))

#photo = pygame.image.load("DSC_2998.jpg")
#photo = pygame.transform.scale(photo, (500, 300))

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
#all_sprites.add(mario)
circles = []

mouseClicked = False

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
            init()
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

    #if state == 'hover':
    #    pygame.draw.rect(screen, BUTTON_HOVER, button)
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

            # if state == 'hover':
    #     pygame.draw.rect(screen, BUTTON_HOVER, button)
    # elif state == 'clicked':
    #     pygame.draw.rect(screen, BUTTON_CLICKED, button)
    # else:
    #     pygame.draw.rect(screen, BUTTON_NORMAL, button)

    clouds.update()
    mario.animate_state(clock)
    mario.update()

    #mario_2.animate_state(clock)
    #mario_2.update()

    #screen.fill(color)

    if mario.background_index > len(backgrounds) - 1:
        mario.background_index = 0

    screen.blit(backgrounds[mario.background_index], (0, 0))

    #screen.blit(photo, (0, 0))

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
    #screen.blit(mario.stat_text, (mario.rect.left, mario.rect.top - 30, 100, 100))


    #back_color = (147, 187, 236)
    #my_images_zero = pygame.transform.scale(frame_images[0], (75, 100))
    #my_images_zero.set_colorkey(back_color)
    #screen.blit(my_images_zero, (1, 450))

    # screen.blit(owl.my_image_6_1, (1, 1))
    # screen.blit(owl.frame_images[0], (200, 1))
    # screen.blit(owl.frame_images[1], (200*2, 1))
    # screen.blit(owl.frame_images[2], (200 * 3, 1))
    # screen.blit(owl.frame_images[3], (200 * 4, 1))
    #
    # screen.blit(owl2.frame_images[0], (1, 1))
    # screen.blit(owl2.frame_images[1], (200, 300))
    # screen.blit(owl2.frame_images[2], (200 * 2, 300))
    # screen.blit(owl2.frame_images[3], (200 * 3, 300))
    # screen.blit(owl2.frame_images[4], (200 * 4, 300))

    owl2.animate_state(clock)
    owl2.update()
    screen.blit(owl2.current_frame, owl2.rect)

    screen.blit(statistic.surf, statistic.rect)
    screen.blit(statistic.text, statistic.place)

    #pygame.draw.rect(screen, WHITE, (20, 20, 100, 75))
    #pygame.draw.rect(screen, LIGHT_BLUE, r1, 8)
    screen.blit(button_start.surf, button_start.rect)
    screen.blit(button_start.surf_text, button_start.rect_text)
    screen.blit(button_jump.surf, button_jump.rect)
    screen.blit(button_jump.surf_text, button_jump.rect_text)
    screen.blit(button_stop.surf, button_stop.rect)
    screen.blit(button_stop.surf_text, button_stop.rect_text)

    #pygame.draw.line(screen, WHITE, [10, 30], [290, 15], 3)
    #pygame.draw.line(screen, WHITE, [10, 50], [290, 35])
    #pygame.draw.aaline(screen, WHITE, [10, 70], [290, 55])

    # pygame.draw.lines(screen, WHITE, False,
    #                   [[0, screen.get_height()], [300, 300], [500, 500], [600, 700]], 5)

    for text, number_rect in number_rects:
        screen.blit(text, number_rect)

    # for color, left, top in circles:
    #     pygame.draw.circle(screen, color, left, top)

    pygame.display.flip()
    #pygame.display.update(r1)
    #r1.top += 200
    #pygame.display.update(r1)


pygame.quit()
