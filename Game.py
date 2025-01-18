from Camera import Camera
from Projectile import Projectile
from ThimeusConstants import (TILE_SIZE, CHARACTER_HEIGHT, COLORS, ENEMY_SETS, SWORD, HOOK, GUN,
                              STAFF, DARK_COLOR, FPS, MAIN_MENU_MODE, STORY_MODE, ARCADE_MODE,
                              LINE_WIDTH)
from ThimeusFunctions import load_image
from Tile import Tile
from Ladder import Ladder
from Spike import Spike
from Liquid import Liquid
from Door import Door
from Player import Player
from Enemy import Enemy
from Weapon import Weapon
import pygame


class Game:
    story_mode_levels = [f"level_{i + 1}.txt" for i in range(30)]

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

        self.font_path = "data/fonts/SatyrSP.otf"
        self.game_mode = MAIN_MENU_MODE
        self.levels = None
        self.camera = None
        self.current_level = 0
        self.clock = pygame.time.Clock()

        self.interface = pygame.sprite.Group()

        self.game_over_label = pygame.sprite.Sprite(self.interface)
        self.game_over_label.image = pygame.font.Font(self.font_path,
                                                      260).render("Игра окончена!", True, "white")
        image_width = self.game_over_label.image.get_size()[0]
        self.game_over_label.rect = self.game_over_label.image.get_rect().move((self.width -
                                                                                image_width) // 2, -220)

        self.results_label = pygame.sprite.Sprite(self.interface)

        btn_size = 150

        self.reload_button = pygame.sprite.Sprite(self.interface)
        self.reload_button.image = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA, 32)
        button_x = (self.width - (btn_size * 2 + btn_size // 2)) // 2
        self.reload_button.rect = self.reload_button.image.get_rect().move(button_x, 860)
        pygame.draw.rect(self.reload_button.image, "white", (0, 0, btn_size, btn_size),
                         LINE_WIDTH * 2, 10)
        self.reload_button.image.blit(pygame.transform.smoothscale(load_image("return.png"),
                                                                   (btn_size, btn_size)), (0, 0))

        self.main_menu_button = pygame.sprite.Sprite(self.interface)
        self.main_menu_button.image = pygame.Surface((btn_size, btn_size), pygame.SRCALPHA, 32)
        button_x = self.reload_button.rect.x + btn_size + btn_size // 2
        self.main_menu_button.rect = self.main_menu_button.image.get_rect().move(button_x, 860)
        pygame.draw.rect(self.main_menu_button.image, "white", (0, 0, btn_size, btn_size),
                         LINE_WIDTH * 2, 10)
        self.main_menu_button.image.blit(pygame.transform.smoothscale(load_image("home.png"),
                                                                      (btn_size, btn_size)), (0, 0))

        Liquid.load_images()
        Projectile.load_images()

    def fade_transition(self, surface):
        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill("black")
        fade_alpha = 0
        while fade_alpha < 255:
            fade_alpha += 10
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
        self.current_level = 0
        self.game_mode = STORY_MODE
        if self.game_mode == STORY_MODE:
            self.levels = Game.story_mode_levels
        elif self.game_mode == ARCADE_MODE:
            pass

    def game_loop(self):
        self.game_over_label.rect.y = -220
        self.reload_button.image.set_alpha(0)
        self.main_menu_button.image.set_alpha(0)

        player, exit_door = self.load_level(self.levels[self.current_level])
        enemies = list(filter(lambda x: isinstance(x, Enemy), self.all_sprites))
        defeat = False
        running = True

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill("black")
        fade_alpha = 255
        faded = False

        while running:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        running = False
                        pygame.quit()
            self.screen.fill(DARK_COLOR)
            for group in self.all_sprites:
                group.update()
                group.draw(self.screen)
            self.clock.tick(FPS)

            if exit_door.exited:
                running = False

            elif player.dead and not defeat:
                defeat = True
                enemies_killed = len([1 for group in enemies if group.dead])
                results_str = [f"Комнат пройдено: {self.current_level + 1}",
                               f"Врагов побеждено: {enemies_killed}"]
                results = list(map(lambda x: pygame.font.Font(self.font_path,
                                                              100).render(x, True, "white"), results_str))
                label_w = max(map(lambda x: x.get_size()[0], results))
                label_h = results[0].get_size()[1]
                self.results_label.image = pygame.Surface((label_w, label_h * len(results_str)),
                                                          pygame.SRCALPHA, 32)
                for i, label in enumerate(results):
                    self.results_label.image.blit(label, (0, i * label_h))
                image_w = self.results_label.image.get_size()[0]
                self.results_label.rect = self.results_label.image.get_rect().move((self.width -
                                                                                    image_w) // 2, 560)
                self.results_label.image.set_alpha(0)

            if defeat:
                if fade_alpha < 220:
                    fade_alpha += 5
                    fade_alpha = fade_alpha if fade_alpha < 220 else 220
                if self.game_over_label.rect.y < 200:
                    self.game_over_label.rect.y += 10
                if self.results_label.image.get_alpha() < 255:
                    self.results_label.image.set_alpha(self.results_label.image.get_alpha() + 5)
                    self.reload_button.image.set_alpha(self.reload_button.image.get_alpha() + 5)
                    self.main_menu_button.image.set_alpha(self.main_menu_button.image.get_alpha() + 5)
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                self.interface.draw(self.screen)

                if pygame.mouse.get_pressed()[0]:
                    if self.reload_button.rect.collidepoint(pygame.mouse.get_pos()):
                        running = False
                    elif self.main_menu_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            if fade_alpha > 0 and not faded:
                fade_alpha -= 10
                fade_alpha = fade_alpha if fade_alpha > 0 else 0
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
            else:
                faded = True

            fps = pygame.font.Font(self.font_path, 150).render(str(round(self.clock.get_fps())), True, "white")
            self.screen.blit(fps, (30, 30))

            pygame.display.flip()
        if not defeat:
            self.current_level = (self.current_level + 1) % 2
        self.fade_transition(self.screen.copy())


    def load_level(self, filename):
        self.clear_all_sprites()

        with open(f"data/levels/{filename}", "r", encoding="utf-8") as file:
            level = file.read().split("\n")
        color = COLORS[level[0]]
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
                    enemy = Enemy(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                  y * TILE_SIZE, CHARACTER_HEIGHT, *ENEMY_SETS[tile], self.all_sprites)
                    self.all_sprites.append(enemy)
                elif tile == "@":
                    player = Player(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                    y * TILE_SIZE, CHARACTER_HEIGHT, COLORS["blue"], self.camera,
                                    self.all_sprites)
                    player.get_weapon(Weapon(player.h, HOOK))
                    player.set_head_sides(3)
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
        for group in self.all_sprites:
            if isinstance(group, Enemy):
                group.set_target(player)
        self.camera.set_target()
        return player, exit_door

