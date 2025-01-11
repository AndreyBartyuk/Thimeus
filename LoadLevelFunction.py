from ThimeusConstants import TILE_SIZE, CHARACTER_HEIGHT, COLORS, HOOK, GUN
from Tile import Tile
from Ladder import Ladder
from Human import Human
from Weapon import Weapon


def load_level(filename, all_sprites, walls, ladders, projectiles, camera):
    with open(f"data/levels/{filename}", "r", encoding="utf-8") as file:
        level = file.read().split("\n")
    color = COLORS[level[0]]
    level_map = level[1:]
    map_width = len(level_map[0])
    map_height = len(level_map)
    for y, row in enumerate(level_map):
        for x, tile in enumerate(row):
            if tile == "#":
                moves = [(0, -1), (1, 0), (0, 1), (-1, 0)]
                neighbours = list()
                for x_move, y_move in moves:
                    if 0 <= x + x_move < map_width and 0 <= y + y_move < map_height:
                        if level_map[y + y_move][x + x_move] == "#":
                            neighbours.append(False)
                        else:
                            neighbours.append(True)
                    else:
                        neighbours.append(False)
                Tile(walls, x * TILE_SIZE, y * TILE_SIZE, neighbours, color)
            elif tile == "P":
                human = Human(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                              y * TILE_SIZE, CHARACTER_HEIGHT, COLORS["blue"],
                              walls, ladders, projectiles, camera)
                human.get_weapon(Weapon(human.h, HOOK))
                human.set_head_sides(3)
                all_sprites.append(human)
            elif tile == "|":
                neighbours = [False, False]
                if 0 <= y + 1 < map_height:
                    if level_map[y + 1][x] == "|":
                        neighbours[0] = True
                if 0 <= y - 1 < map_height:
                    if level_map[y - 1][x] == "|":
                        neighbours[1] = True
                Ladder(ladders, x * TILE_SIZE, y * TILE_SIZE, color, *neighbours)
