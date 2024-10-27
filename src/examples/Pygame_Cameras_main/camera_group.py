import pygame
import sys
import os
from random import randint


class CameraGroup(pygame.sprite.Group):
    def __init__(self, base_path=''):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.tree_selected_index = -1
        self.test_stat = None
        self.test_ground_offset = None
        self.test_tree = None
        self.test_scaled_tree_rect = None
        self.test_tree_selected_index = None
        self.test_worker = None
        self.test_house = None
        self.test_tree_done_count = 0

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
            # pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
            # pygame.mouse.set_pos((right_border, mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
            # pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
            # pygame.mouse.set_pos((right_border, top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
            # pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
            # pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
            # pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
            # pygame.mouse.set_pos((mouse.x, bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            self.zoom_scale += 0.1
        if keys[pygame.K_e]:
            self.zoom_scale -= 0.1

    def get_min_tree(self, worker, tree_list):
        # Ближайшее дерево по y
        p_min_tree = None
        p_min_y = -1
        p_min_tree_y = -1

        for i, tree in enumerate(tree_list):
            if tree.done == 1:
                continue

            if p_min_y == -1:
                p_min_y = tree.rect.center[1]
                p_min_tree_y = i
            if tree.rect.center[1] < p_min_y:
                p_min_y = tree.rect.center[1]
                p_min_tree_y = i

        # Ближайшее дерево по x
        p_min_x = -1
        p_min_tree_x = -1

        for i, tree in enumerate(tree_list):
            if tree.done == 1:
                continue

            if p_min_x == -1:
                p_min_x = tree.rect.center[0]
                p_min_tree_x = i
            if tree.rect.center[0] < p_min_x:
                p_min_x = tree.rect.center[0]
                p_min_tree_x = i

        p_tree_y = None
        p_tree_x = None
        p_distance_tree_y = None
        p_distance_tree_x = None

        if p_min_tree_y >= 0:
            p_tree_y = tree_list[p_min_tree_y]

            p_distance_tree_y = (abs(worker.rect.center[0] - p_tree_y.rect.center[0])
                                 + abs(worker.rect.center[1] - p_tree_y.rect.center[1]))
        if p_min_tree_x >= 0:
            p_tree_x = tree_list[p_min_tree_x]
            p_distance_tree_x = (abs(worker.rect.center[0] - p_tree_x.rect.center[0])
                                 + abs(worker.rect.center[1] - p_tree_x.rect.center[1]))

        if p_distance_tree_y:
            if not p_distance_tree_x:
                return p_tree_y

        if p_distance_tree_x:
            if not p_distance_tree_y:
                return p_tree_x

        if p_distance_tree_y and p_distance_tree_x:
            if p_distance_tree_x <= p_distance_tree_y:
                p_min_tree = p_tree_x
            else:
                p_min_tree = p_tree_y

        return p_min_tree

    def custom_draw(self, events, player, worker, tree_list, house):

        # self.center_target_camera(player)
        # self.box_target_camera(player)
        # self.keyboard_control()
        self.mouse_control()
        self.zoom_keyboard_control()

        # Взаимодействие с деревьями
        self.test_tree = None
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if worker.tree_selected:
            worker.tree_selected.rect.center = worker.rect.center

        # Дом
        self.test_house = house.rect.center

        p_min_tree = self.get_min_tree(worker, tree_list)

        if p_min_tree:
            self.test_worker = 'worker ' + str(worker.rect.center) + ' tree ' + str(p_min_tree.rect.center)
        else:
            self.test_worker = 'worker ' + str(worker.rect.center) + ' tree ' + 'None'

        # Взаимодействие с ближайшим деревом
        if not worker.tree_selected:
            if p_min_tree:
                if p_min_tree.rect.collidepoint((worker.rect.center[0], worker.rect.center[1])):
                    p_min_tree.transform()
                    p_min_tree.done = 1
                    self.test_tree_done_count += 1
                    worker.tree_selected = p_min_tree

                if worker.rect.center[1] <= p_min_tree.rect.center[1]:
                    worker.move('down')
                else:
                    worker.move('up')

                if worker.rect.center[0] >= p_min_tree.rect.center[0]:
                    worker.move('left')
                else:
                    worker.move('right')
            else:
                worker.move('stop')

        if worker.tree_selected:
            if house.rect.collidepoint((worker.rect.center[0], worker.rect.center[1])):
                house.done_tree_count += 1
                worker.tree_selected = None

            if worker.rect.center[1] <= house.rect.center[1]:
                worker.move('down')
            else:
                worker.move('up')

            if worker.rect.center[0] >= house.rect.center[0]:
                worker.move('left')
            else:
                worker.move('right')

        mouse = pygame.mouse.get_pos()

        for i, tree in enumerate(tree_list):
            # Рабочий зашел в дерево
            if tree.rect.collidepoint((player.rect.x, player.rect.y)):
                self.test_tree = tree.rect

            self.test_scaled_tree_rect = None

            scaled_tree_rect = tree.rect.copy()
            self.test_scaled_tree_rect = scaled_tree_rect

            # Дерево
            if scaled_tree_rect.collidepoint((mouse[0] + self.offset[0]),  # * self.zoom_scale
                                             (mouse[1] + self.offset[1])):
                self.test_tree = tree.rect
                self.test_tree_selected_index = str(i) + ' ' + tree.name + ' Размер: ' + str(tree.size)
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.tree_selected_index = i

        # Дом
        if house.rect.collidepoint((mouse[0] + self.offset[0]),  # * self.zoom_scale
                                   (mouse[1] + self.offset[1])):
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if not house.mouse_selected:
                for event in events:
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        house.mouse_selected = True

        # Рабочий
        if worker.rect.collidepoint((mouse[0] + self.offset[0]),  # * self.zoom_scale
                                    (mouse[1] + self.offset[1])):
            if not worker.mouse_selected:
                for event in events:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        worker.mouse_selected = True

        self.internal_surf.fill('#71ddee')

        # ground
        ground_offset = self.ground_rect.topleft - self.offset + self.internal_offset
        self.test_ground_offset = ground_offset
        self.internal_surf.blit(self.ground_surf, ground_offset)

        # active elements
        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset + self.internal_offset
            self.internal_surf.blit(sprite.image, offset_pos)

        if self.zoom_scale < 0:
            self.zoom_scale = 0.01

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        self.display_surface.blit(scaled_surf, scaled_rect)
