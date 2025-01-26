from Camera import Camera
from Interface import Interface
from Projectile import Projectile
from ThimeusConstants import (TILE_SIZE, CHARACTER_HEIGHT, COLORS, ENEMY_SETS, DARK_COLOR,
                              FPS, MAIN_MENU_MODE, STORY_MODE, ARCADE_MODE)
from ThimeusFunctions import load_image
from PlatonicSolid import PlatonicSolid
from Tile import Tile
from Ladder import Ladder
from Spike import Spike
from Liquid import Liquid
from Door import Door
from Player import Player
from Enemy import Enemy
import pygame
import random
import json
import sys


class Game:
    story_mode_levels = [f"level_{i + 1}.txt" for i in range(20)]
    arcade_mode_levels = [f"level_{i + 1}.txt" for i in range(20) if (i + 1) % 4 != 0]

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = pygame.display.get_window_size()

        self.walls = pygame.sprite.Group()
        self.ladders = pygame.sprite.Group()
        self.interactable = pygame.sprite.Group()
        self.decor = pygame.sprite.Group()
        self.obstacles = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        self.all_sprites = [self.walls, self.ladders, self.interactable,
                            self.obstacles, self.decor, self.projectiles]

        self.save_path = "data/save.json"
        self.font_path = "data/fonts/SatyrSP.otf"
        self.game_mode = MAIN_MENU_MODE
        self.levels = None
        self.camera = None
        self.clock = pygame.time.Clock()

        self.interface = pygame.sprite.Group()

        self.game_over_label = pygame.sprite.Sprite(self.interface)
        self.game_over_label.image = pygame.font.Font(self.font_path,
                                                      260).render("Игра окончена!", True, "white")
        image_width = self.game_over_label.image.get_size()[0]
        self.game_over_label.rect = self.game_over_label.image.get_rect().move((self.width - image_width) // 2, -220)
        self.needed_game_over_label_y = -220

        self.results_label = pygame.sprite.Sprite(self.interface)

        self.btn_size = 150
        self.spacing = 100

        self.reload_button = pygame.sprite.Sprite(self.interface)
        self.reload_button.image = pygame.Surface((self.btn_size, self.btn_size), pygame.SRCALPHA, 32)
        self.reload_button.rect = self.reload_button.image.get_rect()
        pygame.draw.rect(self.reload_button.image, "white", (0, 0, self.btn_size, self.btn_size), 10, 10)
        self.reload_button.image.blit(pygame.transform.smoothscale(load_image("return.png"),
                                                                   (self.btn_size, self.btn_size)), (0, 0))

        self.main_menu_button = pygame.sprite.Sprite(self.interface)
        self.main_menu_button.image = pygame.Surface((self.btn_size, self.btn_size), pygame.SRCALPHA, 32)
        self.main_menu_button.rect = self.main_menu_button.image.get_rect()
        pygame.draw.rect(self.main_menu_button.image, "white", (0, 0, self.btn_size, self.btn_size), 10, 10)
        self.main_menu_button.image.blit(pygame.transform.smoothscale(load_image("home.png"),
                                                                      (self.btn_size, self.btn_size)), (0, 0))

        Liquid.load_images()
        Projectile.load_images()

    def fade_transition(self, surface):
        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill("black")
        fade_alpha = 0
        while fade_alpha < 255:
            fade_alpha += 14 # 10
            fade_surface.set_alpha(fade_alpha)
            self.screen.blit(surface, (0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

    def main_loop(self):
        while True:
            if self.game_mode == MAIN_MENU_MODE:
                self.main_menu()
            else:
                self.game_loop()

    def clear_all_sprites(self):
        self.all_sprites = self.all_sprites[:6]
        for group in self.all_sprites:
            group.empty()

    def main_menu(self):
        self.game_mode = STORY_MODE

    def game_loop(self):
        with open(self.save_path) as file:
            save_data = json.load(file)

        if self.game_mode == STORY_MODE:
            level_data = save_data["story_mode_save"]
            current_level = level_data["current_level"]
            if current_level >= len(Game.story_mode_levels):
                self.fade_transition(self.screen.copy())
                return self.story_mode_end()
            filename = Game.story_mode_levels[current_level]
        else:
            level_data = save_data["arcade_mode_save"]
            filename = random.choice(Game.arcade_mode_levels)

        self.game_over_label.rect.y = -220
        self.reload_button.image.set_alpha(0)
        self.main_menu_button.image.set_alpha(0)

        player, exit_door, interface = self.load_level(filename)
        enemies = list(filter(lambda x: isinstance(x, Enemy), self.all_sprites))
        defeat = False
        running = True

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill("black")
        fade_alpha = 255

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif defeat and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_mode == STORY_MODE and self.reload_button.rect.collidepoint(event.pos):
                        running = False
                    elif self.main_menu_button.rect.collidepoint(event.pos):
                        self.game_mode = MAIN_MENU_MODE
                        running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.fade_transition(self.screen.copy())
                    self.game_mode = MAIN_MENU_MODE
                    return None

            solid_found = False
            for sprite in self.interactable:
                if isinstance(sprite, PlatonicSolid):
                    solid_found = True
                    break
            for sprite in self.interactable:
                if not isinstance(sprite, PlatonicSolid):
                    sprite.interactable = not solid_found

            self.screen.fill(DARK_COLOR)
            for group in self.all_sprites:
                group.update()
                group.draw(self.screen)

            if exit_door.exited:
                running = False

            elif player.dead and not defeat:
                defeat = True

                enemies_killed = level_data["enemies_killed"] + len([1 for group in enemies if group.dead])
                levels_completed = level_data["levels_completed"]
                results_str = [f"Комнат пройдено: {levels_completed}",
                               f"Врагов побеждено: {enemies_killed}"]

                if self.game_mode == ARCADE_MODE:
                    points = levels_completed * enemies_killed
                    results_str.append(f"Очки: {points}")

                    with open(self.save_path) as file:
                        save_data = json.load(file)
                    record = False
                    if levels_completed > save_data["arcade_mode_record"]["levels"]:
                        save_data["arcade_mode_record"]["levels"] = levels_completed
                        results_str[0] += "!"
                        record = True
                    if enemies_killed > save_data["arcade_mode_record"]["enemies"]:
                        save_data["arcade_mode_record"]["enemies"] = enemies_killed
                        results_str[1] += "!"
                        record = True
                    if points > save_data["arcade_mode_record"]["points"]:
                        save_data["arcade_mode_record"]["points"] = points
                        results_str[2] += "!"
                        record = True
                    save_data["arcade_mode_save"]["current_health"] = 100
                    save_data["arcade_mode_save"]["current_power"] = 0
                    save_data["arcade_mode_save"]["enemies_killed"] = 0
                    save_data["arcade_mode_save"]["levels_completed"] = 0
                    if record:
                        results_str.append("Новый рекорд!")
                    with open(self.save_path, "w") as file:
                        json.dump(save_data, file, indent=2)

                font = pygame.font.Font(self.font_path, 100)
                results = [font.render(line, True, COLORS["red"] if "!" in line else "white") for line in results_str]
                label_w = max(map(lambda x: x.get_size()[0], results))
                label_h = results[0].get_size()[1]
                self.results_label.image = pygame.Surface((label_w, label_h * len(results_str)),
                                                          pygame.SRCALPHA, 32)
                for i, label in enumerate(results):
                    self.results_label.image.blit(label, (0, i * label_h))
                self.results_label.rect = self.results_label.image.get_rect()
                self.results_label.rect.center = self.screen.get_rect().center
                self.results_label.image.set_alpha(0)

                self.needed_game_over_label_y = self.results_label.rect.top - self.spacing - self.game_over_label.rect.h

                self.reload_button.rect.top = self.main_menu_button.rect.top = (self.results_label.rect.bottom +
                                                                                self.spacing)
                if self.game_mode == STORY_MODE:
                    self.reload_button.rect.right = self.screen.get_rect().centerx - self.spacing // 2
                    self.main_menu_button.rect.left = self.screen.get_rect().centerx + self.spacing // 2
                else:
                    self.main_menu_button.rect.centerx = self.screen.get_rect().centerx

            if defeat:
                if fade_alpha < 220:
                    fade_alpha += 7 # 5
                    fade_alpha = fade_alpha if fade_alpha < 220 else 220
                if self.game_over_label.rect.y < self.needed_game_over_label_y:
                    self.game_over_label.rect.y += 14 # 10
                    if self.game_over_label.rect.y > self.needed_game_over_label_y:
                        self.game_over_label.rect.y = self.needed_game_over_label_y
                if self.results_label.image.get_alpha() < 255:
                    self.results_label.image.set_alpha(self.results_label.image.get_alpha() + 7) # 5
                    if self.game_mode == STORY_MODE:
                        self.reload_button.image.set_alpha(self.reload_button.image.get_alpha() + 7)
                    self.main_menu_button.image.set_alpha(self.main_menu_button.image.get_alpha() + 7)
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                self.interface.draw(self.screen)

            if fade_alpha > 0 and not defeat:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            fps = pygame.font.Font(self.font_path, 150).render(str(round(self.clock.get_fps())), True, "white")
            self.screen.blit(fps, (self.width - 170, 50))

            pygame.display.flip()
            self.clock.tick(FPS)

        if not defeat:
            self.save_data(interface, enemies)

        self.fade_transition(self.screen.copy())

    def save_data(self, interface, enemies):
        with open(self.save_path) as file:
            save_data = json.load(file)
        if self.game_mode == STORY_MODE:
            save_data["story_mode_save"]["current_health"] = 100
            save_data["story_mode_save"]["current_power"] = interface.current_power
            save_data["story_mode_save"]["current_level"] += 1
            save_data["story_mode_save"]["powers_amount"] = interface.powers_amount
            save_data["story_mode_save"]["enemies_killed"] += len([1 for group in enemies if group.dead])
            save_data["story_mode_save"]["levels_completed"] += 1
        elif self.game_mode == ARCADE_MODE:
            save_data["arcade_mode_save"]["current_health"] = 100
            save_data["arcade_mode_save"]["current_power"] = interface.current_power
            save_data["arcade_mode_save"]["enemies_killed"] += len([1 for group in enemies if group.dead])
            save_data["arcade_mode_save"]["levels_completed"] += 1
        with open(self.save_path, "w") as file:
            json.dump(save_data, file, indent=2)

    def load_level(self, filename):
        self.clear_all_sprites()

        with open(f"data/levels/{filename}", "r", encoding="utf-8") as file:
            level = file.read().split("\n")

        color = COLORS[level[0]] if self.game_mode == STORY_MODE else random.choice(list(COLORS.values())[1:])
        level_map = level[1:]
        map_width = len(level_map[0])
        map_height = len(level_map)
        walls = self.all_sprites[0]
        ladders = self.all_sprites[1]
        interactable = self.all_sprites[2]
        obstacles = self.all_sprites[3]
        decor = self.all_sprites[4]
        player = exit_door = None
        self.camera = Camera(self.all_sprites)
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
                    enemy_set = (ENEMY_SETS[tile] if self.game_mode == STORY_MODE
                                 else list(ENEMY_SETS.values())[list(COLORS.values())[1:].index(color)])
                    enemy = Enemy(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                  y * TILE_SIZE, CHARACTER_HEIGHT, *enemy_set, self.all_sprites)
                    self.all_sprites.append(enemy)
                elif tile == "@":
                    player = Player(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                    y * TILE_SIZE, CHARACTER_HEIGHT, COLORS["red"], self.camera,
                                    self.all_sprites)
                    self.all_sprites.append(player)
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
                elif tile in ["^", "<", "v", ">"]:
                    direction = ["^", "<", "v", ">"].index(tile)
                    Spike(obstacles, x * TILE_SIZE, y * TILE_SIZE, direction, color)
                elif tile == "~":
                    up_free = True
                    if 0 <= y - 1 < map_height:
                        if level_map[y - 1][x] == "~":
                            up_free = False
                    Liquid(obstacles, x * TILE_SIZE, y * TILE_SIZE, up_free, color)
                elif tile == "E":
                    exit_door = Door(interactable, x * TILE_SIZE, y * TILE_SIZE, color, True)
                elif tile.isdigit():
                    PlatonicSolid(interactable, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, tile, True)
        for group in self.all_sprites:
            if isinstance(group, Enemy):
                group.set_target(player)
        self.camera.set_target()

        with open(self.save_path) as file:
            save_data = json.load(file)

        level_data = None
        powers_amount = 6
        if self.game_mode == STORY_MODE:
            level_data = save_data["story_mode_save"]
            powers_amount = level_data["powers_amount"]
        elif self.game_mode == ARCADE_MODE:
            level_data = save_data["arcade_mode_save"]

        current_health = level_data["current_health"]
        current_power = level_data["current_power"]

        player.health = current_health

        interface = Interface(player, powers_amount, current_power, self.all_sprites)
        self.all_sprites.append(interface)
        return player, exit_door, interface

    def story_mode_end(self):
        with open(self.save_path) as file:
            save_data = json.load(file)
        save_data["story_mode_save"]["current_health"] = 100
        save_data["story_mode_save"]["current_power"] = 0
        save_data["story_mode_save"]["current_level"] = 0
        save_data["story_mode_save"]["powers_amount"] = 1
        save_data["story_mode_save"]["enemies_killed"] = 0
        save_data["story_mode_save"]["levels_completed"] = 0
        save_data["arcade_mode_unlocked"] = True
        with open(self.save_path, "w") as file:
            json.dump(save_data, file, indent=2)

        end_group = pygame.sprite.Group()

        andrey = pygame.sprite.Sprite(end_group)
        andrey.image = pygame.transform.smoothscale_by(load_image("andrey_.png"), 0.5)
        andrey.rect = andrey.image.get_rect()
        andrey.rect.bottomleft = self.screen.get_rect().bottomleft

        artyom = pygame.sprite.Sprite(end_group)
        artyom.image = pygame.transform.smoothscale_by(load_image("artyom_.png"), 0.5)
        artyom.rect = artyom.image.get_rect()
        artyom.rect.bottomright = self.screen.get_rect().bottomright

        spacing = 100

        end_label = pygame.sprite.Sprite(end_group)
        end_strings = ["Режим Аркады теперь", "доступен в главном меню!"]
        results = list(map(lambda x: pygame.font.Font(self.font_path, 100).render(x, True, "white"), end_strings))
        label_w = max(map(lambda x: x.get_size()[0], results))
        label_h = results[0].get_size()[1]
        end_label.image = pygame.Surface((label_w, label_h * len(end_strings)), pygame.SRCALPHA, 32)
        for i, label in enumerate(results):
            end_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
        image_w, image_h = end_label.image.get_size()
        end_label.rect = end_label.image.get_rect().move((self.width - image_w) // 2, (self.height - image_h) // 2)

        thank_label = pygame.sprite.Sprite(end_group)
        thank_label.image = pygame.font.Font(self.font_path, 250).render("Спасибо за игру!", True, "white")
        thank_label.rect = thank_label.image.get_rect().move((self.width - thank_label.image.get_width()) // 2, 0)
        thank_label.rect.bottom = end_label.rect.top - spacing

        main_menu_button = pygame.sprite.Sprite(end_group)
        main_menu_button.image = self.main_menu_button.image.copy()
        main_menu_button.image.set_alpha(255)
        main_menu_button.rect = main_menu_button.image.get_rect().move((self.width - self.btn_size) // 2, 0)
        main_menu_button.rect.top = end_label.rect.bottom + spacing

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill("black")
        fade_alpha = 255

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if main_menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            self.screen.fill(DARK_COLOR)
            end_group.update()
            end_group.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

