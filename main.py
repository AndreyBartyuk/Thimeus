from screeninfo import get_monitors
import pygame

pygame.init()
monitor = get_monitors()[0]
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = monitor.width, monitor.height
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.toggle_fullscreen()

from Game import Game

game = Game(screen)
game.main_loop()
