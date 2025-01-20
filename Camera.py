from Player import Player
import pygame


class Camera:
    def __init__(self, all_sprites):
        self.screen_width, self.screen_height = pygame.display.get_window_size()
        self.all_sprites = all_sprites
        self.target = None

    def set_target(self):
        for group in self.all_sprites:
            if isinstance(group, Player):
                self.target = group
        target_x = self.target.hit_box.rect.x + self.target.hit_box.rect.w // 2
        target_y = self.target.hit_box.rect.y + self.target.hit_box.rect.h // 2
        self.move(self.screen_width // 2 - target_x, self.screen_height // 2 - target_y)
        for sprite in self.target:
            sprite.rect = sprite.rect.move(self.screen_width // 2 - target_x,
                                           self.screen_height // 2 - target_y)

    def move(self, x_move, y_move):
        for group in self.all_sprites:
            if group == self.target or group.__class__.__name__ == "Interface":
                continue
            for sprite in group:
                sprite.rect = sprite.rect.move(x_move, y_move)