from ThimeusConstants import TILE_SIZE, DARK_COLOR, LINE_WIDTH
import pygame


# Class of wall Tile for locations
class Tile(pygame.sprite.Sprite):
    def __init__(self, group, x, y, neighbours, color):
        super().__init__(group)
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA, 32)
        self.image.fill(DARK_COLOR)
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)
        for index, side in enumerate(neighbours):
            if side:
                if index == 0:
                    pygame.draw.line(self.image, color, (0, 0), (TILE_SIZE, 0), LINE_WIDTH * 3)
                elif index == 1:
                    pygame.draw.line(self.image, color, (TILE_SIZE, 0), (TILE_SIZE, TILE_SIZE), LINE_WIDTH * 3)
                elif index == 2:
                    pygame.draw.line(self.image, color, (TILE_SIZE, TILE_SIZE), (0, TILE_SIZE), LINE_WIDTH * 3)
                elif index == 3:
                    pygame.draw.line(self.image, color, (0, TILE_SIZE), (0, 0), LINE_WIDTH * 3)
