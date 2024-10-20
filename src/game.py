import os
import pygame
from mario_game import MarioGame
from examples.Pygame_Cameras_main.camera import CameraGame
import sys
#sys.path.append('examples\\Pygame_Cameras_main')
from button import Button


class Game:
    def __init__(self):
        self.init()
        self.window_size = (1600, 800)
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE)

        self.mario_game = MarioGame(self.screen)
        self.marioGame_running_flag = False
        self.сamera_game = CameraGame(self.screen, base_path='examples\\Pygame_Cameras_main')
        self.сamera_game_running_flag = False

        self.font = pygame.font.Font(None, 32)

        self.button_mario_start = Button(text='Марио')
        self.button_mario_start.set_init_pos(100, 650)

        self.button_camera_start = Button(text='Камера')
        self.button_camera_start.set_init_pos(100, 690)

        self.screen_color = (50, 50, 50)

    def init(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
        pygame.init()
        pygame.display.set_caption("Игры")

    def games_stop(self):
        self.marioGame_running_flag = False
        self.сamera_game_running_flag = False

    def is_games_running(self):
        if self.marioGame_running_flag:
            return True
        if self.сamera_game_running_flag:
            return True

        return False

    def run(self):

        self.screen.fill(self.screen_color)

        clock = pygame.time.Clock()

        running = True
        while running:

            mouse = pygame.mouse.get_pos()
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    running = False

                if not self.marioGame_running_flag and not self.сamera_game.running:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

                self.button_mario_start.update_event(event, mouse)
                self.button_camera_start.update_event(event, mouse)

            if self.mario_game.running:
                self.mario_game.run(events)
            else:
                # Переключение один раз
                if self.marioGame_running_flag:
                    self.screen.fill(self.screen_color)
                self.marioGame_running_flag = False

            if self.сamera_game.running:
                self.сamera_game.run(events)
            else:
                # Переключение один раз
                if self.сamera_game_running_flag:
                    self.screen.fill(self.screen_color)
                self.сamera_game_running_flag = False

            if self.button_mario_start.state == 'clicked':
                self.mario_game.set_running(True)
                self.marioGame_running_flag = True
                self.button_mario_start.state = 'normal'

            if self.button_camera_start.state == 'clicked':
                self.сamera_game.set_running(True)
                self.сamera_game_running_flag = True
                self.button_camera_start.state = 'normal'

            # Отрисовка без включенных игр
            if not self.is_games_running():
                self.screen.blit(self.button_mario_start.surf, self.button_mario_start.rect)
                self.screen.blit(self.button_mario_start.surf_text, self.button_mario_start.rect_text)

                self.screen.blit(self.button_camera_start.surf, self.button_camera_start.rect)
                self.screen.blit(self.button_camera_start.surf_text, self.button_camera_start.rect_text)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
