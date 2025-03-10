from ThimeusConstants import DARK_COLOR, LINE_WIDTH, RIGHT_ARM, LEFT_ARM
from ThimeusFunctions import create_particle_rect
from Legs import Legs
from Arm import Arm
from Head import Head
import pygame


# Class of the Human for inheriting by Player and Enemy classes
class Human(pygame.sprite.Group):
    def __init__(self, x, y, height, color, is_player, all_sprites):
        super().__init__()
        self.x = x
        self.y = y
        self.h = height
        self.w = self.h // 3
        self.center = (self.w // 2, self.h // 2)
        self.color = pygame.Color(color)

        self.hit_box = pygame.sprite.Sprite(self)
        self.hit_box.image = pygame.Surface((self.w, self.h), pygame.SRCALPHA, 32)
        self.hit_box.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        mask_surface = pygame.Surface((self.w, self.h))
        mask_surface.fill("black")
        self.hit_box.mask = pygame.mask.from_surface(mask_surface)
        # pygame.draw.rect(self.hit_box.image, "white", (0, 0, *self.hit_box.rect.size), 3, 3)

        self.velocity = [0, 0]
        self.gravity = 0.7
        self.friction = 1.12
        self.acceleration = 1.4
        self.jump = 19
        self.climbing_speed = 8.4
        self.max_x_speed = 11.2 + self.friction
        self.dash_speed = 40
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

        self.walls = all_sprites[0]
        self.ladders = all_sprites[1]
        self.interactable = all_sprites[2]
        self.obstacles = all_sprites[3]
        self.decor = all_sprites[4]
        self.projectiles = all_sprites[5]
        self.all_sprites = all_sprites

        self.right_arm = Arm(self, self.h // 3, RIGHT_ARM, self.color, is_player, all_sprites)
        self.right_arm.set_axis(self.x + self.w * 1.1, self.y + self.w)
        self.left_arm = Arm(self, self.h // 3, LEFT_ARM, self.color, is_player, all_sprites)
        self.left_arm.set_axis(self.x - self.w * 0.1, self.y + self.w)

        self.head = Head(self, self.w, 6, self.color)
        self.head.rect = self.head.rect.move(self.x, self.y)

        self.weapon = None
        self.weapon_delay = 0
        self.current_delay = 0

        self.obstacle_damage = 0.5
        self.max_health = 100
        self.health = 100
        self.dead = False
        self.dashing = False
        self.hit_by_obstacles = True

    # Get events for Human behaviour
    def get_events(self):
        pass

    # Update the state of the Human
    def update(self):
        for sprite in self:
            sprite.update()

        if self.current_delay != 0:
            self.current_delay -= 1

        self.get_events()

        if abs(self.velocity[0]) > self.max_x_speed and not self.dashing:
            self.velocity[0] = self.max_x_speed * (1 if self.velocity[0] > 0 else -1)

        if not self.standing and not self.dashing:
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

        # Obstacles check
        if self.hit_by_obstacles:
            if pygame.sprite.spritecollide(self.hit_box, self.obstacles, False):
                self.get_damage(self.obstacle_damage)

        # Idle animation
        self.idle_count = (self.idle_count + 1) % self.max_idle_count
        if self.idle_count == 0:

            self.body.rect = self.body.rect.move(0, self.idle_direction)
            self.head.rect = self.head.rect.move(0, -self.idle_direction)
            self.left_arm.rect = self.left_arm.rect.move(0, -self.idle_direction)
            self.right_arm.rect = self.right_arm.rect.move(0, -self.idle_direction)

            self.idle_move += self.idle_direction
            if self.idle_move == 2 or self.idle_move == -2:
                self.idle_direction = -self.idle_direction

    # Move the Human
    def move(self, x_move, y_move):
        for sprite in self:
           sprite.rect = sprite.rect.move(x_move, y_move)

    # Set amount of sides for the Head of the Human
    def set_head_sides(self, amount):
        self.head.sides = amount

    # Set color for the Human
    def set_color(self, color):
        self.color = color
        self.head.color = color
        self.legs.color = color
        self.right_arm.color = color
        self.left_arm.color = color
        self.body.image.fill((0, 0, 0, 0))
        points = [(0, 0), (self.w, 0), (self.w // 2, self.h // 4)]
        pygame.draw.polygon(self.body.image, DARK_COLOR, points)
        pygame.draw.polygon(self.body.image, self.color, points, LINE_WIDTH)

    # Set the Weapon for the Human
    def set_weapon(self, weapon):
        self.weapon = weapon
        self.left_arm.get_weapon(weapon)
        self.right_arm.get_weapon(weapon)
        self.current_delay = self.right_arm.current_delay = self.left_arm.current_delay = 0
        self.weapon_delay = weapon.duration + weapon.delay

    # Reduce amount of health points
    def get_damage(self, damage):
        if not self.dead and not self.dashing:
            create_particle_rect(self.hit_box.rect.x, self.hit_box.rect.y,
                                 *self.hit_box.rect.size, round(damage / 2), self.color, self.decor)
            self.health -= damage
            if self.health <= 0:
                self.kill()

    # Death of the Human
    def kill(self):
        if not self.dead:
            create_particle_rect(self.hit_box.rect.x, self.hit_box.rect.y,
                                 *self.hit_box.rect.size, 100, self.color, self.decor)
            self.all_sprites.remove(self)
            for sprite in self:
                sprite.kill()
            self.dead = True
