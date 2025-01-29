import pygame
import random


class Particle(pygame.sprite.Sprite):
    images = [pygame.Surface((i * 3 + 7, i * 3 + 7), pygame.SRCALPHA, 32) for i in range(3)]

    def __init__(self, group, x, y, x_acceleration, y_acceleration, color):
        super().__init__(group)
        self.image = random.choice(Particle.images).copy()
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect().move(x, y)
        self.x_acceleration = x_acceleration
        self.y_acceleration = y_acceleration
        self.velocity = [0, 0]

    def update(self):
        self.velocity[0] += self.x_acceleration
        self.velocity[1] += self.y_acceleration
        self.rect = self.rect.move(*self.velocity)
        if not self.rect.colliderect(pygame.Rect(0, 0, *pygame.display.get_window_size())):
            self.kill()
            del self

