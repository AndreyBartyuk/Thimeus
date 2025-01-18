TILE_SIZE = 100
CHARACTER_HEIGHT = TILE_SIZE * 2
LINE_WIDTH = 5
FPS = 70

MAIN_MENU_MODE = b"main_menu_mode"
STORY_MODE = b"story_mode"
ARCADE_MODE = b"arcade_mode"

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

ENEMY_SETS = {"o": (COLORS["orange"], FLAMETHROWER, 3),
              "y": (COLORS["yellow"], STAFF, 3),
              "g": (COLORS["green"], AXE, 4),
              "b": (COLORS["blue"], HOOK, 3),
              "p": (COLORS["purple"], GUN, 5)}
