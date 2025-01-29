from math import sin ,cos, radians, pi
from ThimeusConstants import LINE_WIDTH, DARK_COLOR
import pygame


class Legs(pygame.sprite.Sprite):
    def __init__(self, group, w, h, color):
        super().__init__(group)
        self.w = w
        self.h = h
        self.image = pygame.Surface((w, h), pygame.SRCALPHA, 32)
        self.rect = pygame.Rect(0, 0, w, h)
        self.color = pygame.Color(color)
        self.angle = 0
        self.leg_width = self.w // 4
        self.speed = 0

    def update(self):
        self.angle = (self.angle + self.speed) % 360
        if self.speed == 0 and self.angle != 0:
            self.angle -= 7
            if self.angle < 0:
                self.angle = 0

        self.image.fill((0, 0, 0, 0))

        self.draw_leg(self.angle)
        self.draw_leg(self.angle + 180)

    def draw_leg(self, angle):
        up_points = [(self.w // 2 + self.w // 6 * cos(radians(angle) + 2 * pi) - self.leg_width // 2,
                      self.h // 8 + self.h // 12 * sin(radians(angle) + 2 * pi))]
        up_points += [(up_points[0][0] + self.w // 4, up_points[0][1])]

        down_points = [(self.w // 2 + self.w // 2.8 * cos(radians(angle) + 2 * pi) - self.leg_width // 2,
                        self.h // 8 * 7 + self.h // 8 * sin(radians(angle) + 2 * pi))]
        down_points = [(down_points[0][0] + self.w // 4, down_points[0][1])] + down_points

        pygame.draw.polygon(self.image, DARK_COLOR, up_points + down_points)
        pygame.draw.polygon(self.image, self.color, up_points + down_points, LINE_WIDTH)
