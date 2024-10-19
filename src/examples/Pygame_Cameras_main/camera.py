import pygame
import sys
import os
from random import randint


class Tree(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/tree.png')).convert_alpha()
		self.rect = self.image.get_rect(topleft=pos)
		self.name = 'Дерево'
		self.size = 1


class Player(pygame.sprite.Sprite):
	def __init__(self, pos, group, base_path=''):
		super().__init__(group)
		self.image = pygame.image.load(os.path.join(base_path, 'graphics/player.png')).convert_alpha()
		self.rect = self.image.get_rect(center=pos)
		self.direction = pygame.math.Vector2()
		self.speed = 20  # default 5

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[pygame.K_UP]:
			self.direction.y = -1
		elif keys[pygame.K_DOWN]:
			self.direction.y = 1
		else:
			self.direction.y = 0

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
		else:
			self.direction.x = 0

	def update(self):
		self.input()
		self.rect.center += self.direction * self.speed


class CameraGroup(pygame.sprite.Group):
	def __init__(self, base_path=''):
		super().__init__()
		self.display_surface = pygame.display.get_surface()

		self.test_stat = None
		self.test_ground_offset = None
		self.test_tree = None
		self.test_scaled_tree_rect = None
		self.test_tree_selected_index = None

		# camera offset 
		self.offset = pygame.math.Vector2()
		self.half_w = self.display_surface.get_size()[0] // 2
		self.half_h = self.display_surface.get_size()[1] // 2

		# box setup
		self.camera_borders = {'left': 100, 'right': 100, 'top': 100, 'bottom': 100}
		l = self.camera_borders['left']
		t = self.camera_borders['top']
		w = self.display_surface.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
		h = self.display_surface.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
		self.camera_rect = pygame.Rect(l, t, w, h)

		# ground
		self.ground_surf = pygame.image.load(os.path.join(base_path, 'graphics/ground.png')).convert_alpha()
		self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

		# camera speed
		self.keyboard_speed = 5
		self.mouse_speed = 0.2

		# zoom 
		self.zoom_scale = 1
		self.internal_surf_size = (2500, 2500)
		self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
		self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
		self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
		self.internal_offset = pygame.math.Vector2()
		self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
		self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

	def center_target_camera(self, target):
		self.offset.x = target.rect.centerx - self.half_w
		self.offset.y = target.rect.centery - self.half_h

	def box_target_camera(self, target):

		if target.rect.left < self.camera_rect.left:
			self.camera_rect.left = target.rect.left
		if target.rect.right > self.camera_rect.right:
			self.camera_rect.right = target.rect.right
		if target.rect.top < self.camera_rect.top:
			self.camera_rect.top = target.rect.top
		if target.rect.bottom > self.camera_rect.bottom:
			self.camera_rect.bottom = target.rect.bottom

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a]: self.camera_rect.x -= self.keyboard_speed
		if keys[pygame.K_d]: self.camera_rect.x += self.keyboard_speed
		if keys[pygame.K_w]: self.camera_rect.y -= self.keyboard_speed
		if keys[pygame.K_s]: self.camera_rect.y += self.keyboard_speed

		self.offset.x = self.camera_rect.left - self.camera_borders['left']
		self.offset.y = self.camera_rect.top - self.camera_borders['top']

	def mouse_control(self):
		mouse = pygame.math.Vector2(pygame.mouse.get_pos())
		mouse_offset_vector = pygame.math.Vector2()

		left_border = self.camera_borders['left']
		top_border = self.camera_borders['top']
		right_border = self.display_surface.get_size()[0] - self.camera_borders['right']
		bottom_border = self.display_surface.get_size()[1] - self.camera_borders['bottom']

		self.test_stat = mouse_offset_vector

		if top_border < mouse.y < bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector.x = mouse.x - left_border
				#pygame.mouse.set_pos((left_border, mouse.y))
			if mouse.x > right_border:
				mouse_offset_vector.x = mouse.x - right_border
				#pygame.mouse.set_pos((right_border, mouse.y))
		elif mouse.y < top_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,top_border)
				#pygame.mouse.set_pos((left_border, top_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,top_border)
				#pygame.mouse.set_pos((right_border, top_border))
		elif mouse.y > bottom_border:
			if mouse.x < left_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(left_border,bottom_border)
				#pygame.mouse.set_pos((left_border, bottom_border))
			if mouse.x > right_border:
				mouse_offset_vector = mouse - pygame.math.Vector2(right_border,bottom_border)
				#pygame.mouse.set_pos((right_border, bottom_border))

		if left_border < mouse.x < right_border:
			if mouse.y < top_border:
				mouse_offset_vector.y = mouse.y - top_border
				#pygame.mouse.set_pos((mouse.x, top_border))
			if mouse.y > bottom_border:
				mouse_offset_vector.y = mouse.y - bottom_border
				#pygame.mouse.set_pos((mouse.x, bottom_border))

		self.offset += mouse_offset_vector * self.mouse_speed

	def zoom_keyboard_control(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_q]:
			self.zoom_scale += 0.1
		if keys[pygame.K_e]:
			self.zoom_scale -= 0.1

	def custom_draw(self, player, tree_list):
		
		# self.center_target_camera(player)
		# self.box_target_camera(player)
		# self.keyboard_control()
		self.mouse_control()
		self.zoom_keyboard_control()

		# Взаимодействие с деревьями
		self.test_tree = None
		pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

		for i, tree in enumerate(tree_list):
			if tree.rect.collidepoint((player.rect.x, player.rect.y)):
				self.test_tree = tree.rect

			self.test_scaled_tree_rect = None
			mouse = pygame.mouse.get_pos()
			scaled_tree_rect = tree.rect.copy()
			self.test_scaled_tree_rect = scaled_tree_rect

			if scaled_tree_rect.collidepoint((mouse[0] + self.offset[0]), # * self.zoom_scale
									(mouse[1] + self.offset[1])):
				self.test_tree = tree.rect
				self.test_tree_selected_index = str(i) + ' ' + tree.name + ' Размер: ' + str(tree.size)
				pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

		self.internal_surf.fill('#71ddee')

		# ground 
		ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
		self.test_ground_offset = ground_offset
		self.internal_surf.blit(self.ground_surf, ground_offset)

		# active elements
		for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
			self.internal_surf.blit(sprite.image, offset_pos)

		if self.zoom_scale < 0:
			self.zoom_scale = 0.01

		scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
		scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

		self.display_surface.blit(scaled_surf, scaled_rect)


class CameraGame:
	def __init__(self, screen, base_path):
		self.running = False
		self.screen = screen
		self.base_path = base_path

		self.clock = pygame.time.Clock()

		# setup
		self.camera_group = CameraGroup(base_path=self.base_path)
		self.player = Player((640, 360), self.camera_group, base_path=self.base_path)

		self.tree_list = []
		for i in range(20):
			random_x = randint(1000, 2000)
			random_y = randint(1000, 2000)
			tree = Tree((random_x, random_y), self.camera_group, base_path=self.base_path)
			tree.name = tree.name + ' ' + str(i+1)
			self.tree_list.append(tree)

	def set_running(self, value):
		self.running = value

		if self.running:
			pygame.event.set_grab(True)
		else:
			pygame.event.set_grab(False)

	def run(self, events):
		if not self.running:
			return

		for event in events:

			if event.type == pygame.QUIT:
				self.set_running(False)

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.set_running(False)

			if event.type == pygame.MOUSEWHEEL:
				self.camera_group.zoom_scale += event.y * 0.03

		self.screen.fill('#71ddee')

		self.camera_group.update()
		self.camera_group.custom_draw(self.player, self.tree_list)

		# Панель управления
		# self.display_surface.blit(scaled_surf, scaled_rect)
		BLACK = (0, 0, 0)
		panel_surf = pygame.Surface((400, 800))
		pygame.draw.rect(panel_surf, BLACK,
						 pygame.Rect(0, 0, 400, 800))

		# Статистика
		stats = [
				('Статистика', ''),
				('player.rect', self.player.rect),
				('camera_group.offset', self.camera_group.offset),
				('camera_group.camera_rect', self.camera_group.camera_rect),
				('test_stat', self.camera_group.test_stat),
				('zoom_scale', self.camera_group.zoom_scale),
				('len(tree_list)', len(self.tree_list)),
				('test_ground_offset', self.camera_group.test_ground_offset),
				('test_tree', self.camera_group.test_tree),
				('pygame.mouse.get_pos()', pygame.mouse.get_pos()),
				('test_scaled_tree_rect', self.camera_group.test_scaled_tree_rect),
				('test_tree_selected_index', self.camera_group.test_tree_selected_index)
				]
		for i, line in enumerate(stats):
			font = pygame.font.Font(None, 24)
			surf_text = font.render(str(line[0]) + ': ' + str(line[1]), True, (255, 255, 255))
			panel_surf.blit(surf_text, (10, 300 + (i*30)))

		scaled_surf = pygame.transform.scale(self.camera_group.internal_surf, self.camera_group.internal_surface_size_vector * 0.1)
		panel_surf.blit(scaled_surf, (0, 0))

		self.screen.blit(panel_surf, (0, 0))

		#pygame.display.update()
		self.clock.tick(60)


def main():
	pygame.init()
	screen = pygame.display.set_mode((1280, 720))
	clock = pygame.time.Clock()
	pygame.event.set_grab(True)

	# setup
	camera_group = CameraGroup()
	player = Player((640, 360), camera_group)

	tree_list = []
	for i in range(20):
		random_x = randint(1000, 2000)
		random_y = randint(1000, 2000)
		tree_list.append(Tree((random_x, random_y), camera_group))

	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()

			if event.type == pygame.MOUSEWHEEL:
				camera_group.zoom_scale += event.y * 0.03

		screen.fill('#71ddee')

		camera_group.update()
		camera_group.custom_draw(player)

		pygame.display.update()
		clock.tick(60)


if __name__ == '__main__':
	main()
