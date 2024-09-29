import os
import pygame
from mario_game import MarioGame
from mario import Mario
from owl import Owl
from owl2 import Owl2
from cloud import Cloud
from button import Button
from player import Player
from statistic import Statistic
from book import Book


class Game:
    def __init__(self):
        self.init()
        self.window_size = (1600, 800)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)
        self.marioGame = MarioGame(self.screen)
        self.marioGame_running_flag = False
        #self.marioGame.main()
        self.font = pygame.font.Font(None, 32)

        self.button_start = Button(text='Марио')
        self.button_start.set_init_pos(100, 720)
        self.screen_color = (50, 50, 50)

    def init(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
        pygame.init()
        pygame.display.set_caption("Игры")

    def run(self):

        self.screen.fill(self.screen_color)

        clock = pygame.time.Clock()

        running = True
        while running:

            mouse = pygame.mouse.get_pos()

            events = pygame.event.get()

            if self.marioGame.running:
                self.marioGame.run(events)
            else:
                # Переключение один раз
                if self.marioGame_running_flag:
                    self.screen.fill(self.screen_color)
                self.marioGame_running_flag = False

            for event in events:

                if event.type == pygame.QUIT:
                    running = False

                #if event.type == pygame.KEYDOWN:
                #    if event.key == pygame.K_ESCAPE:
                #        running = False

                self.button_start.update_event(event, mouse)

            if self.button_start.state == 'clicked':
                self.marioGame.set_running(True)
                self.marioGame_running_flag = True
                self.button_start.state = 'normal'

            # Отрисовка без включенных игр
            if not self.marioGame.running:
                self.screen.blit(self.button_start.surf, self.button_start.rect)
                self.screen.blit(self.button_start.surf_text, self.button_start.rect_text)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
