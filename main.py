from screeninfo import get_monitors
import pygame

pygame.init()
monitor = get_monitors()[0]
screen_size = screen_width, screen_height = monitor.width, monitor.height
screen = pygame.display.set_mode(screen_size)
pygame.display.toggle_fullscreen()

from Game import Game

game = Game(screen)
game.main_loop()
