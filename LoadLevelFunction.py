import pygame.sprite

from ThimeusConstants import TILE_SIZE, CHARACTER_HEIGHT, COLORS, ENEMY_SETS, SWORD, HOOK, GUN, \
    STAFF
from Tile import Tile
from Ladder import Ladder
from Spike import Spike
from Liquid import Liquid
from Door import Door
from Player import Player
from Enemy import Enemy
from Weapon import Weapon


def load_level(filename, all_sprites, camera):
    with open(f"data/levels/{filename}", "r", encoding="utf-8") as file:
        level = file.read().split("\n")
    color = COLORS[level[0]]
    level_map = level[1:]
    map_width = len(level_map[0])
    map_height = len(level_map)
    walls = all_sprites[0]
    ladders = all_sprites[1]
    interactable = all_sprites[2]
    obstacles = all_sprites[3]
    decor = all_sprites[4]
    player = exit_door = None
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
            elif tile in ENEMY_SETS:
                enemy = Enemy(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                              y * TILE_SIZE, CHARACTER_HEIGHT, *ENEMY_SETS[tile], all_sprites)
                all_sprites.append(enemy)
            elif tile == "@":
                player = Player(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                y * TILE_SIZE, CHARACTER_HEIGHT, COLORS["purple"], camera, all_sprites)
                player.get_weapon(Weapon(player.h, GUN))
                player.set_head_sides(5)
                all_sprites.append(player)
                Door(decor, x * TILE_SIZE, (y - 1) * TILE_SIZE, color, False)
            elif tile == "|":
                neighbours = [False, False]
                if 0 <= y + 1 < map_height:
                    if level_map[y + 1][x] == "|":
                        neighbours[0] = True
                if 0 <= y - 1 < map_height:
                    if level_map[y - 1][x] == "|":
                        neighbours[1] = True
                Ladder(ladders, x * TILE_SIZE, y * TILE_SIZE, color, *neighbours)
            elif tile == "^":
                Spike(obstacles, x * TILE_SIZE, y * TILE_SIZE, color)
            elif tile == "~":
                up_free = True
                if 0 <= y - 1 < map_height:
                    if level_map[y - 1][x] == "~":
                        up_free = False
                Liquid(obstacles, x * TILE_SIZE, y * TILE_SIZE, up_free, color)
            elif tile == "E":
                exit_door = Door(interactable, x * TILE_SIZE, y * TILE_SIZE, color, True)
    for group in all_sprites:
        if isinstance(group, Enemy):
            group.set_target(player)
    return player, exit_door
