from ThimeusConstants import DARK_COLOR, LINE_WIDTH, MELEE_ATTACK, RANGED_ATTACK
from Legs import Legs
from Arm import Arm
from Head import Head
import pygame


class Human(pygame.sprite.Group):
    def __init__(self, x, y, h, color):
        super().__init__()
        self.x = x
        self.y = y
        self.h = h
        self.w = self.h // 3
        self.color = pygame.Color(color)

        self.v = [0, 0]
        self.hit_box = pygame.sprite.Sprite(self)
        self.hit_box.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.hit_box.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.gravity = 0.5
        self.friction = 0.8
        self.max_x_speed = 8 + self.friction
        self.standing = False

        self.count = 0
        self.dir = 1
        self.body_move = 0
        self.max_count = 30

        self.body = pygame.sprite.Sprite(self)
        self.body.image = pygame.Surface((self.w, self.h // 2), pygame.SRCALPHA, 32)
        self.body.rect = self.body.image.get_rect().move(self.x, self.y + self.h // 3)
        points = [(0, 0), (self.w, 0), (self.w // 2, self.h // 4)]
        pygame.draw.polygon(self.body.image, DARK_COLOR, points)
        pygame.draw.polygon(self.body.image, self.color, points, LINE_WIDTH)

        self.legs = Legs(self, self.w, self.h // 2, self.color)
        self.legs.rect = self.legs.rect.move(self.x, self.y + self.w * 1.7)

        self.r_arm = Arm(self, self.h // 3, self.color)
        self.r_arm.type = 1
        self.r_arm.set_axis(self.x + self.w * 1.1, self.y + self.w)
        self.l_arm = Arm(self, self.h // 3, self.color)
        self.l_arm.set_axis(self.x - self.w * 0.1, self.y + self.w)

        self.head = Head(self, self.w, 6, self.color)
        self.head.rect = self.head.rect.move(self.x, self.y)

        self.weapon = None
        self.weapon_delay = 0
        self.cur_delay = 0

    def get_events(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.v[0] += 1
        if keys[pygame.K_a]:
            self.v[0] -= 1

        if keys[pygame.K_LSHIFT]:
            pass # rivok

        if keys[pygame.K_w]:
            if any(self.hit_box.rect.colliderect(ladder.rect) for ladder in ladders):
                self.v[1] = -6

        if keys[pygame.K_SPACE] and self.standing:
            self.v[1] -= 15

        if abs(self.v[0]) > self.max_x_speed:
            self.v[0] = self.max_x_speed * (1 if self.v[0] > 0 else -1)

        # attack
        mouse_buttons = pygame.mouse.get_pressed()
        if self.cur_delay != 0:
            self.cur_delay -= 1
        if mouse_buttons[0] and self.weapon is not None and self.cur_delay == 0:
            self.cur_delay = self.weapon_delay
            if self.weapon.attack == MELEE_ATTACK:
                self.l_arm.melee_attack()
                self.r_arm.melee_attack()
            elif self.weapon.attack == RANGED_ATTACK:
                self.l_arm.ranged_attack()
                self.r_arm.ranged_attack()

    def update(self):
        for sprite in self:
            sprite.update()

        self.get_events()

        if not self.standing:
            self.v[1] += self.gravity
        self.move(0, self.v[1])
        on_ground = False
        collisions = pygame.sprite.spritecollide(self.hit_box, walls, False)
        for wall in collisions:
            if self.v[1] > 0:
                self.move(0, wall.rect.top - self.hit_box.rect.bottom)
                self.standing = True
                on_ground = True
            elif self.v[1] < 0:
                self.move(0, wall.rect.bottom - self.hit_box.rect.top)
            self.v[1] = 0

        if not on_ground:
            self.standing = False

        self.move(self.v[0], 0)
        collisions = pygame.sprite.spritecollide(self.hit_box, walls, False)
        for wall in collisions:
            if self.v[0] > 0:  # moving right
                self.move(wall.rect.left - self.hit_box.rect.right, 0)
            elif self.v[0] < 0:  # moving left
                self.move(wall.rect.right - self.hit_box.rect.left, 0)

        if self.v[0] > 0:
            self.v[0] -= self.friction
            self.v[0] = self.v[0] if self.v[0] >= 0 else 0
        elif self.v[0] < 0:
            self.v[0] += self.friction
            self.v[0] = self.v[0] if self.v[0] <= 0 else 0

        self.head.speed = self.v[0] // 2 + 0.1 * self.dir
        self.legs.speed = self.v[0]

        # idle animation
        self.count = (self.count + 1) % self.max_count
        if self.count == 0:

            self.body.rect = self.body.rect.move(0, self.dir)
            self.head.rect = self.head.rect.move(0, -self.dir)
            self.l_arm.rect = self.l_arm.rect.move(0, -self.dir)
            self.r_arm.rect = self.r_arm.rect.move(0, -self.dir)

            self.body_move += self.dir
            if self.body_move == 2 or self.body_move == -2:
                self.dir = -self.dir

    def move(self, x_move, y_move):
        camera.move(-x_move, -y_move)
        # for sprite in self:
        #    sprite.rect = sprite.rect.move(x_move, y_move)

    def get_weapon(self, weapon):
        self.weapon = weapon
        self.l_arm.get_weapon(weapon)
        self.r_arm.get_weapon(weapon)
        self.cur_delay = 0
        self.weapon_delay = weapon.duration + weapon.delay
