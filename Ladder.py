from ThimeusConstants import LINE_WIDTH, TILE_SIZE
import pygame


# Class of the Ladder for the locations
class Ladder(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color, bottom, top):
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect().move(x, y)
        line_width = round(LINE_WIDTH * 1.8)
        pygame.draw.line(self.image, color, (TILE_SIZE / 5 * 1.5, 0),
                         (TILE_SIZE / 5 * 1.5, TILE_SIZE), line_width)
        pygame.draw.line(self.image, color, (TILE_SIZE / 5 * 3.5, 0),
                         (TILE_SIZE / 5 * 3.5, TILE_SIZE), line_width)
        amount = 4
        for i in range(amount):
            if (i == amount - 1 and not bottom) or (i == 0 and not top):
                continue
            pygame.draw.line(self.image, color, (line_width, TILE_SIZE / (amount - 1) * i),
                             (TILE_SIZE - line_width, TILE_SIZE / (amount - 1) * i), line_width)
        self.mask = pygame.mask.from_surface(self.image)