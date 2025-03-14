import pygame
from random import randint

class Circles:
    """ Круги """

    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    GRAY = (125, 125, 125)
    LIGHT_BLUE = (64, 128, 255)
    YELLOW = (225, 225, 0)
    PINK = (230, 50, 230)
    GREEN_2 = (0, 225, 0)
    def __init__(self, x_pos=50, y_pos=50, radius=40):
        self.colors = [Circles.WHITE, Circles.BLUE, Circles.GREEN, Circles.RED,
                       Circles.GRAY, Circles.LIGHT_BLUE, Circles.YELLOW, Circles.PINK, Circles.GREEN_2]
        self.colors_states = []
        self.colors_states_list = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius

    def int_parts(self, value: int, step: int):
        """ Разбиение числа на равные части """

        parts = []
        part = value // step
        for i in range(step):
            parts.append(part * i)

        return parts
    def draw(self, sc, FPS, current_frame_index, lines_count, circle_count):
        """ Отрисовка массива кругов разных цветов """

        fps_parts = self.int_parts(value=FPS, step=4)

        if current_frame_index in fps_parts:
            self.colors_states_list = []

        for x in range(lines_count):
            if len(self.colors_states) == 0:
                for i in range(circle_count):
                    self.colors_states.append(self.colors[randint(0, len(self.colors) - 1)])

            if current_frame_index in fps_parts:
                self.colors_states = []
                for i in range(circle_count):
                    self.colors_states.append(self.colors[randint(0, len(self.colors) - 1)])

            self.colors_states_list.append(self.colors_states)

        for k in range(lines_count):
            for i in range(circle_count):
                pygame.draw.circle(sc, self.colors_states_list[k][i], (self.x_pos + (i * 100), self.y_pos + 100 * k), self.radius)
