import pygame

pygame.init()

BLACK = (0, 0, 0)
W, H = 1000, 570

sc = pygame.display.set_mode((W, H))

clock = pygame.time.Clock()
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    clock.tick(FPS)
