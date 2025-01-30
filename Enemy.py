from ThimeusConstants import MELEE_ATTACK, RANGED_ATTACK
from Human import Human
from Weapon import Weapon
import pygame


# Class of Enemy for the locations
class Enemy(Human):
    def __init__(self, x, y, height, color, weapon, head_sides, level, all_sprites):
        super().__init__(x, y, height, color, False, all_sprites)
        self.set_weapon(Weapon(self.h, weapon))
        self.set_head_sides(head_sides)

        self.view_field = pygame.sprite.Sprite(self)
        self.view_field.image = pygame.Surface((self.h * 10, self.h * 1.5), pygame.SRCALPHA, 32)
        self.view_field.rect = self.view_field.image.get_rect()
        self.view_field.rect.center = self.hit_box.rect.center
        # pygame.draw.rect(self.view_field.image, "white", (0, 0, *self.view_field.rect.size), 3, 3)

        self.target = None
        self.needed_distance = 300 if self.weapon.attack == MELEE_ATTACK else 500

        self.level = level
        self.weapon_delay = max(round(self.weapon_delay * 2 - self.level * 0.1 * self.weapon_delay), 1)
        self.weapon.damage = self.weapon.damage * 0.5 + (self.level * 0.1 * self.weapon.damage)
        self.max_x_speed = self.max_x_speed * 0.8 + self.level * 0.1 * self.max_x_speed
        self.max_health = self.max_health + self.level * 0.1 * self.max_health
        self.health = self.max_health
        self.hit_by_obstacles = False

        self.health_bar = pygame.sprite.Sprite(self)
        self.health_bar.image = pygame.Surface((self.w * 2, self.w / 3), pygame.SRCALPHA, 32)
        self.health_bar.rect = self.health_bar.image.get_rect().move(x - self.w / 2, y - self.w / 2)

        self.touch_point = pygame.sprite.Sprite(self)
        self.touch_point.image = pygame.Surface((self.hit_box.rect.w // 3, self.hit_box.rect.w // 3),
                                                pygame.SRCALPHA, 32)
        self.touch_point.rect = self.touch_point.image.get_rect()
        self.touch_point.rect.centerx = self.hit_box.rect.centerx
        self.touch_point.rect.bottom = self.hit_box.rect.bottom + 5
        # pygame.draw.rect(self.touch_point.image, "white", (0, 0, *self.touch_point.rect.size), 3, 3)

    # Set target for the Enemy
    def set_target(self, target):
        self.target = target

    # Get the events for Enemy behaviour
    def get_events(self):
        distance = ((self.hit_box.rect.x + self.center[0]) -
                    (self.target.hit_box.rect.x + self.target.center[0]))

        if self.view_field.rect.colliderect(self.target.hit_box.rect) and not self.target.dead:
            pos = (self.target.hit_box.rect.x + self.target.hit_box.rect.w // 2,
                   self.target.hit_box.rect.y + self.target.hit_box.rect.h // 2)
            self.right_arm.set_target(*pos)
            self.left_arm.set_target(*pos)

            if distance > 0:
                if distance < self.needed_distance:
                    self.velocity[0] += self.acceleration
                elif distance > self.needed_distance:
                    self.velocity[0] -= self.acceleration
            elif distance < 0:
                if abs(distance) < self.needed_distance:
                    self.velocity[0] -= self.acceleration
                elif abs(distance) > self.needed_distance:
                    self.velocity[0] += self.acceleration
            elif distance == 0:
                self.velocity[0] *= -1

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

        new_rect = self.touch_point.rect.copy().move(self.velocity[0], 0)
        if not new_rect.collideobjects([sprite.rect for sprite in self.walls]):
            self.velocity[0] = 0

        self.health_bar.image.fill((0, 0, 0, 0))
        part_rect = pygame.Rect(0, 0, self.health_bar.rect.w * (self.health / self.max_health),
                                self.health_bar.rect.h)
        pygame.draw.rect(self.health_bar.image, self.color, part_rect, 0, 3)
        pygame.draw.rect(self.health_bar.image, self.color, (0, 0, *self.health_bar.rect.size), 4, 3)

        # text = pygame.font.Font("data/fonts/SatyrSP.otf", self.h // 5).render(str(self.level + 1), True, self.color)
        # pygame.display.get_surface().blit(text, (self.hit_box.rect.centerx, self.hit_box.rect.top - 150))
