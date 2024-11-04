import os
import pygame


class HouseGoldMine(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/zolotaja_shakhta.png')).convert_alpha()
		self.image = pygame.transform.scale(self.image, (308, 326))
		self.rect = self.image.get_rect(topleft=pos)
		self.name = 'Золотая шахта'
		self.visible = True
		self.size = 1
		self.gold_count = 10
		self.done_tree_count = 0
		self.mouse_selected = False

	def check_visible(self):
		if self.gold_count == 0:
			self.visible = False

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))

	def clip(self, surface, x, y, x_size, y_size):
		handle_surface = surface.copy()
		clipRect = pygame.Rect(x, y, x_size, y_size)
		handle_surface.set_clip(clipRect)
		image = surface.subsurface(handle_surface.get_clip())
		return image.copy()
