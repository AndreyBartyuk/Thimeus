import pygame
from screeninfo import get_monitors
from Groups import walls, projectiles, ladders, decor


pygame.init()
monitor = get_monitors()[0]
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height
screen = pygame.display.set_mode(SCREEN_SIZE)


from PlatonicSolid import PlatonicSolid
from LoadLevelFunction import load_level
from ThimeusConstants import DARK_COLOR
from Camera import Camera


pygame.display.toggle_fullscreen()
clock = pygame.time.Clock()
FPS = 100
pygame.display.flip()
running = True
all_sprites = [walls, projectiles, ladders, decor]
load_level("level_1.txt")

PlatonicSolid(300, 200, 100, 4)
PlatonicSolid(450, 200, 100, 6)
PlatonicSolid(600, 200, 100, 8)
PlatonicSolid(750, 200, 100, 20)
PlatonicSolid(900, 200, 100, 12)
camera = Camera()
while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
    screen.fill(DARK_COLOR)
    for group in all_sprites:
        group.update()
        group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()