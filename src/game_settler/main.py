import pygame
import sys
import os
from random import randint
from .tree import Tree, TreeSmall
from .gold import Gold
from .house import House
from .house_gold_mine import HouseGoldMine, HouseGoldMineSmall
from .player import Player
from .worker import Worker
from .camera_group import CameraGroup


class SettlerGame:
    def __init__(self, screen, clock, base_path):
        self.running = False
        self.screen = screen
        self.clock = clock
        self.base_path = base_path
        self.font = pygame.font.Font(None, 24)

        # Объявление объектов
        self.camera_group = CameraGroup(base_path=self.base_path)
        self.player = Player((1000, 1000), self.camera_group, base_path=self.base_path)
        self.worker = Worker((1000, 1150), self.camera_group, type='Worker', base_path=self.base_path)
        self.worker_gold_miner = Worker((1000, 1050), self.camera_group, type='GoldMiner', base_path=self.base_path)

        self.tree_list = []
        for i in range(20):
            random_x = randint(1000, 2000)
            random_y = randint(1000, 2000)
            tree = Tree((random_x, random_y), self.camera_group, base_path=self.base_path)
            tree.name = tree.name + ' ' + str(i + 1)
            self.tree_list.append(tree)

        self.gold = Gold((0, 0), self.camera_group, base_path=self.base_path)

        self.panel_tree_small = TreeSmall((10, 10), base_path=self.base_path)
        self.panel_tree_small.transform()
        self.panel_tree_small_new = TreeSmall((10, 10), base_path=self.base_path)
        self.panel_tree_small_new.transform()
        self.panel_tree_small_selected = None

        self.panel_house_gold_mine_small = HouseGoldMineSmall((10, 10), base_path=self.base_path)
        self.panel_house_gold_mine_small.transform()
        self.panel_house_gold_mine_small_new = HouseGoldMineSmall((10, 10), base_path=self.base_path)
        self.panel_house_gold_mine_small_new.transform()
        self.panel_house_gold_mine_small_selected = None

        self.stat_common_selected = True
        self.set_active_house = False

        self.house = House((640, 1000), self.camera_group, base_path=self.base_path)
        self.house_gold_mine_list = []
        self.house_gold_mine_list.append(HouseGoldMine((1500, 900), self.camera_group, base_path=self.base_path))
        self.house_gold_mine_list.append(HouseGoldMine((1800, 900), self.camera_group, base_path=self.base_path))

        self.camera_group.offset = (210, 785)

    def get_house_gold_mine(self):
        return self.house_gold_mine_list[0]

    def add_tree(self, tree_small):
        tree = Tree((tree_small.rect.x + self.camera_group.offset[0],
                     tree_small.rect.y + self.camera_group.offset[1]),
                    self.camera_group, base_path=self.base_path)
        self.tree_list.append(tree)

    def add_house_gold_mine(self, house_gold_mine_small):
        house_gold_mine = HouseGoldMine((house_gold_mine_small.rect.x + self.camera_group.offset[0],
                     house_gold_mine_small.rect.y + self.camera_group.offset[1]),
                    self.camera_group, base_path=self.base_path)
        self.house_gold_mine_list.append(house_gold_mine)

    def set_running(self, value):
        self.running = value

        if self.running:
            pygame.event.set_grab(True)
        else:
            pygame.event.set_grab(False)

    def select_objects(self, value):
        self.house.mouse_selected = value

        for house in self.house_gold_mine_list:
            house.mouse_selected = value
        self.worker.mouse_selected = value
        self.worker_gold_miner.mouse_selected = value

        if not value:
            self.camera_group.tree_selected_index = -1

    def get_selected_objects(self):
        if self.house.mouse_selected:
            return 'house'

        for house in self.house_gold_mine_list:
            if house.mouse_selected:
                return 'house_gold_mine'

        if self.worker.mouse_selected:
            return 'worker'

        if self.worker_gold_miner.mouse_selected:
            return 'worker_gold_miner'

        if self.camera_group.tree_selected_index >= 0:
            return 'tree'

        if self.stat_common_selected:
            return 'common stat'

        return None

    def get_selected_new_objects(self):
        if self.panel_tree_small_selected:
            return 'new tree'
        elif self.panel_house_gold_mine_small_selected:
            return 'new house_gold_mine'

        return None

    def select_house_after_common(self):
        """ Выбираем дом если включен флаг, затем флаг выключаем """
        if self.set_active_house:
            self.house.mouse_selected = True
            self.set_active_house = False

    def contol_panel(self, mouse):
        """  Панель управления """

        color_black = (0, 0, 0)
        w, display_height = pygame.display.get_surface().get_size()

        # Создание панели
        panel_surf = pygame.Surface((400, display_height))
        pygame.draw.rect(panel_surf, color_black, pygame.Rect(0, 0, 400, display_height))

        # Формирование текста на панели
        selected_object = self.get_selected_objects()
        stats = []
        p_stats_y = 300

        # Текст если выбран дом
        if selected_object == 'house':
            stats = [
                ('Дом', ''),
                ('Собрано деревьев в доме', self.house.done_tree_count),
                ('Золото', self.house.done_gold_count)
            ]

            # Уменьшенные картинки объектов
            self.panel_tree_small.rect.x = 100
            self.panel_tree_small.rect.y = p_stats_y + ((len(stats) - 1) * 30) + 30
            panel_surf.blit(self.panel_tree_small.image, self.panel_tree_small.rect)

            self.panel_house_gold_mine_small.rect.x = 200
            self.panel_house_gold_mine_small.rect.y = p_stats_y + ((len(stats) - 1) * 30) + 30
            panel_surf.blit(self.panel_house_gold_mine_small.image, self.panel_house_gold_mine_small.rect)

        # Текст если выбрана шахта
        elif selected_object == 'house_gold_mine':
            stats = [
                ('Золотая шахта', ''),
                ('Золото в шахте',
                 self.house_gold_mine_list[self.camera_group.house_gold_mine_selected_index].gold_count)
            ]

        # Текст если выбран рабочий
        elif selected_object == 'worker':
            stats = [
                ('Рабочий', ''),
                ('test_worker', self.camera_group.test_worker)
            ]

        # Текст если выбран золотодобытчик
        elif selected_object == 'worker_gold_miner':
            stats = [
                ('Шахтер золота', '')
            ]

        # Текст если выбрано дерево
        elif selected_object == 'tree':
            stats = [
                ('Дерево', ''),
                ('Деревьево номер', self.camera_group.tree_selected_index)
            ]

        # Текст если не выбран ни один объект - общая статистика
        elif selected_object == 'common stat':
            stats = [
                ('Статистика', ''),
                ('fps', self.clock.get_fps()),
                ('test_worker_gold_miner', self.camera_group.test_worker_gold_miner),
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

        # Отрисовка текста панели
        for i, line in enumerate(stats):
            surf_text = self.font.render(str(line[0]) + ': ' + str(line[1]), True, (255, 255, 255))
            panel_surf.blit(surf_text, (10, p_stats_y + (i * 30)))

        # Миникарта
        scaled_surf = pygame.transform.scale(self.camera_group.internal_surf,
                                             self.camera_group.internal_surface_size_vector * 0.1)
        panel_surf.blit(scaled_surf, (0, 0))

        # Создание новых объектов - удерживаем мышкой новый объект
        if self.panel_tree_small_selected:
            self.panel_tree_small_new.rect.x = mouse[0]
            self.panel_tree_small_new.rect.y = mouse[1]
            self.screen.blit(self.panel_tree_small_new.image, self.panel_tree_small_new.rect)

        elif self.panel_house_gold_mine_small_selected:
            self.panel_house_gold_mine_small_new.rect.x = mouse[0]
            self.panel_house_gold_mine_small_new.rect.y = mouse[1]
            self.screen.blit(self.panel_house_gold_mine_small_new.image, self.panel_house_gold_mine_small_new.rect)
        # else:
        #     # Оставляем объект
        #     self.add_tree(self.panel_tree_small_new)

        return panel_surf

    def run(self, events):
        if not self.running:
            return

        mouse = pygame.mouse.get_pos()

        for event in events:

            if event.type == pygame.QUIT:
                self.set_running(False)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.set_running(False)

            if event.type == pygame.MOUSEWHEEL:
                self.camera_group.zoom_scale += event.y * 0.03

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.panel_tree_small_selected:
                    self.panel_tree_small_selected = False
                    # Оставляем объект
                    self.add_tree(self.panel_tree_small_new)
                    self.set_active_house = True
                elif self.panel_house_gold_mine_small_selected:
                    self.panel_house_gold_mine_small_selected = False
                    # Оставляем объект
                    self.add_house_gold_mine(self.panel_house_gold_mine_small_new)
                    self.set_active_house = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.panel_tree_small.rect.collidepoint(mouse[0], mouse[1]):
                    self.panel_tree_small_selected = True
                elif self.panel_house_gold_mine_small.rect.collidepoint(mouse[0], mouse[1]):
                    self.panel_house_gold_mine_small_selected = True

            # Если нажали мышкой на экране и не выбрали ни одного объекта
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.get_selected_objects() and not self.get_selected_new_objects():
                    # == 'common stat'
                    self.select_objects(False)
                    self.stat_common_selected = True

            self.select_house_after_common()

        self.screen.fill('#71ddee')

        # Обновление объектов
        self.camera_group.update()
        self.camera_group.house_gold_mine_update(mouse, events, self.house_gold_mine_list)
        self.camera_group.gold_miner_update(mouse, events, self.worker_gold_miner, self.gold, self.house, self.worker,
                                            self.house_gold_mine_list)
        self.camera_group.worker_update(events, self.house, self.player, self.worker, self.tree_list)
        self.camera_group.custom_draw()

        # Контрольная панель
        panel_surf = self.contol_panel(mouse)
        self.screen.blit(panel_surf, (0, 0))
