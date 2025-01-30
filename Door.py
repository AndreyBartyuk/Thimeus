from ThimeusConstants import TILE_SIZE, DARK_COLOR, LINE_WIDTH
from ThimeusFunctions import change_color, load_image
import pygame


# Class of the Door for the locations
class Door(pygame.sprite.Sprite):
    def __init__(self, group, x, y, color, is_exit):
        super().__init__(group)
        self.is_exit = is_exit
        self.color = color
        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE * 3), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect().move(x, y)
        points = ((TILE_SIZE // 2, TILE_SIZE // 1.8), (TILE_SIZE - LINE_WIDTH, TILE_SIZE),
                  (TILE_SIZE - LINE_WIDTH, TILE_SIZE * 3), (LINE_WIDTH, TILE_SIZE * 3),
                  (LINE_WIDTH, TILE_SIZE))
        pygame.draw.polygon(self.image, DARK_COLOR, points)
        pygame.draw.polygon(self.image, self.color, points, round(LINE_WIDTH * 1.5))
        filename = "arrowUp.png" if self.is_exit else "arrowDown.png"
        icon = pygame.transform.scale(change_color(load_image(filename), self.color),
                                      (TILE_SIZE, TILE_SIZE))
        self.image.blit(icon, (0, TILE_SIZE))
        self.exited = False
        self.interactable = True

    # Player interaction with the Door
    def interact(self, *args):
        self.exited = True
