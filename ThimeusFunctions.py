from Particle import Particle
import random
import pygame
import os
import sys
import math
import numba


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

def generate_wave(width, height, amplitude, frequency, phase, color):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)
    for x in range(width):
        y = int(height / 2 + amplitude * math.sin(frequency * x + phase))
        pygame.draw.line(surface, color, (x, y), (x, height), 2)
    return surface

def change_color(image: pygame.Surface, color):
    image = image.copy()
    for x in range(image.get_width()):
        for y in range(image.get_height()):
            if image.get_at((x, y))[3] != 0:
                image.set_at((x, y), color)
    return image

