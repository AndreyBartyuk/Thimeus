from Particle import Particle
import random
import pygame
import os
import sys


def load_image(name, color_key=None):
    fullname = os.path.join("data", name)
    if not os.path.isfile(fullname):
        print(f"Image file {name} does not exist")
        sys.exit()
    image_ = pygame.image.load(fullname)
    if color_key is not None:
        image_ = image_.convert()
        if color_key == -1:
            color_key = image_.get_at((0, 0))
        image_.set_colorkey(color_key)
    else:
        image_ = image_.convert_alpha()
    return image_


def create_particle_rect(x, y, w, h, amount, parent, group):
    for i in range(amount):
        pos = (x + random.randrange(w), y + random.randrange(h))
        Particle(group, *pos, random.randint(-5, 5) / 30, random.randint(10, 30) / 30, parent)


