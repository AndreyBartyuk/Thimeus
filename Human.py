from ThimeusConstants import DARK_COLOR, LINE_WIDTH, MELEE_ATTACK, RANGED_ATTACK, RIGHT_ARM, LEFT_ARM
from Legs import Legs
from Arm import Arm
from Head import Head
import pygame


class Human(pygame.sprite.Group):
    def __init__(self, x, y, height, color, walls_group, ladders_group, projectiles_group, camera):
        super().__init__()
        self.x = x
        self.y = y
        self.h = height
        self.w = self.h // 3
        self.color = pygame.Color(color)

        self.hit_box = pygame.sprite.Sprite(self)
        self.hit_box.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.hit_box.rect = pygame.Rect(self.x, self.y, self.w, self.h)

        self.velocity = [0, 0]
        self.gravity = 0.5
        self.friction = 0.8
        self.max_x_speed = 8 + self.friction
        self.standing = False

        self.idle_count = 0
        self.idle_direction = 1
        self.idle_move = 0
        self.max_idle_count = 30

        self.body = pygame.sprite.Sprite(self)
        self.body.image = pygame.Surface((self.w, self.h // 2), pygame.SRCALPHA, 32)
        self.body.rect = self.body.image.get_rect().move(self.x, self.y + self.h // 3)
        points = [(0, 0), (self.w, 0), (self.w // 2, self.h // 4)]
        pygame.draw.polygon(self.body.image, DARK_COLOR, points)
        pygame.draw.polygon(self.body.image, self.color, points, LINE_WIDTH)

        self.legs = Legs(self, self.w, self.h // 2, self.color)
        self.legs.rect = self.legs.rect.move(self.x, self.y + self.w * 1.7)

        self.walls = walls_group
        self.ladders = ladders_group
        self.projectiles = projectiles_group
        self.camera = camera

        self.right_arm = Arm(self, self.h // 3, RIGHT_ARM, self.color, self.projectiles, self.walls)
        self.right_arm.set_axis(self.x + self.w * 1.1, self.y + self.w)
        self.left_arm = Arm(self, self.h // 3, LEFT_ARM, self.color, self.projectiles, self.walls)
        self.left_arm.set_axis(self.x - self.w * 0.1, self.y + self.w)

        self.head = Head(self, self.w, 6, self.color)
        self.head.rect = self.head.rect.move(self.x, self.y)

        self.weapon = None
        self.weapon_delay = 0
        self.current_delay = 0

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

        if abs(self.velocity[0]) > self.max_x_speed:
            self.velocity[0] = self.max_x_speed * (1 if self.velocity[0] > 0 else -1)

        # attack
        mouse_buttons = pygame.mouse.get_pressed()
        if self.current_delay != 0:
            self.current_delay -= 1
        if mouse_buttons[0] and self.weapon is not None and self.current_delay == 0:
            self.current_delay = self.weapon_delay
            if self.weapon.attack == MELEE_ATTACK:
                self.left_arm.melee_attack()
                self.right_arm.melee_attack()
            elif self.weapon.attack == RANGED_ATTACK:
                self.left_arm.ranged_attack()
                self.right_arm.ranged_attack()

    def update(self):
        for sprite in self:
            sprite.update()

        self.get_events()

        if not self.standing:
            self.velocity[1] += self.gravity
        self.move(0, self.velocity[1])
        on_ground = False
        collisions = pygame.sprite.spritecollide(self.hit_box, self.walls, False)
        for wall in collisions:
            if self.velocity[1] > 0:
                self.move(0, wall.rect.top - self.hit_box.rect.bottom)
                self.standing = True
                on_ground = True
            elif self.velocity[1] < 0:
                self.move(0, wall.rect.bottom - self.hit_box.rect.top)
            self.velocity[1] = 0
        if not on_ground:
            self.standing = False

        self.move(self.velocity[0], 0)
        collisions = pygame.sprite.spritecollide(self.hit_box, self.walls, False)
        for wall in collisions:
            if self.velocity[0] > 0:  # moving right
                self.move(wall.rect.left - self.hit_box.rect.right, 0)
            elif self.velocity[0] < 0:  # moving left
                self.move(wall.rect.right - self.hit_box.rect.left, 0)

        if self.velocity[0] > 0:
            self.velocity[0] -= self.friction
            self.velocity[0] = self.velocity[0] if self.velocity[0] >= 0 else 0
        elif self.velocity[0] < 0:
            self.velocity[0] += self.friction
            self.velocity[0] = self.velocity[0] if self.velocity[0] <= 0 else 0

        self.head.speed = self.velocity[0] // 2 + 0.1 * self.idle_direction
        self.legs.speed = self.velocity[0]

        # idle animation
        self.idle_count = (self.idle_count + 1) % self.max_idle_count
        if self.idle_count == 0:

            self.body.rect = self.body.rect.move(0, self.idle_direction)
            self.head.rect = self.head.rect.move(0, -self.idle_direction)
            self.left_arm.rect = self.left_arm.rect.move(0, -self.idle_direction)
            self.right_arm.rect = self.right_arm.rect.move(0, -self.idle_direction)

            self.idle_move += self.idle_direction
            if self.idle_move == 2 or self.idle_move == -2:
                self.idle_direction = -self.idle_direction

    def move(self, x_move, y_move):
        self.camera.move(-x_move, -y_move)
        # for sprite in self:
        #    sprite.rect = sprite.rect.move(x_move, y_move)

    def set_head_sides(self, amount):
        self.head.sides = amount

    def get_weapon(self, weapon):
        self.weapon = weapon
        self.left_arm.get_weapon(weapon)
        self.right_arm.get_weapon(weapon)
        self.current_delay = 0
        self.weapon_delay = weapon.duration + weapon.delay
