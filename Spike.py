from ThimeusConstants import DARK_COLOR, TILE_SIZE, LINE_WIDTH
import pygame


class Spike(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color):
        super().__init__(group)
        self.color = color
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect().move(x, y)
        pygame.draw.polygon(self.image, DARK_COLOR, ((LINE_WIDTH, TILE_SIZE),
                                                     (TILE_SIZE - LINE_WIDTH, TILE_SIZE),
                                                     (TILE_SIZE // 2, LINE_WIDTH * 2)))
        pygame.draw.polygon(self.image, self.color, ((LINE_WIDTH, TILE_SIZE),
                                                     (TILE_SIZE - LINE_WIDTH, TILE_SIZE),
                                                     (TILE_SIZE // 2, LINE_WIDTH * 2)),
                            round(LINE_WIDTH * 1.5))
