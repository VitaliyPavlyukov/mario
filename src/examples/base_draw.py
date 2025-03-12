import pygame
from random import randint

def get_int_parts(value:int, step:int):
    """ Разбиение числа на равные части"""

    parts = []
    part = value // step
    for i in range(step):
        parts.append(part * i)

    return parts


pygame.init()

BLACK = (0, 0, 0)
W, H = 1700, 1000

sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

GRAY = (125, 125, 125)
LIGHT_BLUE = (64, 128, 255)
YELLOW = (225, 225, 0)
PINK = (230, 50, 230)
GREEN_2 = (0, 225, 0)

COLORS = [WHITE, BLUE, GREEN, RED,
          GRAY, LIGHT_BLUE, YELLOW, PINK, GREEN_2]

COLORS_states = []
COLORS_states_list = []

ALPH = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'к', 'л', 'м', 'н',
        'о', 'п', 'р', 'с', 'т']
ALPH_states = []

current_frame_index = 0
font = pygame.font.Font(None, 24)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    current_frame_index += 1

    if FPS == current_frame_index:
        current_frame_index = 0

    sc.fill(BLACK)

    pygame.draw.rect(sc, WHITE, (10, 10, 50, 100))
    pygame.draw.rect(sc, BLUE, (100, 10, 50, 100), 2)

    pygame.draw.line(sc, GREEN, (200, 20), (350, 50))
    pygame.draw.aaline(sc, GREEN, (200, 40), (350, 70))

    pygame.draw.lines(sc, RED, True, [(200, 80), (250, 80), (300, 200)], 2)
    pygame.draw.aalines(sc, RED, True, [(300, 80), (350, 80), (400, 200)], 2)

    pygame.draw.polygon(sc, WHITE, [[150, 210], [180, 250], [90, 290], [30, 230]])
    pygame.draw.polygon(sc, WHITE, [[150, 310], [180, 350], [90, 390], [30, 330]], 1)

    pygame.draw.circle(sc, BLUE, (300, 250), 40)

    # Массив кругов разных цветов
    fps_parts = get_int_parts(value=FPS, step=4)
    lines_count = 3
    circle_count = 10

    if current_frame_index in fps_parts:
        COLORS_states_list = []

    for x in range(lines_count):
        if len(COLORS_states) == 0:
            for i in range(circle_count):
                COLORS_states.append(COLORS[randint(0, len(COLORS) - 1)])

        if current_frame_index in fps_parts:
            COLORS_states = []
            for i in range(circle_count):
                COLORS_states.append(COLORS[randint(0, len(COLORS) - 1)])

        COLORS_states_list.append(COLORS_states)

    for k in range(lines_count):
        for i in range(circle_count):
            pygame.draw.circle(sc, COLORS_states_list[k][i], (50 + (i * 100), 500 + 100 * k), 40)

    # Массив букв
    alph_count = 20
    if len(ALPH_states) == 0:
        for i in range(alph_count):
            ALPH_states.append(ALPH[randint(0, len(ALPH) - 1)])

    if current_frame_index == 0:
        ALPH_states = []
        for i in range(alph_count):
            ALPH_states.append(ALPH[randint(0, len(ALPH) - 1)])

    for i in range(alph_count):
        surf_text = font.render(str(ALPH_states[i]), True, (255, 255, 255))
        sc.blit(surf_text, (10 + i * 50, 800))

    pygame.draw.ellipse(sc, BLUE, (300, 300, 100, 50), 1)

    pi = 3.14
    pygame.draw.arc(sc, RED, (450, 30, 50, 150), pi, 2 * pi, 5)

    pygame.display.update()

    clock.tick(FPS)


"""
    pygame.draw.rect(surface, …) – прямоугольник;
    pygame.draw.line(surface, …) – линия;
    pygame.draw.aaline(surface, …) – сглаженная линия;
    pygame.draw.lines(surface, …) – ломаная линия;
    pygame.draw.aalines(surface, …) – ломаная сглаженная линия;
    pygame.draw.polygon(surface, …) – полигон;
    pygame.draw.circle(surface, …) – круг;
    pygame.draw.ellipse(surface, …) – эллипс;
    pygame.draw.arc(surface, …) – дуга. 
"""