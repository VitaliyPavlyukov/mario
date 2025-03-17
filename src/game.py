import os
import pygame
from mario_game.mario_game import MarioGame
from game_settler.main import SettlerGame
from mario_game.button import Button

os.environ['SDL_VIDEO_CENTERED'] = '1'


class Game:
    def __init__(self):
        self.init()
        self.displayInfo = pygame.display.Info()
        print(self.displayInfo.current_w, self.displayInfo.current_h)

        self.window_size = (0, 0) #scaled 1707 960
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.OPENGL)

        self.clock = pygame.time.Clock()

        self.games = {'Mario': MarioGame(self.screen),
                      'Settler': SettlerGame(self.screen, self.clock, base_path='game_settler')
                      }

        self.font = pygame.font.Font(None, 32)

        self.button_mario_start = Button(text='Марио', width=130, alpha=255)
        self.button_mario_start.set_init_pos(100, 650, 'center')

        self.button_camera_start = Button(text='Поселенцы', width=130, alpha=255)
        self.button_camera_start.set_init_pos(100, 690,'center')

        self.screen_color = (50, 50, 50)

    def init(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
        pygame.init()
        pygame.display.set_caption("Игры")

    def games_stop(self):
        for key in self.games.keys():
            self.games[key].running = False

    def is_games_running(self):
        for _, game in self.games.items():
            if game.running:
                return True

        return False

    def run(self):

        self.screen.fill(self.screen_color)
        fullscreen = False

        drivers = pygame.display.get_driver()
        print('drivers', drivers)

        running = True
        while running:
            events = pygame.event.get()

            for event in events:

                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F11:  # enter/exit fullscreen upon pressing F11
                        if not fullscreen:
                            # 2560 1440
                            # 1920 1080
                            self.screen = pygame.display.set_mode((2560, 1440), pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE )
                            fullscreen = True
                        else:
                            self.screen = pygame.display.set_mode(self.window_size)
                            fullscreen = False

                if not self.is_games_running():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            running = False

            for key, value_game in self.games.items():
                if value_game.running:
                    value_game.run(events)

            if self.button_mario_start.clicked():
                self.games['Mario'].set_running(True)
                self.games['Mario'].running = True
                self.button_mario_start.set_not_clicked()

            if self.button_camera_start.clicked():
                self.games['Settler'].set_running(True)
                self.games['Settler'].running = True
                self.button_camera_start.set_not_clicked()

            # Отрисовка без включенных игр
            if not self.is_games_running():
                self.screen.fill(self.screen_color)
                self.button_mario_start.draw(self.screen, events)
                self.button_camera_start.draw(self.screen, events)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
