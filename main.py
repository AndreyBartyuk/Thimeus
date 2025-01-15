from screeninfo import get_monitors
import pygame


pygame.init()
monitor = get_monitors()[0]
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.toggle_fullscreen()


from PlatonicSolid import PlatonicSolid
from LoadLevelFunction import load_level
from ThimeusConstants import DARK_COLOR, FPS
from Camera import Camera


walls = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
ladders = pygame.sprite.Group()
decor = pygame.sprite.Group()

all_sprites = [walls, ladders, projectiles, decor]
camera = Camera(all_sprites)
load_level("level_1.txt", all_sprites, camera)

PlatonicSolid(decor, 300, 200, 100, 4)
PlatonicSolid(decor, 450, 200, 100, 6)
PlatonicSolid(decor, 600, 200, 100, 8)
PlatonicSolid(decor, 750, 200, 100, 20)
PlatonicSolid(decor, 900, 200, 100, 12)

camera.set_target()
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                running = False
    screen.fill(DARK_COLOR)
    for group in all_sprites:
        group.update()
        group.draw(screen)
    print(clock.tick(FPS))
    pygame.display.flip()
pygame.quit()