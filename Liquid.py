from ThimeusFunctions import generate_wave
from ThimeusConstants import COLORS, TILE_SIZE
from math import pi
import pygame


class Liquid(pygame.sprite.Sprite):
    images = dict()

    @staticmethod
    def load_images():
        frame_amount = 20 # 30
        for color in COLORS:
            frames = list()
            for frame in [generate_wave(TILE_SIZE, TILE_SIZE, TILE_SIZE / 20, 0.127,
                                        i * 2 * pi / frame_amount, COLORS[color])
                          for i in range(frame_amount)]:
                frames += [frame]
            Liquid.images[COLORS[color]] = frames

    def __init__(self, group, x, y, up_free, color):
        super().__init__(group)
        self.up_free = up_free
        self.frames = None
        if up_free:
            self.frames = Liquid.images[color]
            self.frame_amount = len(self.frames)
            self.image = self.frames[0]
        else:
            self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
            self.image.fill(color)
        self.current_frame = 0
        self.rect = self.image.get_rect().move(x, y)

    def update(self):
        if self.up_free:
            self.current_frame = (self.current_frame + 1) % self.frame_amount
            self.image = self.frames[self.current_frame]




