import pygame
import sys
import os
from random import randint
from examples.Pygame_Cameras_main.tree import Tree
from examples.Pygame_Cameras_main.house import House
from examples.Pygame_Cameras_main.player import Player
from examples.Pygame_Cameras_main.worker import Worker
from examples.Pygame_Cameras_main.camera_group import CameraGroup


class CameraGame:
    def __init__(self, screen, base_path):
        self.running = False
        self.screen = screen
        self.base_path = base_path
        self.font = pygame.font.Font(None, 24)

        # setup
        self.camera_group = CameraGroup(base_path=self.base_path)
        self.player = Player((1000, 1000), self.camera_group, base_path=self.base_path)
        self.worker = Worker((1000, 1150), self.camera_group, base_path=self.base_path)

        self.tree_list = []
        for i in range(20):
            random_x = randint(1000, 2000)
            random_y = randint(1000, 2000)
            tree = Tree((random_x, random_y), self.camera_group, base_path=self.base_path)
            tree.name = tree.name + ' ' + str(i + 1)
            self.tree_list.append(tree)

        self.house = House((640, 1000), self.camera_group, base_path=self.base_path)

        self.camera_group.offset = (210, 785)

    def set_running(self, value):
        self.running = value

        if self.running:
            pygame.event.set_grab(True)
        else:
            pygame.event.set_grab(False)

    def select_objects(self, value):
        self.house.mouse_selected = value
        self.worker.mouse_selected = value

        if not value:
            self.camera_group.tree_selected_index = -1

    def get_selected_objects(self):
        if self.house.mouse_selected:
            return 'house'

        if self.worker.mouse_selected:
            return 'worker'

        if self.camera_group.tree_selected_index >= 0:
            return 'tree'

        return None

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

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.get_selected_objects():
                    self.select_objects(False)

        self.screen.fill('#71ddee')

        self.camera_group.update()
        self.camera_group.custom_draw(events, self.player, self.worker, self.tree_list, self.house)

        # Панель управления
        BLACK = (0, 0, 0)
        panel_surf = pygame.Surface((400, 800))
        pygame.draw.rect(panel_surf, BLACK, pygame.Rect(0, 0, 400, 800))

        p_selected_object = self.get_selected_objects()
        stats = []

        if not p_selected_object:
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
                ('test_tree_selected_index', self.camera_group.test_tree_selected_index),
                ('test_worker', self.camera_group.test_worker),
                ('test_house', self.camera_group.test_house),
                ('Собрано деревьев', self.camera_group.test_tree_done_count),
                ('Собрано деревьев в доме', self.house.done_tree_count)
            ]

        elif p_selected_object == 'house':
            # Статистика
            stats = [
                ('Дом', ''),
                ('Собрано деревьев в доме', self.house.done_tree_count)
            ]

        elif p_selected_object == 'worker':
            # Статистика
            stats = [
                ('Рабочий', ''),
                ('test_worker', self.camera_group.test_worker)
            ]

        elif p_selected_object == 'tree':
            # Статистика
            stats = [
                ('Дерево', ''),
                ('test_tree', self.camera_group.test_tree),
				('Деревьево номер', self.camera_group.tree_selected_index),
                ('Собрано деревьев', self.camera_group.test_tree_done_count)
            ]

        # Панель управления
        # Текст панели
        for i, line in enumerate(stats):
            surf_text = self.font.render(str(line[0]) + ': ' + str(line[1]), True, (255, 255, 255))
            panel_surf.blit(surf_text, (10, 300 + (i * 30)))

        # Миникарта
        scaled_surf = pygame.transform.scale(self.camera_group.internal_surf,
                                             self.camera_group.internal_surface_size_vector * 0.1)
        panel_surf.blit(scaled_surf, (0, 0))

        self.screen.blit(panel_surf, (0, 0))


# def main():
# 	pygame.init()
# 	screen = pygame.display.set_mode((1280, 720))
# 	clock = pygame.time.Clock()
# 	pygame.event.set_grab(True)
#
# 	# setup
# 	camera_group = CameraGroup()
# 	player = Player((640, 360), camera_group)
# 	worker = Worker((640, 450), camera_group)
#
# 	tree_list = []
# 	for i in range(20):
# 		random_x = randint(1000, 2000)
# 		random_y = randint(1000, 2000)
# 		tree_list.append(Tree((random_x, random_y), camera_group))
#
# 	while True:
# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				pygame.quit()
# 				sys.exit()
# 			if event.type == pygame.KEYDOWN:
# 				if event.key == pygame.K_ESCAPE:
# 					pygame.quit()
# 					sys.exit()
#
# 			if event.type == pygame.MOUSEWHEEL:
# 				camera_group.zoom_scale += event.y * 0.03
#
# 		screen.fill('#71ddee')
#
# 		camera_group.update()
# 		camera_group.custom_draw(player, worker)
#
# 		pygame.display.update()
# 		clock.tick(60)
#
#
# if __name__ == '__main__':
# 	main()
