import os
import pygame


class HouseGoldMine(pygame.sprite.Sprite):
	""" Золотая шахта """
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.name = 'Золотая шахта'
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/zolotaja_shakhta.png')).convert_alpha()
		self.max_width = 308
		self.max_height = 326
		self.image = pygame.transform.scale(self.image, (self.max_width, self.max_height))
		self.default_rect_center = pos
		self.rect = self.image.get_rect(center=self.default_rect_center)
		self.visible = True
		self.size = 1
		self.max_gold_count = 2
		self.gold_count = 2
		self.done_tree_count = 0
		self.done = 0
		self.mouse_selected = False

	def check_visible(self):
		if self.gold_count == 0:
			self.visible = False
			self.done = 1

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))

	def transform_by_gold_count(self):
		self.image = pygame.transform.scale(self.image, (self.max_width // self.max_gold_count * self.gold_count,
														 self.max_height // self.max_gold_count * self.gold_count))
		self.rect = self.image.get_rect(center=self.default_rect_center)

	def clip(self, surface, x, y, x_size, y_size):
		handle_surface = surface.copy()
		clipRect = pygame.Rect(x, y, x_size, y_size)
		handle_surface.set_clip(clipRect)
		image = surface.subsurface(handle_surface.get_clip())
		return image.copy()

	def update(self):
		self.transform_by_gold_count()


class HouseGoldMineSmall(pygame.sprite.Sprite):
	""" Золотая шахта """
	def __init__(self, pos, base_path=''):
		super().__init__()
		self.name = 'Золотая шахта'
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/zolotaja_shakhta.png')).convert_alpha()
		self.max_width = 308
		self.max_height = 326
		self.image = pygame.transform.scale(self.image, (self.max_width, self.max_height))
		self.default_rect_center = pos
		self.rect = self.image.get_rect(center=self.default_rect_center)
		self.visible = True
		self.size = 1
		self.mouse_selected = False

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect(center=self.default_rect_center)
