from ThimeusConstants import COLORS, SWORD, FLAMETHROWER, AXE, STAFF, HOOK, GUN, DARK_COLOR
from ThimeusFunctions import change_color, create_particle_rect
from PlatonicSolid import PlatonicSolid
import pygame
import math


class Interface(pygame.sprite.Group):
    powers = [(COLORS["red"], SWORD, 6),
              (COLORS["orange"], FLAMETHROWER, 3),
              (COLORS["green"], AXE, 4),
              (COLORS["yellow"], STAFF, 3),
              (COLORS["blue"], HOOK, 3),
              (COLORS["purple"], GUN, 5)]

    def __init__(self, player, powers_amount, current_power, all_sprites):
        super().__init__()
        self.player = player
        self.color = self.player.color
        self.max_health = self.player.max_health
        self.health = self.player.health

        self.all_sprites = all_sprites
        self.decor = self.all_sprites[4]

        self.line_width = 10
        left, top = 50, 50

        self.health_bar = pygame.sprite.Sprite(self)
        self.health_bar.image = pygame.Surface((900, 75), pygame.SRCALPHA, 32)
        self.health_bar.rect = self.health_bar.image.get_rect().move(left, top)

        self.powers_amount = powers_amount
        self.current_powers = Interface.powers[:powers_amount]

        self.slot_size = 120
        self.spacing = 36

        self.font_size = 65
        self.inventory = pygame.sprite.Sprite(self)
        self.inventory.image = pygame.Surface((self.slot_size * 6 + self.spacing * 5,
                                               self.slot_size + self.font_size), pygame.SRCALPHA, 32)
        self.inventory.rect = self.inventory.image.get_rect().move(left, top + 75 + self.spacing)

        self.power_reload = pygame.sprite.Sprite(self)
        self.power_reload.image = pygame.Surface((self.slot_size - self.line_width, self.slot_size - self.line_width),
                                                 pygame.SRCALPHA, 32)
        self.power_reload.rect = self.power_reload.image.get_rect().move(self.inventory.rect.right + self.spacing,
                                                                         self.inventory.rect.top + self.line_width)
        self.power_cooldown = 500
        self.current_power_cooldown = 0

        self.pointer = pygame.sprite.Sprite(self)
        self.pointer.image = pygame.Surface((self.slot_size - self.line_width, self.slot_size // 10),
                                            pygame.SRCALPHA, 32)
        self.pointer.rect = self.pointer.image.get_rect().move(left + self.line_width,
                                                               self.inventory.rect.y - self.spacing // 2)
        pygame.draw.rect(self.pointer.image, self.color, (0, 0, *self.pointer.rect.size), 0, 10)

        self.solids = list()
        self.load_inventory()

        self.current_power = current_power
        self.set_power(current_power)

    def add_power(self):
        self.powers_amount += 1
        self.current_powers = Interface.powers[:self.powers_amount]
        self.load_inventory()

    def load_inventory(self):
        for solid in self.solids:
            solid.kill()
        self.solids = list()

        font = pygame.font.Font("data/fonts/SatyrSP.otf", self.font_size)

        self.inventory.image.fill((0, 0, 0, 0))
        for i, power in enumerate(self.current_powers):
            rect = (i * (self.slot_size + self.spacing) + self.line_width, self.line_width,
                    self.slot_size - self.line_width, self.slot_size - self.line_width)
            pygame.draw.rect(self.inventory.image, DARK_COLOR, rect, 0, 10)
            pygame.draw.rect(self.inventory.image, power[0], rect, self.line_width, 10)
            number = font.render(str(i + 1), True, power[0])
            self.inventory.image.blit(number, (rect[0] + (rect[2] - number.get_size()[0]) // 2,
                                               self.slot_size + self.line_width))
            self.solids.append(PlatonicSolid(self, self.inventory.rect.x + rect[0] + self.line_width,
                                             self.inventory.rect.y + rect[1] + self.line_width,
                                             rect[2] - self.line_width * 2, i, False))

    def update(self):
        self.health = self.player.health
        if self.health < 0:
            self.health = 0
        self.health_bar.image.fill((0, 0, 0, 0))
        rect = (self.line_width, self.line_width, 900 - self.line_width, 75 - self.line_width)
        part_rect = (self.line_width * 2, self.line_width,
                     (900 - self.line_width * 2) * self.health / self.max_health - self.line_width, 75 - self.line_width)
        pygame.draw.rect(self.health_bar.image, DARK_COLOR, rect, 0, 10)
        if self.health > 0:
            pygame.draw.rect(self.health_bar.image, self.color, part_rect, 0, 10)
        pygame.draw.rect(self.health_bar.image, self.color, rect, self.line_width, 10)

        self.power_reload.image.fill((0, 0, 0, 0))
        pygame.draw.arc(self.power_reload.image, self.color, (self.line_width, self.line_width,
                                                              self.power_reload.rect.w - self.line_width * 2,
                                                              self.power_reload.rect.h - self.line_width * 2),
                        math.pi, -math.pi + math.pi * 2 * (self.current_power_cooldown / self.power_cooldown), 25)

        if self.current_power_cooldown == 0:
            for power in range(self.powers_amount):
                if eval(f"pygame.key.get_pressed()[pygame.K_{power + 1}]"):
                    if self.current_power == power:
                        continue
                    self.set_power(power)
                    self.current_power_cooldown = self.power_cooldown
                    create_particle_rect(self.player.hit_box.rect.x, self.player.hit_box.rect.y,
                                         *self.player.hit_box.rect.size, 20, self.color, self.decor)
                    break
        else:
            self.current_power_cooldown -= 1

        needed_pointer_x = (self.inventory.rect.x + self.current_power *
                            (self.slot_size + self.spacing) + self.line_width)
        if self.pointer.rect.x < needed_pointer_x:
            self.pointer.rect.x += 40
            if self.pointer.rect.x > needed_pointer_x:
                self.pointer.rect.x = needed_pointer_x
        elif self.pointer.rect.x > needed_pointer_x:
            self.pointer.rect.x -= 40
            if self.pointer.rect.x < needed_pointer_x:
                self.pointer.rect.x = needed_pointer_x

        for solid in self.solids:
            solid.update()

    def set_power(self, power):
        self.current_power = power
        self.pointer.image = change_color(self.pointer.image, self.powers[power][0])
        self.color = self.powers[power][0]
        self.player.set_power(*self.powers[power])

