import pygame


class Statistic(pygame.sprite.Sprite):
    """ Статистика """

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
