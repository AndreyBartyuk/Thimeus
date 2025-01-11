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

