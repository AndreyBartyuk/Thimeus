from math import sin, cos, radians
from ThimeusConstants import (SWORD, FLAMETHROWER, AXE, STAFF, HOOK, GUN,
                              SWORD_PROJECTILE_IMAGES, FLAMETHROWER_PROJECTILE_IMAGES,
                              AXE_PROJECTILE_IMAGES, STAFF_PROJECTILE_IMAGES,
                              HOOK_PROJECTILE_IMAGES, GUN_PROJECTILE_IMAGES, COLORS)
import pygame
import random


class Projectile(pygame.sprite.Sprite):
    def __init__(self, group, x, y, speed, angle, kind, damage, is_player, all_sprites, flip=False):
        super().__init__(group)
        self.kind = kind
        self.angle = angle
        self.speed_x = speed * cos(radians(self.angle))
        self.speed_y = speed * sin(radians(self.angle))
        self.current_frame = 0
        self.frames = list()
        self.frame_amount = 0

        self.walls = all_sprites[0]
        self.all_sprites = all_sprites

        self.is_player = is_player
        self.screen_rect = pygame.Rect(0, 0, *pygame.display.get_window_size())

        self.damage = damage
        if self.is_player:
            self.targets = [[group, False] for group in self.all_sprites
                            if group.__class__.__name__ == "Enemy"]
        else:
            self.targets = [[group, False] for group in self.all_sprites
                            if group.__class__.__name__ == "Player"]

        if self.kind == SWORD:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in SWORD_PROJECTILE_IMAGES]:
                self.frames += [frame] * 8
            self.frame_amount = 40
            self.lifetime = 40
            self.destroyed_by_walls = False
            self.color = COLORS["red"]

        elif self.kind == FLAMETHROWER:
            size = FLAMETHROWER_PROJECTILE_IMAGES[0].get_size()[0] + random.randrange(0, 20, 5)
            self.frames = [pygame.transform.rotate(pygame.transform.scale(image, (size, size)),
                                                   -self.angle)
                           for image in FLAMETHROWER_PROJECTILE_IMAGES]
            self.frame_amount = 60
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["orange"]

        elif self.kind == AXE:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in AXE_PROJECTILE_IMAGES]:
                self.frames += [frame] * 6
            self.frame_amount = 66
            self.lifetime = 66
            self.destroyed_by_walls = False
            self.color = COLORS["green"]

        elif self.kind == STAFF:
            size = STAFF_PROJECTILE_IMAGES[0].get_size()[0] + random.randrange(0, 20, 5)
            for frame in [pygame.transform.rotate(pygame.transform.scale(image, (size, size)),
                                                  -self.angle)
                          for image in STAFF_PROJECTILE_IMAGES]:
                self.frames += [frame] * 5
            self.frame_amount = 25
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["yellow"]

        elif self.kind == HOOK:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in HOOK_PROJECTILE_IMAGES]:
                self.frames += [frame] * 4
            self.frame_amount = 68
            self.lifetime = 68
            self.destroyed_by_walls = False
            self.color = COLORS["blue"]

        elif self.kind == GUN:
            for frame in [pygame.transform.rotate(image, -self.angle)
                          for image in GUN_PROJECTILE_IMAGES]:
                self.frames += [frame] * 5
            self.frame_amount = 50
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["purple"]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x - self.rect.w / 2, y - self.rect.h / 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.image = self.frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.rect.move(self.speed_x, self.speed_y)

        if self.lifetime != -1:
            self.lifetime -= 1
        for index, (target, is_hit) in enumerate(self.targets):
            if not is_hit:
                if pygame.sprite.collide_mask(self, target.hit_box):
                    self.targets[index][1] = True
                    target.get_damage(self.damage)

        if ((pygame.sprite.spritecollide(self, self.walls, dokill=False,
                                         collided=pygame.sprite.collide_mask) and
             self.destroyed_by_walls) or not self.rect.colliderect(self.screen_rect)
                or self.lifetime == 0):
            self.kill()
            del self

