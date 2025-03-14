import pygame
from random import randint

class Alphs:
    """ Массив букв """
    def __init__(self, x_pos=10, y_pos=10):
        self.alph = ('а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'к', 'л', 'м', 'н',
                     'о', 'п', 'р', 'с', 'т')
        self.alph_states = []
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.font = pygame.font.Font(None, 24)
    def draw(self, sc, current_frame_index, alph_count):
        """ Отрисовка массива букв """

        if len(self.alph_states) == 0:
            for i in range(alph_count):
                self.alph_states.append(self.alph[randint(0, len(self.alph) - 1)])

        if current_frame_index == 0:
            self.alph_states = []
            for i in range(alph_count):
                self.alph_states.append(self.alph[randint(0, len(self.alph) - 1)])

        for i in range(alph_count):
            surf_text = self.font.render(str(self.alph_states[i]), True, (255, 255, 255))
            sc.blit(surf_text, (self.x_pos + i * 50, self.y_pos))