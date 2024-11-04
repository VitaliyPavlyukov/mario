import os
import pygame


class HouseGoldMine(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/zolotaja_shakhta.png')).convert_alpha()
		#self.image = self.clip(self.image, 165, 0, 308, 326)
		self.image = pygame.transform.scale(self.image, (308, 326))
		#self.image.set_colorkey((47, 50, 47))

		self.rect = self.image.get_rect(topleft=pos)
		self.name = 'Дом'
		self.size = 1
		self.done_tree_count = 0
		self.mouse_selected = False

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))

	def clip(self, surface, x, y, x_size, y_size):  # Get a part of the image
		handle_surface = surface.copy()  # Sprite that will get process later
		clipRect = pygame.Rect(x, y, x_size, y_size)  # Part of the image
		handle_surface.set_clip(clipRect)  # Clip or you can call cropped
		image = surface.subsurface(handle_surface.get_clip())  # Get subsurface
		return image.copy()  # Return
