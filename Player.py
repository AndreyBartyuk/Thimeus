from ThimeusConstants import MELEE_ATTACK, RANGED_ATTACK
from ThimeusFunctions import load_image, change_color, create_particle_trace
from Human import Human
from Weapon import Weapon
import pygame


# Class of the Player for the game loop
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

        self.dash_duration = 10
        self.current_dash_cooldown = 0

    # Get events for the Player behaviour
    def get_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.velocity[0] += self.acceleration
        if keys[pygame.K_a]:
            self.velocity[0] -= self.acceleration

        if keys[pygame.K_LSHIFT]:
            if self.current_dash_cooldown == 0 and self.velocity[0] != 0:
                direction = 1 if self.velocity[0] >= 0 else -1
                self.velocity = [self.dash_speed * direction, 0]
                self.current_dash_cooldown = self.dash_duration
                self.dashing = True
        if self.dashing:
            direction = 1 if self.velocity[0] >= 0 else -1
            create_particle_trace(self.hit_box.rect.x, self.hit_box.rect.y,
                                  *self.hit_box.rect.size, 5,
                                  -direction, self.color, self.decor)

        if self.current_dash_cooldown != 0:
            self.current_dash_cooldown -= 1
            if self.current_dash_cooldown == 0 and self.dashing:
                self.current_dash_cooldown = self.dash_duration * 3
                self.dashing = False

        if keys[pygame.K_w]:
            if any(self.hit_box.rect.colliderect(ladder.rect) for ladder in self.ladders):
                self.velocity[1] = -self.climbing_speed

        if keys[pygame.K_SPACE] and self.standing:
            self.velocity[1] -= self.jump

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
            if any([sprite.interactable for sprite in interactions]):
                self.interact_button.image = self.key_r_image.copy()
                if keys[pygame.K_r]:
                    for sprite in interactions:
                        if sprite.interactable:
                            sprite.interact(self.all_sprites)
        else:
            self.interact_button.image.fill((0, 0, 0, 0))

    # Set current power for the Player
    def set_power(self, color, weapon, head_sides):
        self.set_color(color)
        self.set_weapon(Weapon(self.h, weapon))
        self.set_head_sides(head_sides)
        self.key_r_image = change_color(self.key_r_image, self.color)

    # Move the objects with Camera to imitate Player motion
    def move(self, x_move, y_move):
        self.camera.move(-x_move, -y_move)
