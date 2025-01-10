from ThimeusFunctions import load_image
from screeninfo import get_monitors
import pygame


TILE_SIZE = 100
CHARACTER_HEIGHT = TILE_SIZE * 2
LINE_WIDTH = 5
DARK_COLOR = "#151515"
COLORS = {"red": "#DE324C", "orange": "#F4895F", "yellow": "#F8E16F",
          "green": "#95CF92", "blue": "#369ACC", "purple": "#9656A2"}

SWORD = b"sword"
FLAMETHROWER = b"flamethrower"
AXE = b"axe"
STAFF = b"staff"
HOOK = b"hook"
GUN = b"gun"

MELEE_ATTACK = b"melee"
RANGED_ATTACK = b"ranged"

FLAME_PROJECTILE = b"flame"
sprite_sheet = load_image("flame_one_color.png")
w = sprite_sheet.get_size()[0] // 61
h = sprite_sheet.get_size()[1]
FLAME_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)), (200, 200))
                for i in range(60)]

SWORD_SLASH = b"sword_slash"
sprite_sheet = load_image("sword_slash_one_color.png")
w = sprite_sheet.get_size()[0] // 5
h = sprite_sheet.get_size()[1]
SWORD_SLASH_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)), (300, 500))
                      for  i in range(5)]

AXE_HIT = b"axe_hit"
sprite_sheet = load_image("axe_hit_one_color.png")
w = sprite_sheet.get_size()[0] // 12
h = sprite_sheet.get_size()[1]
AXE_HIT_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h), (200, 200))
                  for i in range(12)]

THUNDER = b"thunder"
sprite_sheet = load_image("thunder_one_color.png")
w = sprite_sheet.get_size()[0] // 5
h = sprite_sheet.get_size()[1]
THUNDER_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h), (150, 150))
                  for i in range(5)]

HOOK_WAVE = b"hook_wave"
sprite_sheet = load_image("hook_wave_alt_one_color.png")
w = sprite_sheet.get_size()[0] // 17
h = sprite_sheet.get_size()[1]
HOOK_WAVE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h), (300, 300))
                    for i in range(17)]

BULLET = b"bullet"
sprite_sheet = load_image("bullet_one_color.png")
w = sprite_sheet.get_size()[0] // 10
h = sprite_sheet.get_size()[1]
BULLET_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h), (120, 100))
                 for i in range(10)]