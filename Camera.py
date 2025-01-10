import pygame
from Human import Human


class Camera:
    def __init__(self):
        self.target = None
        for group in all_sprites:
            if isinstance(group, Human):
                self.target = group
        target_x = self.target.hit_box.rect.x + self.target.hit_box.rect.w // 2
        target_y = self.target.hit_box.rect.y + self.target.hit_box.rect.h // 2
        self.move(SCREEN_WIDTH // 2 - target_x, SCREEN_HEIGHT // 2 - target_y)
        for sprite in self.target:
            sprite.rect = sprite.rect.move(SCREEN_WIDTH // 2 - target_x,
                                           SCREEN_HEIGHT // 2 - target_y)

    def move(self, x_move, y_move):
        for group in all_sprites:
            if group == self.target:
                continue
            for sprite in group:
                sprite.rect = sprite.rect.move(x_move, y_move)