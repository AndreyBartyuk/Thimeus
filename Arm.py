from math import atan2, pi, degrees, sin, cos, radians
from ThimeusConstants import (DARK_COLOR, LINE_WIDTH, SWORD, FLAMETHROWER, AXE, STAFF, HOOK, GUN,
                              RIGHT_ARM, LEFT_ARM, MELEE_ATTACK)
from Projectile import Projectile
import pygame
import random


class Arm(pygame.sprite.Sprite):
    def __init__(self, group, length, kind, color, is_player, all_sprites):
        super().__init__(group)
        self.image = pygame.Surface((500, 500), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.angle = 90
        self.l = length
        self.w = length // 8
        self.color = pygame.Color(color)
        self.type = kind
        self.speed = 14 # 10

        self.is_active = False
        self.is_targeting = True

        self.weapon = None
        self.delay = 0
        self.current_delay = 0

        self.walls_group = all_sprites[0]
        self.projectiles_group = all_sprites[5]
        self.all_sprites = all_sprites

        self.target_pos = (0, 0)
        self.is_player = is_player
        self.targets = list()
        self.mask = pygame.mask.from_surface(self.image)

    def set_axis(self, x, y):
        self.rect.x = x - self.rect.w // 2
        self.rect.y = y - self.rect.h // 2

    def set_target(self, x, y):
        self.target_pos = (x, y)

    def update(self):
        self.image.fill((0, 0, 0, 0))
        axis_x = self.rect.x + self.rect.w // 2
        axis_y = self.rect.y + self.rect.h // 2

        cur_x, cur_y = self.target_pos

        self.is_active = True
        if self.current_delay == 0:
            self.targets = list()
            angle = degrees(1.5 * pi - atan2((axis_x - cur_x), (axis_y - cur_y)))
            if self.type == LEFT_ARM:
                if not 100 < angle % 360 < 260:
                    angle = 100
                    self.is_active = False
            elif self.type == RIGHT_ARM:
                if not 280 < angle < 440:
                    angle = 440
                    self.is_active = False
            self.move(angle)
        else:
            if self.weapon.attack == MELEE_ATTACK:
                if not self.targets:
                    name = "Enemy" if self.is_player else "Player"
                    self.targets = [[group, False] for group in self.all_sprites
                                    if group.__class__.__name__ == name]
                for index, (target, is_hit) in enumerate(self.targets):
                    if not is_hit:
                        if pygame.sprite.collide_mask(self, target.hit_box):
                            self.targets[index][1] = True
                            target.get_damage(self.weapon.damage)

            self.current_delay -= 1
            if self.type == RIGHT_ARM:
                self.move(self.angle + self.speed)
            else:
                self.move(self.angle - self.speed)

        if self.weapon is not None and self.is_active:
            weapon_points = self.get_rotated_weapon_points()
            for point_set in weapon_points:
                pygame.draw.polygon(self.image, DARK_COLOR, point_set, 0)
                pygame.draw.polygon(self.image, self.color, point_set, LINE_WIDTH - 1)
            self.mask = pygame.mask.from_surface(self.image)

        points = self.get_rotated_arm_points(self.l, self.w, self.angle)
        pygame.draw.polygon(self.image, DARK_COLOR, points)
        pygame.draw.polygon(self.image, self.color, points, LINE_WIDTH)

    def move(self, angle):
        if self.angle > angle:
            self.angle = self.angle - self.speed
            if self.angle < angle:
                self.angle = angle
        elif self.angle < angle:
            self.angle = self.angle + self.speed
            if self.angle > angle:
                self.angle = angle

    def get_rotated_arm_points(self, width, height, angle):
        x, y = self.rect.w // 2, self.rect.w // 2
        points = [(0, -height), (0, height), (width, height), (width, -height)]
        rotated_points = list()
        for point in points:
            rotated_x = point[0] * cos(radians(angle)) - point[1] * sin(radians(angle))
            rotated_y = point[0] * sin(radians(angle)) + point[1] * cos(radians(angle))
            rotated_points.append((rotated_x + x, rotated_y + y))
        return rotated_points

    def get_rotated_weapon_points(self):
        x, y = (self.rect.w // 2, self.rect.w // 2)
        x_move, y_move = self.weapon.blit_point
        if self.type == LEFT_ARM:
            x_move = -x_move
        rotated_polygons = list()
        for point_set in self.weapon.polygons:
            polygon = list()
            if self.type == LEFT_ARM:
                point_set = [(-x, y) for x, y in point_set]
            for point in point_set:
                rotated_x = ((point[0] + x_move) * cos(radians(self.angle)) - (point[1] + y_move) *
                             sin(radians(self.angle)))
                rotated_y = ((point[0] + x_move) * sin(radians(self.angle)) + (point[1] + y_move) *
                             cos(radians(self.angle)))
                if self.type == LEFT_ARM:
                    polygon.append((-rotated_x + x, -rotated_y + y))
                else:
                    polygon.append((rotated_x + x, rotated_y + y))
            rotated_polygons.append(polygon)
        return rotated_polygons

    def get_rotated_projectile_pos(self):
        x, y = (self.rect.w // 2, self.rect.w // 2)
        point = self.weapon.projectile_pos
        if self.type == RIGHT_ARM:
            rotated_x = point[0] * cos(radians(self.angle)) - point[1] * sin(radians(self.angle))
            rotated_y = point[0] * sin(radians(self.angle)) + point[1] * cos(radians(self.angle))
        else:
            rotated_x = point[0] * cos(radians(self.angle)) + point[1] * sin(radians(self.angle))
            rotated_y = point[0] * sin(radians(self.angle)) - point[1] * cos(radians(self.angle))
        return rotated_x + self.rect.x + x, rotated_y + self.rect.y + y

    def melee_attack(self):
        if not self.is_active or self.current_delay != 0:
            return None
        self.current_delay = self.delay
        pos = self.get_rotated_projectile_pos()
        damage = self.weapon.damage
        if self.weapon.type == SWORD:
            Projectile(self.projectiles_group, pos[0], pos[1], 0, self.angle, SWORD, damage,
                       self.is_player, self.all_sprites, flip=not bool(self.type))
        elif self.weapon.type == AXE:
            Projectile(self.projectiles_group, pos[0], pos[1], 3, self.angle, AXE, damage,
                       self.is_player, self.all_sprites, flip=not bool(self.type))
        elif self.weapon.type == HOOK:
            Projectile(self.projectiles_group, pos[0], pos[1], 15, self.angle, HOOK, damage,
                       self.is_player, self.all_sprites, flip=not bool(self.type))

    def ranged_attack(self):
        if not self.is_active:
            return None
        pos = self.get_rotated_projectile_pos()
        damage = self.weapon.damage
        if self.weapon.type == FLAMETHROWER:
            Projectile(self.projectiles_group, pos[0], pos[1], 10, self.angle + random.randrange(-10, 11, 5),
                       FLAMETHROWER, damage, self.is_player, self.all_sprites)
        elif self.weapon.type == STAFF:
            for i in range(-2, 3):
                Projectile(self.projectiles_group, pos[0], pos[1], 10, self.angle + i * 10,
                           STAFF, damage, self.is_player, self.all_sprites)
        elif self.weapon.type == GUN:
            Projectile(self.projectiles_group, pos[0], pos[1], 21, self.angle + random.randrange(-2, 3),
                       GUN, damage, self.is_player, self.all_sprites)

    def get_weapon(self, weapon):
        self.weapon = weapon
        self.delay = weapon.duration
