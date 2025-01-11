from ThimeusFunctions import load_image
import pygame


TILE_SIZE = 100
CHARACTER_HEIGHT = TILE_SIZE * 2
LINE_WIDTH = 5
FPS = 100

DARK_COLOR = "#151515"
COLORS = {"red": "#DE324C", "orange": "#F4895F", "yellow": "#F8E16F",
          "green": "#95CF92", "blue": "#369ACC", "purple": "#9656A2"}

RIGHT_ARM = 1
LEFT_ARM = 0

SWORD = b"sword"
FLAMETHROWER = b"flamethrower"
AXE = b"axe"
STAFF = b"staff"
HOOK = b"hook"
GUN = b"gun"

MELEE_ATTACK = b"melee"
RANGED_ATTACK = b"ranged"

sprite_sheet = load_image("sword_slash_one_color.png")
w = sprite_sheet.get_size()[0] // 5
h = sprite_sheet.get_size()[1]
SWORD_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)),
                                                  (300, 500)) for i in range(5)]

sprite_sheet = load_image("flame_one_color.png")
w = sprite_sheet.get_size()[0] // 61
h = sprite_sheet.get_size()[1]
FLAMETHROWER_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)),
                                                         (200, 200))  for i in range(60)]

sprite_sheet = load_image("axe_hit_one_color.png")
w = sprite_sheet.get_size()[0] // 12
h = sprite_sheet.get_size()[1]
AXE_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                                (200, 200)) for i in range(12)]

sprite_sheet = load_image("thunder_one_color.png")
w = sprite_sheet.get_size()[0] // 5
h = sprite_sheet.get_size()[1]
STAFF_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                                  (150, 150)) for i in range(5)]

sprite_sheet = load_image("hook_wave_alt_one_color.png")
w = sprite_sheet.get_size()[0] // 17
h = sprite_sheet.get_size()[1]
HOOK_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                                 (300, 300)) for i in range(17)]

sprite_sheet = load_image("bullet_one_color.png")
w = sprite_sheet.get_size()[0] // 10
h = sprite_sheet.get_size()[1]
GUN_PROJECTILE_IMAGES = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                                (120, 100)) for i in range(10)]
