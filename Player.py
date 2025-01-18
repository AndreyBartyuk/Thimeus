from ThimeusConstants import MELEE_ATTACK, RANGED_ATTACK
from ThimeusFunctions import load_image, change_color
from Human import Human
import pygame


class Player(Human):
    def __init__(self, x, y, height, color, camera, all_sprites):
        super().__init__(x, y, height, color, True, all_sprites)
        self.camera = camera

        self.health_bar = pygame.sprite.Sprite(self)
        self.health_bar.image = pygame.Surface((self.w * 2, self.w / 3), pygame.SRCALPHA, 32)
        self.health_bar.rect = self.health_bar.image.get_rect().move(x - self.w / 2, y - self.w / 2)

        self.interact_button = pygame.sprite.Sprite(self)
        self.key_r_image = pygame.transform.scale(change_color(load_image("keyR.png"), self.color),
                                                  (self.w, self.w))
        self.interact_button.image = self.key_r_image.copy()
        self.interact_button.rect = self.interact_button.image.get_rect().move(x, y - self.w * 1.6)

    def get_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity[0] += 1
        if keys[pygame.K_a]:
            self.velocity[0] -= 1

        if keys[pygame.K_LSHIFT]:
            pass # rivok

        if keys[pygame.K_w]:
            if any(self.hit_box.rect.colliderect(ladder.rect) for ladder in self.ladders):
                self.velocity[1] = -6

        if keys[pygame.K_SPACE] and self.standing:
            self.velocity[1] -= 15

        # arm target
        self.right_arm.set_target(*pygame.mouse.get_pos())
        self.left_arm.set_target(*pygame.mouse.get_pos())

        # attack
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and self.weapon is not None and self.current_delay == 0:
            self.current_delay = self.weapon_delay
            if self.weapon.attack == MELEE_ATTACK:
                self.left_arm.melee_attack()
                self.right_arm.melee_attack()
            elif self.weapon.attack == RANGED_ATTACK:
                self.left_arm.ranged_attack()
                self.right_arm.ranged_attack()

        self.health_bar.image.fill((0, 0, 0, 0))
        part_rect = pygame.Rect(0, 0, self.health_bar.rect.w * (self.health / self.max_health),
                                self.health_bar.rect.h)
        pygame.draw.rect(self.health_bar.image, self.color, part_rect, 0, 3)
        pygame.draw.rect(self.health_bar.image, self.color, (0, 0, *self.health_bar.rect.size), 4, 3)

        interactions = pygame.sprite.spritecollide(self.hit_box, self.interactable, False)
        if interactions:
            self.interact_button.image = self.key_r_image.copy()
            if keys[pygame.K_r]:
                for sprite in interactions:
                    sprite.interact()
        else:
            self.interact_button.image.fill((0, 0, 0, 0))

    def set_params(self, color, weapon, head_sides):
        self.color = color
        self.weapon = weapon
        self.set_head_sides(head_sides)
        self.key_r_image = change_color(self.key_r_image, self.color)

    def move(self, x_move, y_move):
        self.camera.move(-x_move, -y_move)