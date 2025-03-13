import pygame
from elements.curcles import Circles
from elements.alphs import Alphs

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

circles = Circles(x_pos=50, y_pos=500, radius=40)
alphs = Alphs(x_pos=10, y_pos=800)

current_frame_index = 0
font = pygame.font.Font(None, size=24)

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
    circles.draw(sc, FPS, current_frame_index, 3, 10)

    # Массив букв
    alphs.draw(sc, current_frame_index, 20)

    pygame.draw.ellipse(sc, BLUE, (300, 300, 100, 50), 1)

    pi = 3.14
    pygame.draw.arc(sc, RED, (450, 30, 50, 150), pi, 2 * pi, 5)

    pygame.display.update()

    clock.tick(FPS)
