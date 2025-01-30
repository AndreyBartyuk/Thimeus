from Camera import Camera
from Interface import Interface
from Projectile import Projectile
from ThimeusConstants import (TILE_SIZE, CHARACTER_HEIGHT, COLORS, ENEMY_SETS, DARK_COLOR,
                              FPS, MAIN_MENU_MODE, STORY_MODE, ARCADE_MODE, RECORD_DISPLAY_MODE, INFO_DISPLAY_MODE,
                              CONTROLS_DISPLAY_MODE)
from ThimeusFunctions import load_image, change_color, colors_are_close
from PlatonicSolid import PlatonicSolid
from Tile import Tile
from Ladder import Ladder
from Spike import Spike
from Liquid import Liquid
from Door import Door
from Player import Player
from Enemy import Enemy
from math import sin, cos, pi
import pygame
import random
import json
import sys


# Main class of the Game
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

        self.btn_size = 150
        self.spacing = 100

        # Main menu interface
        self.main_menu_interface = pygame.sprite.Group()

        self.main_label = pygame.sprite.Sprite(self.main_menu_interface)
        self.main_label.image = pygame.font.Font(self.font_path, 260).render("Тимей", True, "white")
        self.main_label.rect = self.main_label.image.get_rect()

        self.story_btn = pygame.sprite.Sprite(self.main_menu_interface)
        self.story_btn.image = pygame.Surface((780, 130), pygame.SRCALPHA, 32)
        text = pygame.font.Font(self.font_path, 110).render("Режим Истории", True, "white")
        icon = pygame.transform.smoothscale(load_image("scroll.png"), (110, 110))
        self.story_btn.image.blit(icon, (10, 10))
        self.story_btn.image.blit(text, (130, 20))
        pygame.draw.rect(self.story_btn.image, "white", (0, 0, *self.story_btn.image.get_size()), 10, 10)
        self.story_btn.rect = self.story_btn.image.get_rect()

        self.arcade_btn = pygame.sprite.Sprite(self.main_menu_interface)
        self.arcade_btn.image = pygame.Surface((780, 130), pygame.SRCALPHA, 32)
        text = pygame.font.Font(self.font_path, 110).render("Режим Аркады", True, "white")
        icon = pygame.transform.smoothscale(load_image("joystick.png"), (110, 110))
        self.arcade_btn.image.blit(icon, (10, 10))
        self.arcade_btn.image.blit(text, (130, 20))
        pygame.draw.rect(self.arcade_btn.image, "white", (0, 0, *self.arcade_btn.image.get_size()), 10, 10)
        self.arcade_btn.rect = self.arcade_btn.image.get_rect()

        self.exit_btn = pygame.sprite.Sprite(self.main_menu_interface)
        self.exit_btn.image = pygame.transform.smoothscale(load_image("power.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.exit_btn.image, "white", (0, 0, *self.exit_btn.image.get_size()), 10, 10)
        self.exit_btn.rect = self.exit_btn.image.get_rect()

        self.controls_btn = pygame.sprite.Sprite(self.main_menu_interface)
        self.controls_btn.image = pygame.transform.smoothscale(load_image("board.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.controls_btn.image, "white", (0, 0, *self.controls_btn.image.get_size()), 10, 10)
        self.controls_btn.rect = self.controls_btn.image.get_rect()

        self.info_btn = pygame.sprite.Sprite(self.main_menu_interface)
        self.info_btn.image = pygame.transform.smoothscale(load_image("info.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.info_btn.image, "white", (0, 0, *self.info_btn.image.get_size()), 10, 10)
        self.info_btn.rect = self.info_btn.image.get_rect()

        self.main_menu_solids = [PlatonicSolid(self.main_menu_interface, 0, 0, 200, i + 1, False) for i in range(5)]

        # Record display interface
        self.record_display_interface = pygame.sprite.Group()

        self.record_header = pygame.sprite.Sprite(self.record_display_interface)
        self.record_header.image = pygame.font.Font(self.font_path, 260).render("Аркада", True, "white")
        self.record_header.rect = self.record_header.image.get_rect()

        self.record_label = pygame.sprite.Sprite(self.record_display_interface)

        self.play_button = pygame.sprite.Sprite(self.record_display_interface)
        self.play_button.image = pygame.transform.smoothscale(load_image("right.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.play_button.image, "white", (0, 0, *self.play_button.image.get_size()), 10, 10)
        self.play_button.rect = self.play_button.image.get_rect()

        sprite_sheet = load_image("infinity_spritesheet.png")
        w = sprite_sheet.get_size()[0] // 20
        h = sprite_sheet.get_size()[1]
        self.infinity_frames = list()
        for frame in [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)),
                                             (500, 200)) for i in range(20)]:
            self.infinity_frames += [pygame.transform.rotate(frame, 270)] * 4

        self.infinity_right = pygame.sprite.Sprite(self.record_display_interface)
        self.infinity_right.image = self.infinity_frames[0]
        self.infinity_right.rect = self.infinity_right.image.get_rect()

        self.infinity_left = pygame.sprite.Sprite(self.record_display_interface)
        self.infinity_left.image = self.infinity_frames[0]
        self.infinity_left.rect = self.infinity_left.image.get_rect()

        # Controls display interface
        self.controls_display_interface = pygame.sprite.Group()

        self.controls_header = pygame.sprite.Sprite(self.controls_display_interface)
        self.controls_header.image = pygame.font.Font(self.font_path, 260).render("Управление", True, "white")
        self.controls_header.rect = self.controls_header.image.get_rect()

        self.controls_label = pygame.sprite.Sprite(self.controls_display_interface)
        controls_strings = sorted(["A, D - Движение влево, вправо", "Пробел - Прыжок", "W - Движение по лестнице",
                                   "Левый Shift - Рывок", "ЛКМ - Атака", "Escape - Выход в главное меню",
                                   "1, 2, 3, 4, 5, 6 - Выбор силы", "R - Взаимодействие"], key=len, reverse=True)
        results = list(map(lambda x: pygame.font.Font(self.font_path, 60).render(x, True, "white"), controls_strings))
        label_w = max(map(lambda x: x.get_size()[0], results))
        label_h = results[0].get_size()[1]
        self.controls_label.image = pygame.Surface((label_w, label_h * len(controls_strings)), pygame.SRCALPHA, 32)
        for i, label in enumerate(results):
            self.controls_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
        self.controls_label.rect = self.controls_label.image.get_rect()

        self.controls_solid = PlatonicSolid(self.controls_display_interface, 0, 0, 200, 0, False)

        # Information display interface
        self.info_display_interface = pygame.sprite.Group()

        self.info_header = pygame.sprite.Sprite(self.info_display_interface)
        self.info_header.image = pygame.font.Font(self.font_path, 260).render("Информация", True, "white")
        self.info_header.rect = self.info_header.image.get_rect()

        self.info_solids = [PlatonicSolid(self.info_display_interface, 0, 0, 200, i + 1, False) for i in range(5)]

        self.info_label = pygame.sprite.Sprite(self.info_display_interface)
        info_strings = ["\"Тимей\" - это 2D RPG с элементами платформера, ",
                        "вдохновленная одноименным трактатом Платона.",
                        "Игрокам предстоит исследовать мир, основанный на концепции ",
                        "пяти Платоновых тел, каждое из которых ассоциируется ",
                        "с одной из стихий. Геймплей сочетает в себе ",
                        "сражения с противниками и платформерные элементы.", "",
                        "Разработчики: Бартюк Андрей, Беликов Артём"]
        results = list(map(lambda x: pygame.font.Font(self.font_path, 60).render(x, True, "white"), info_strings))
        label_w = max(map(lambda x: x.get_size()[0], results))
        label_h = results[0].get_size()[1]
        self.info_label.image = pygame.Surface((label_w, label_h * len(info_strings)), pygame.SRCALPHA, 32)
        for i, label in enumerate(results):
            self.info_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
        self.info_label.rect = self.info_label.image.get_rect()

        # Story mode end interface
        self.end_interface = pygame.sprite.Group()

        self.andrey = pygame.sprite.Sprite(self.end_interface)
        self.andrey.image = pygame.transform.smoothscale_by(load_image("andrey_.png"), 0.5)
        self.andrey.rect = self.andrey.image.get_rect()

        self.artyom = pygame.sprite.Sprite(self.end_interface)
        self.artyom.image = pygame.transform.smoothscale_by(load_image("artyom_.png"), 0.5)
        self.artyom.rect = self.artyom.image.get_rect()

        self.end_label = pygame.sprite.Sprite(self.end_interface)
        end_strings = ["Режим Аркады теперь", "доступен в главном меню!"]
        results = list(map(lambda x: pygame.font.Font(self.font_path, 100).render(x, True, "white"), end_strings))
        label_w = max(map(lambda x: x.get_size()[0], results))
        label_h = results[0].get_size()[1]
        self.end_label.image = pygame.Surface((label_w, label_h * len(end_strings)), pygame.SRCALPHA, 32)
        for i, label in enumerate(results):
            self.end_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
        self.end_label.rect = self.end_label.image.get_rect()

        self.end_header = pygame.sprite.Sprite(self.end_interface)
        self.end_header.image = pygame.font.Font(self.font_path, 250).render("Спасибо за игру!", True, "white")
        self.end_header.rect = self.end_header.image.get_rect()

        # Game over interface
        self.game_over_interface = pygame.sprite.Group()

        self.game_over_label = pygame.sprite.Sprite(self.game_over_interface)
        self.game_over_label.image = pygame.font.Font(self.font_path, 260).render("Игра окончена!", True, "white")
        image_width = self.game_over_label.image.get_size()[0]
        self.game_over_label.rect = self.game_over_label.image.get_rect().move((self.width - image_width) // 2, -220)
        self.needed_game_over_label_y = -220

        self.results_label = pygame.sprite.Sprite(self.game_over_interface)

        self.reload_btn = pygame.sprite.Sprite(self.game_over_interface)
        self.reload_btn.image = pygame.transform.smoothscale(load_image("return.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.reload_btn.image, "white", (0, 0, self.btn_size, self.btn_size), 10, 10)
        self.reload_btn.rect = self.reload_btn.image.get_rect()

        self.main_menu_btn = pygame.sprite.Sprite(self.game_over_interface, self.record_display_interface,
                                                  self.info_display_interface, self.controls_display_interface,
                                                  self.end_interface)
        self.main_menu_btn.image = pygame.transform.smoothscale(load_image("home.png"), (self.btn_size, self.btn_size))
        pygame.draw.rect(self.main_menu_btn.image, "white", (0, 0, self.btn_size, self.btn_size), 10, 10)
        self.main_menu_btn.rect = self.main_menu_btn.image.get_rect()

        Liquid.load_images()
        Projectile.load_images()

    # Fade transition for changing the scene
    def fade_transition(self, surface):
        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 0
        while fade_alpha < 255:
            fade_alpha += 14
            fade_surface.set_alpha(fade_alpha)
            self.screen.blit(surface, (0, 0))
            self.screen.blit(fade_surface, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)

    # Main loop of the Game
    def main_loop(self):
        while True:
            if self.game_mode == MAIN_MENU_MODE:
                self.main_menu()
            elif self.game_mode == INFO_DISPLAY_MODE:
                self.info_display()
            elif self.game_mode == CONTROLS_DISPLAY_MODE:
                self.controls_display()
            elif self.game_mode == RECORD_DISPLAY_MODE:
                self.record_display()
            else:
                self.game_loop()

    # Clear all sprites from game loop
    def clear_all_sprites(self):
        self.all_sprites = self.all_sprites[:6]
        for group in self.all_sprites:
            group.empty()

    # Main menu loop
    def main_menu(self):
        self.story_btn.rect.centerx = self.screen.get_rect().centerx
        self.story_btn.rect.top = self.screen.get_rect().centery
        self.arcade_btn.rect.centerx = self.screen.get_rect().centerx
        self.arcade_btn.rect.top = self.story_btn.rect.bottom + self.spacing // 2

        self.main_label.rect.centerx = self.screen.get_rect().centerx
        self.main_label.rect.bottom = self.story_btn.rect.top - self.spacing

        self.exit_btn.rect.bottomleft = (self.spacing // 2, self.height - self.spacing // 2)
        self.controls_btn.rect.x = self.exit_btn.rect.x
        self.controls_btn.rect.bottom = self.exit_btn.rect.top - self.spacing // 2
        self.info_btn.rect.x = self.controls_btn.rect.x
        self.info_btn.rect.bottom = self.controls_btn.rect.top - self.spacing // 2

        with open(self.save_path) as file:
            save_data = json.load(file)
        arcade_unlocked = save_data["arcade_mode_unlocked"]
        self.arcade_btn.image.set_alpha(255)
        if not arcade_unlocked:
            self.arcade_btn.image.set_alpha(0)

        angle = 0
        radius = 600
        center_x, center_y = self.screen.get_rect().center

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        while self.game_mode == MAIN_MENU_MODE:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.story_btn.rect.collidepoint(mouse_pos):
                        self.game_mode = STORY_MODE
                    elif arcade_unlocked and self.arcade_btn.rect.collidepoint(mouse_pos):
                        self.game_mode = RECORD_DISPLAY_MODE
                    elif self.controls_btn.rect.collidepoint(mouse_pos):
                        self.game_mode = CONTROLS_DISPLAY_MODE
                    elif self.info_btn.rect.collidepoint(mouse_pos):
                        self.game_mode = INFO_DISPLAY_MODE
                    elif self.exit_btn.rect.collidepoint(mouse_pos):
                        sys.exit()

            points = [((center_x + radius * cos(angle + 2 * pi * i / 5)),
                       (center_y + radius * sin(angle + 2 * pi * i / 5))) for i in range(5)]
            for solid, pos in zip(self.main_menu_solids, points):
                solid.rect.center = pos
            angle = (angle + 0.01) % (2 * pi)

            self.screen.fill(DARK_COLOR)

            self.main_menu_interface.update()
            self.main_menu_interface.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.fade_transition(self.screen.copy())

    # Controls display loop
    def controls_display(self):
        self.controls_label.rect.center = self.screen.get_rect().center

        self.controls_header.rect.centerx = self.screen.get_rect().centerx
        self.controls_header.rect.bottom = self.controls_label.rect.top - self.spacing

        self.controls_solid.rect.centerx = self.screen.get_rect().centerx
        self.controls_solid.rect.top = self.controls_label.rect.bottom + self.spacing

        self.main_menu_btn.image.set_alpha(255)
        self.main_menu_btn.rect.bottomleft = (self.spacing // 2, self.height - self.spacing // 2)

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.main_menu_btn.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            self.screen.fill(DARK_COLOR)
            self.controls_display_interface.update()
            self.controls_display_interface.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.fade_transition(self.screen.copy())

    # Info display loop
    def info_display(self):
        self.info_label.rect.center = self.screen.get_rect().center

        self.info_header.rect.centerx = self.screen.get_rect().centerx
        self.info_header.rect.bottom = self.info_label.rect.top - self.spacing

        self.main_menu_btn.image.set_alpha(255)
        self.main_menu_btn.rect.bottomleft = (self.spacing // 2, self.height - self.spacing // 2)

        start = self.screen.get_rect().centerx - 500 - self.spacing
        step = 200 + self.spacing // 2
        for i, solid in enumerate(self.info_solids):
            solid.rect.x = start + i * step
            solid.rect.top = self.info_label.rect.bottom + self.spacing

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.main_menu_btn.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            self.screen.fill(DARK_COLOR)
            self.info_display_interface.update()
            self.info_display_interface.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.fade_transition(self.screen.copy())

    # Record display loop
    def record_display(self):
        with open(self.save_path) as file:
            save_data = json.load(file)
        enemies, levels, points = save_data["arcade_mode_record"].values()
        record_strings = ["Рекорды:", f"Врагов побеждено: {enemies}",
                          f"Комнат пройдено: {levels}", f"Очков набрано: {points}"]
        results = list(map(lambda x: pygame.font.Font(self.font_path, 100).render(x, True, "white"), record_strings))
        label_w = max(map(lambda x: x.get_size()[0], results))
        label_h = results[0].get_size()[1]
        self.record_label.image = pygame.Surface((label_w, label_h * len(record_strings)), pygame.SRCALPHA, 32)
        for i, label in enumerate(results):
            self.record_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
        self.record_label.rect = self.record_label.image.get_rect()
        self.record_label.rect.center = self.screen.get_rect().center

        self.record_header.rect.centerx = self.screen.get_rect().centerx
        self.record_header.rect.bottom = self.record_label.rect.top - self.spacing

        self.play_button.rect.centerx = self.screen.get_rect().centerx
        self.play_button.rect.top = self.record_label.rect.bottom + self.spacing

        self.infinity_right.rect.centery = self.screen.get_rect().centery
        self.infinity_right.rect.left = self.record_label.rect.right + self.spacing * 2
        self.infinity_left.rect.centery = self.screen.get_rect().centery
        self.infinity_left.rect.right = self.record_label.rect.left - self.spacing * 2
        colors = list(COLORS.values())
        current_color = 0
        first_rgb = pygame.color.Color(colors[current_color])
        second_rgb = pygame.color.Color(colors[current_color + 1])
        current_frame = 0

        self.main_menu_btn.image.set_alpha(255)
        self.main_menu_btn.rect.bottomleft = (self.spacing // 2, self.height - self.spacing // 2)

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_button.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = ARCADE_MODE
                        running = False
                    elif self.main_menu_btn.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            current_frame = (current_frame + 1) % len(self.infinity_frames)
            new_color = first_rgb.lerp(second_rgb, 0.1)
            frame = change_color(self.infinity_frames[current_frame].copy(), new_color)
            self.infinity_right.image = self.infinity_left.image = frame
            first_rgb = new_color

            if colors_are_close(first_rgb, second_rgb):
                current_color = (current_color + 1) % len(colors)
                first_rgb = pygame.color.Color(colors[current_color])
                second_rgb = pygame.color.Color(colors[(current_color + 1) % len(colors)])

            self.screen.fill(DARK_COLOR)
            self.record_display_interface.update()
            self.record_display_interface.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.fade_transition(self.screen.copy())

    # Game loop
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
        self.reload_btn.image.set_alpha(0)
        self.main_menu_btn.image.set_alpha(0)

        player, exit_door, interface = self.load_level(filename)
        enemies = list(filter(lambda x: isinstance(x, Enemy), self.all_sprites))
        defeat = False
        running = True

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif defeat and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.game_mode == STORY_MODE and self.reload_btn.rect.collidepoint(event.pos):
                        running = False
                    elif self.main_menu_btn.rect.collidepoint(event.pos):
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
                self.results_label.image = pygame.Surface((label_w, label_h * len(results_str)), pygame.SRCALPHA, 32)
                for i, label in enumerate(results):
                    self.results_label.image.blit(label, ((label_w - label.get_size()[0]) // 2, i * label_h))
                self.results_label.rect = self.results_label.image.get_rect()
                self.results_label.rect.center = self.screen.get_rect().center
                self.results_label.image.set_alpha(0)

                self.needed_game_over_label_y = self.results_label.rect.top - self.spacing - self.game_over_label.rect.h

                self.reload_btn.rect.top = self.main_menu_btn.rect.top = (self.results_label.rect.bottom +
                                                                          self.spacing)
                if self.game_mode == STORY_MODE:
                    self.reload_btn.rect.right = self.screen.get_rect().centerx - self.spacing // 2
                    self.main_menu_btn.rect.left = self.screen.get_rect().centerx + self.spacing // 2
                else:
                    self.main_menu_btn.rect.centerx = self.screen.get_rect().centerx

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
                        self.reload_btn.image.set_alpha(self.reload_btn.image.get_alpha() + 7)
                    self.main_menu_btn.image.set_alpha(self.main_menu_btn.image.get_alpha() + 7)
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))
                self.game_over_interface.draw(self.screen)

            if fade_alpha > 0 and not defeat:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            # fps = pygame.font.Font(self.font_path, 150).render(str(round(self.clock.get_fps())), True, "white")
            # self.screen.blit(fps, (self.width - 170, 50))

            pygame.display.flip()
            self.clock.tick(FPS)

        if not defeat:
            self.save_data(interface, enemies)

        self.fade_transition(self.screen.copy())

    # Save the changed data
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

    # Load the level for the game loop
    def load_level(self, filename):
        self.clear_all_sprites()

        with open(f"data/levels/{filename}", "r", encoding="utf-8") as file:
            level = file.read().split("\n")
        with open(self.save_path) as file:
            save_data = json.load(file)

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
                    enemy_level = 0
                    if self.game_mode == ARCADE_MODE:
                        enemy_level = save_data["arcade_mode_save"]["levels_completed"] // 10
                    enemy = Enemy(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                  y * TILE_SIZE, CHARACTER_HEIGHT, *enemy_set, enemy_level, self.all_sprites)
                    self.all_sprites.append(enemy)
                elif tile == "@":
                    player = Player(x * TILE_SIZE + (TILE_SIZE - CHARACTER_HEIGHT // 3) // 2,
                                    y * TILE_SIZE, CHARACTER_HEIGHT, COLORS["red"], self.camera,
                                    self.all_sprites)
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
        self.all_sprites.append(player)
        self.camera.set_target()

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

    # Story mode end loop
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

        self.andrey.rect.bottomleft = self.screen.get_rect().bottomleft
        self.artyom.rect.bottomright = self.screen.get_rect().bottomright

        self.end_label.rect.center = self.screen.get_rect().center
        self.end_header.rect.centerx = self.screen.get_rect().centerx
        self.end_header.rect.bottom = self.end_label.rect.top - self.spacing

        self.main_menu_btn.image.set_alpha(255)
        self.main_menu_btn.rect.centerx = self.screen.get_rect().centerx
        self.main_menu_btn.rect.top = self.end_label.rect.bottom + self.spacing

        fade_surface = pygame.Surface(pygame.display.get_window_size())
        fade_surface.fill(DARK_COLOR)
        fade_alpha = 255

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.main_menu_btn.rect.collidepoint(pygame.mouse.get_pos()):
                        self.game_mode = MAIN_MENU_MODE
                        running = False

            self.screen.fill(DARK_COLOR)
            self.end_interface.update()
            self.end_interface.draw(self.screen)

            if fade_alpha > 0:
                fade_alpha -= 14
                fade_surface.set_alpha(fade_alpha)
                self.screen.blit(fade_surface, (0, 0))

            pygame.display.flip()
            self.clock.tick(FPS)

        self.fade_transition(self.screen.copy())
