import os
import pygame


class House(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/Summer-Medieval-City-2D-Tileset2.png')).convert_alpha()
		self.image = self.clip(self.image, 165, 0, 308, 326)
		self.image = pygame.transform.scale(self.image, (308, 326))
		self.image.set_colorkey((47, 50, 47))

		self.rect = self.image.get_rect(topleft=pos)
		self.name = 'Дом'
		self.size = 1
		self.done_tree_count = 0
		self.done_gold_count = 0
		self.mouse_selected = False

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))

	def clip(self, surface, x, y, x_size, y_size):
		handle_surface = surface.copy()
		clipRect = pygame.Rect(x, y, x_size, y_size)
		handle_surface.set_clip(clipRect)
		image = surface.subsurface(handle_surface.get_clip())
		return image.copy()
