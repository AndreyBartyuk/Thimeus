from ThimeusFunctions import load_image
from ThimeusConstants import COLORS
from Particle import Particle
from random import randrange
import pygame


class PlatonicSolid(pygame.sprite.Sprite):
    colors = [COLORS["red"], COLORS["orange"], COLORS["green"],
              COLORS["yellow"], COLORS["blue"], COLORS["purple"]]

    def __init__(self, group, x, y, size, num, interactable):
        super().__init__(group)
        sprite_sheet_ = load_image(f"{num}_spritesheet.png")
        self.num = num
        self.frame_amount = 25 if num != 0 else 50
        self.frames = list()
        image_w = image_h = 500
        mult = 4

        if num == 0:
            for frame in [pygame.transform.scale(sprite_sheet_.subsurface(i * image_w, j * image_h, image_w, image_h),
                                                 (size, size)) for j in range(5) for i in range(10)]:
                self.frames += [frame] * mult
        else:
            for frame in [pygame.transform.scale(sprite_sheet_.subsurface(i * image_w, 0, image_w, image_h),
                                                 (size, size)) for i in range(self.frame_amount)]:
                self.frames += [frame] * mult

        self.frame_amount *= mult
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(x, y)

        self.interactable = interactable

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.image = self.frames[self.current_frame]

    def interact(self, *args):
        all_sprites = args[0]

        decor = all_sprites[4]
        interface = all_sprites[-1]

        interface.add_power()
        interface.set_power(int(self.num))

        for i in range(200):
            Particle(decor, self.rect.x + randrange(self.rect.w), self.rect.y + randrange(self.rect.h),
                     randrange(-21, 22, 2) / 10, randrange(-21, 22, 2) / 10, PlatonicSolid.colors[int(self.num)])
        self.kill()
