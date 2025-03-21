import os
import pygame


class Tree(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/tree.png')).convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.name = 'Дерево'
		self.size = 1
		self.done = 0

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))


class TreeSmall(pygame.sprite.Sprite):
	def __init__(self, pos, base_path=''):
		super().__init__()
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/tree.png')).convert_alpha()
		self.default_pos = pos
		self.rect = self.image.get_rect(center=pos)
		self.name = 'Дерево'
		self.size = 1
		self.done = 0

	def transform(self):
		self.image = pygame.transform.scale(self.image, (50, 50))
		self.rect = self.image.get_rect(topleft=self.default_pos)
