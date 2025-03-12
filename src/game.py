import os
import pygame
from mario_game.mario_game import MarioGame
from game_settler.main import SettlerGame
from mario_game.button import Button

os.environ['SDL_VIDEO_CENTERED'] = '1'

class Game:
    def __init__(self):
        self.init()
        self.displayInfo = pygame.display.Info()  # You have to call this before pygame.display.set_mode()
        print(self.displayInfo.current_w, self.displayInfo.current_h)
        #print('displayInfo', self.displayInfo)
        #self.screen_width, screen_height = info.current_w, info.current_h
        self.window_size = (0, 0) #scaled 1707 960
        self.screen = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.OPENGL)

        self.clock = pygame.time.Clock()

        self.mario_game = MarioGame(self.screen)
        self.marioGame_running_flag = False
        self.settler_game = SettlerGame(self.screen, self.clock, base_path='game_settler')
        self.settler_game_running_flag = False

        self.font = pygame.font.Font(None, 32)

        self.button_mario_start = Button(text='Марио')
        self.button_mario_start.set_init_pos(100, 650)

        self.button_camera_start = Button(text='Поселенцы', width=130)
        self.button_camera_start.set_init_pos(100, 690)

        self.screen_color = (50, 50, 50)

    def init(self):
        pygame.mixer.pre_init(44100, -16, 1, 512)  # важно вызвать до pygame.init()
        pygame.init()
        pygame.display.set_caption("Игры")

    def games_stop(self):
        self.marioGame_running_flag = False
        self.settler_game_running_flag = False

    def is_games_running(self):
        if self.marioGame_running_flag:
            return True
        if self.settler_game_running_flag:
            return True

        return False

    def run(self):

        self.screen.fill(self.screen_color)
        fullscreen = False

        drivers = pygame.display.get_driver()
        print('drivers', drivers)

        running = True
        while running:

            mouse = pygame.mouse.get_pos()
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

                if not self.marioGame_running_flag and not self.settler_game.running:
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

            if self.settler_game.running:
                self.settler_game.run(events)
            else:
                # Переключение один раз
                if self.settler_game_running_flag:
                    self.screen.fill(self.screen_color)
                self.settler_game_running_flag = False

            if self.button_mario_start.state == 'clicked':
                self.mario_game.set_running(True)
                self.marioGame_running_flag = True
                self.button_mario_start.state = 'normal'

            if self.button_camera_start.state == 'clicked':
                self.settler_game.set_running(True)
                self.settler_game_running_flag = True
                self.button_camera_start.state = 'normal'

            # Отрисовка без включенных игр
            if not self.is_games_running():
                self.screen.blit(self.button_mario_start.surf, self.button_mario_start.rect)
                self.screen.blit(self.button_mario_start.surf_text, self.button_mario_start.rect_text)

                self.screen.blit(self.button_camera_start.surf, self.button_camera_start.rect)
                self.screen.blit(self.button_camera_start.surf_text, self.button_camera_start.rect_text)

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
