import pygame


class Page:
    def __init__(self, text):
        self.text = text


class Book(pygame.sprite.Sprite):
    """ Книга """
    def __init__(self):
        super(Book, self).__init__()
        self.surf = pygame.Surface((300, 200))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.left = 100
        self.rect.top = 70
        self.show = False
        self.pages = []
        self.current_page = None
        self.current_page_index = 0
        self.pages.append(Page('Первая страница'))
        self.pages.append(Page('Вторая страница'))
        self.pages.append(Page('Третья страница'))

        self.font = pygame.font.Font(None, 24)
        self.surf_text = self.font.render('', True, (0, 0, 0))
        self.rect_text = self.surf_text.get_rect()
        self.set_page(0)

    def set_page(self, value):
        if value > len(self.pages) - 1:
            value -= 1
        elif value < 0:
            value = 0

        self.current_page_index = value
        self.current_page = self.pages[self.current_page_index]
        self.surf_text = self.font.render(self.current_page.text, True, (0, 0, 0))
        self.rect_text.left = self.rect.left + ((self.surf.get_width() - self.surf_text.get_width()) // 2)
        self.rect_text.top = self.rect.top + ((self.surf.get_height() - self.surf_text.get_height()) // 2)
