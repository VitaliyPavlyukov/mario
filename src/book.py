import pygame


class Page:
    def __init__(self, text):
        self.text = text
        self.lines = self.text_format(text)

    def text_format(self, text):
        lines = []
        line = ''

        for paragraph in text.split('\n'):
            lines.append(line)
            line = ''

            if len(paragraph) == 0:
                if len(lines) > 0:
                    if len(lines[-1]) > 0:
                        lines.append(line)
                        line = ''
                        continue

            for word in paragraph.split(' '):
                if len(line) > 40:
                    lines.append(line.strip())
                    line = word
                else:
                    line = line + ' ' + word + ' '

        return lines


class Book(pygame.sprite.Sprite):
    """ Книга """
    def __init__(self, width=500, height=600):
        super(Book, self).__init__()
        self.width = width
        self.height = height
        #self.surf = pygame.Surface((self.width, self.height))
        self.surf = pygame.transform.scale(pygame.image.load(
            "images\\1678145837_bogatyr-club-p-bloknot-maket-foni-pinterest-40.png"), (self.width, self.height))
        #self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect()
        self.rect.left = (1600 // 2) - (self.width // 2)
        self.rect.top = (800 // 2) - (self.height // 2)
        self.show = False
        self.pages = []
        self.current_page = None
        self.current_page_index = 0
        self.font = pygame.font.Font(None, 24)
        self.surf_text = self.font.render('', True, (0, 0, 0))
        self.rect_text = self.surf_text.get_rect()

        self.book_text = ''
        self.load_book_text()
        self.build_pages()
        self.set_page(0)

    def load_book_text(self):
        with open('book\\mario.txt', encoding='utf-8') as f:
            self.book_text = f.read()

    def build_pages(self):
        all_page = Page(self.book_text)

        page_index = 0
        line_step = 0
        lines = []
        for line in all_page.text_format(all_page.text):

            if len(line) == 0:
                continue

            line_step += 1
            lines.append(line)

            if line_step > 8:
                page = Page('')
                page.lines = lines
                self.pages.append(page)
                line_step = 0
                lines = []

    def set_page(self, value):
        if value > len(self.pages) - 1:
            value -= 1
        elif value < 0:
            value = 0

        self.current_page_index = value
        self.current_page = self.pages[self.current_page_index]
        self.surf_text = self.font.render(self.current_page.text, True, (0, 0, 0))
        self.rect_text.left = self.rect.left + 20  # + ((self.surf.get_width() - self.surf_text.get_width()) // 2)
        self.rect_text.top = self.rect.top + 100  # + ((self.surf.get_height() - self.surf_text.get_height()) // 2)
