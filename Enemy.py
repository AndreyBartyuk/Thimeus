from ThimeusConstants import MELEE_ATTACK, RANGED_ATTACK, DARK_COLOR
from Human import Human
from Weapon import Weapon
import pygame
import random


class Enemy(Human):
    def __init__(self, x, y, height, color, weapon, head_sides, all_sprites):
        super().__init__(x, y, height, color, False, all_sprites)
        self.get_weapon(Weapon(self.h, weapon))
        self.set_head_sides(head_sides)

        self.view_field = pygame.sprite.Sprite(self)
        self.view_field.image = pygame.Surface((self.h * 10, self.h * 1.5), pygame.SRCALPHA, 32)
        pos = (x + self.w // 2 - self.view_field.image.get_size()[0] // 2,
               y + self.h // 2 - self.view_field.image.get_size()[1] // 2)
        self.view_field.rect = self.view_field.image.get_rect().move(pos)

        self.target = None
        self.needed_distance = (300 + random.randrange(6) * 25 if self.weapon.attack == MELEE_ATTACK
                                else 400 + random.randrange(5) * 100)

        self.health_bar = pygame.sprite.Sprite(self)
        self.health_bar.image = pygame.Surface((self.w * 2, self.w / 3), pygame.SRCALPHA, 32)
        self.health_bar.rect = self.health_bar.image.get_rect().move(x - self.w / 2, y - self.w / 2)

    def set_target(self, target):
        self.target = target

    def get_events(self):
        if self.view_field.rect.colliderect(self.target.hit_box.rect) and not self.target.dead:
            pos = (self.target.hit_box.rect.x + self.target.hit_box.rect.w // 2,
                   self.target.hit_box.rect.y + self.target.hit_box.rect.h // 2)
            self.right_arm.set_target(*pos)
            self.left_arm.set_target(*pos)

            distance = ((self.hit_box.rect.x + self.center[0]) -
                        (self.target.hit_box.rect.x + self.target.center[0]))
            if distance > 0:
                if distance < self.needed_distance:
                    self.velocity[0] += 1
                elif distance > self.needed_distance:
                    self.velocity[0] -= 1
            elif distance < 0:
                if abs(distance) < self.needed_distance:
                    self.velocity[0] -= 1
                elif  abs(distance) > self.needed_distance:
                    self.velocity[0] += 1
            elif distance == 0:
                self.velocity[0] = -self.velocity[0]

            if self.current_delay == 0:
                self.current_delay = self.weapon_delay
                if self.weapon.attack == MELEE_ATTACK:
                    self.left_arm.melee_attack()
                    self.right_arm.melee_attack()
                elif self.weapon.attack == RANGED_ATTACK:
                    self.left_arm.ranged_attack()
                    self.right_arm.ranged_attack()
        else:
            pos = (self.hit_box.rect.x + self.center[0], self.hit_box.rect.y + self.center[1])
            self.right_arm.set_target(*pos)
            self.left_arm.set_target(*pos)

        self.health_bar.image.fill((0, 0, 0, 0))
        part_rect = pygame.Rect(0, 0, self.health_bar.rect.w * (self.health / self.max_health),
                                self.health_bar.rect.h)
        pygame.draw.rect(self.health_bar.image, self.color, part_rect, 0, 3)
        pygame.draw.rect(self.health_bar.image, self.color, (0, 0, *self.health_bar.rect.size), 4, 3)
