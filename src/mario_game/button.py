import pygame


class Button(pygame.sprite.Sprite):
    """ Кнопка с текстом """

    color_WHITE = (255, 255, 255)
    color_BLACK = (0, 0, 0)
    color_GRAY = (125, 125, 125)
    color_LIGHT_BLUE = (64, 128, 255)
    color_GREEN = (0, 200, 64)
    color_YELLOW = (225, 225, 0)
    color_PINK = (230, 50, 230)
    color_RED = (225, 0, 50)
    color_GREEN_2 = (0, 225, 0)
    color_BLUE = (0, 0, 225)

    def __init__(self, text, width=75, height=25, alpha=128):
        super(Button, self).__init__()
        self.text = text
        self.width = width
        self.height = height
        self.backcolor = Button.color_WHITE
        self.surf = pygame.Surface((self.width, self.height))
        self.surf.set_alpha(alpha)
        self.surf.fill(self.backcolor)
        self.rect = self.surf.get_rect()
        self.mouseClicked = False
        self.state = 'normal'
        self.font = pygame.font.Font(None, 24)
        self.surf_text = self.font.render(self.text, True, Button.color_BLACK)
        self.rect_text = self.surf_text.get_rect()
        self.begin_left = 0
        self.begin_top = 0
        self.text_position = 'center'

        self.set_init_pos(0, 0)

    def set_backcolor(self, color):
        """ Установка фона """

        self.backcolor = color
        self.surf.fill(self.backcolor)

    def set_init_pos(self, left, top, text_position='center'):
        """ Установка первоначальной позиции """

        self.text_position = text_position
        self.rect.left = left
        self.rect.top = top

        self.rect_text.top = self.rect.top + ((self.surf.get_height() - self.surf_text.get_height()) // 2)

        if self.text_position == 'left':
            self.rect_text.left = self.rect.left + 5
        elif self.text_position == 'center':
            self.rect_text.left = self.rect.left + ((self.surf.get_width() - self.surf_text.get_width()) // 2)
        else:
            self.rect_text.left = self.rect.left + ((self.surf.get_width() - self.surf_text.get_width()) // 2)

    def set_text(self, text):
        """ Установка текста """

        self.text = text
        self.surf_text = self.font.render(self.text, True, Button.color_BLACK)
        self.rect_text = self.surf_text.get_rect()
        self.set_init_pos(self.rect.left, self.rect.top)

    def update_event(self, events, mouse):
        """ Обновление состояния """

        self.mouseClicked = False

        for event in events:
            if self.rect.collidepoint(mouse):
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # mouse button down
                    self.set_backcolor(Button.color_BLUE)
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    # mouse button up
                    self.set_backcolor(Button.color_WHITE)
                    self.mouseClicked = True

            if self.rect.collidepoint(mouse) and self.mouseClicked:
                self.state = 'clicked'
            elif self.rect.collidepoint(mouse):
                self.state = 'hover'
                self.set_backcolor(Button.color_GREEN)
            else:
                self.set_backcolor(Button.color_WHITE)
                self.state = 'normal'

    def clicked(self):
        """ Проверка нажата ли кнопка """
        return self.state == 'clicked'

    def set_not_clicked(self):
        """ Убирается нажатие кнопки в нормальное состояние """
        self.state = 'normal'

    def draw(self, screen, events):
        """ Отрисовка """

        mouse = pygame.mouse.get_pos()
        self.update_event(events, mouse)
        screen.blit(self.surf, self.rect)
        screen.blit(self.surf_text, self.rect_text)
