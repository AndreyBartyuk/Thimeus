from math import sin, cos, pi, radians
from ThimeusConstants import DARK_COLOR, LINE_WIDTH
import pygame


class Head(pygame.sprite.Sprite):
    def __init__(self, group, size, sides, color):
        super().__init__(group)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(0, 0, size, size)
        self.color = pygame.Color(color)
        self.sides = sides
        self.angle = 0
        self.size = size
        self.radius = size // 2.2
        self.speed = 0

    def update(self):
        self.angle += self.speed
        self.image.fill((0, 0, 0, 0))
        points = [(self.size // 2 + self.radius * cos(radians(self.angle) + 2 * pi * i / self.sides),
                   self.size // 2 + self.radius * sin(radians(self.angle) + 2 * pi * i / self.sides))
                  for i in range(self.sides)]
        pygame.draw.polygon(self.image, DARK_COLOR, points)
        pygame.draw.polygon(self.image, self.color, points, LINE_WIDTH)