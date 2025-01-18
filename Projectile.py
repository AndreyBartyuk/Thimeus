from math import sin, cos, radians
from ThimeusConstants import SWORD, FLAMETHROWER, AXE, STAFF, HOOK, GUN, COLORS
from ThimeusFunctions import load_image
import pygame


class Projectile(pygame.sprite.Sprite):
    images = dict()

    @staticmethod
    def load_images():
        sprite_sheet = load_image("sword_projectile.png")
        w = sprite_sheet.get_size()[0] // 5
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)),
                                          (300, 500)) for i in range(5)]
        Projectile.images[SWORD] = sprites

        sprite_sheet = load_image("flamethrower_projectile.png")
        w = sprite_sheet.get_size()[0] // 61
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface((i * w, 0, w, h)),
                                          (200, 200)) for i in range(60)]
        Projectile.images[FLAMETHROWER] = sprites

        sprite_sheet = load_image("axe_projectile.png")
        w = sprite_sheet.get_size()[0] // 12
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                          (200, 200)) for i in range(12)]
        Projectile.images[AXE] = sprites

        sprite_sheet = load_image("staff_projectile.png")
        w = sprite_sheet.get_size()[0] // 5
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                          (150, 150)) for i in range(5)]
        Projectile.images[STAFF] = sprites

        sprite_sheet = load_image("hook_projectile.png")
        w = sprite_sheet.get_size()[0] // 17
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                          (300, 300)) for i in range(17)]
        Projectile.images[HOOK] = sprites

        sprite_sheet = load_image("gun_projectile.png")
        w = sprite_sheet.get_size()[0] // 10
        h = sprite_sheet.get_size()[1]
        sprites = [pygame.transform.scale(sprite_sheet.subsurface(i * w, 0, w, h),
                                          (120, 100)) for i in range(10)]
        Projectile.images[GUN] = sprites

    def __init__(self, group, x, y, speed, angle, kind, damage, is_player, all_sprites, flip=False):
        super().__init__(group)
        self.kind = kind
        self.angle = angle
        self.speed_x = speed * cos(radians(self.angle))
        self.speed_y = speed * sin(radians(self.angle))
        self.current_frame = 0
        self.frame_amount = 0
        self.frames = list()
        sprites = Projectile.images[self.kind]

        self.walls = all_sprites[0]
        self.all_sprites = all_sprites

        self.is_player = is_player
        self.screen_rect = pygame.Rect(0, 0, *pygame.display.get_window_size())

        self.damage = damage
        target = "Enemy" if self.is_player else "Player"
        self.targets = [[group, False] for group in self.all_sprites
                        if group.__class__.__name__ == target]

        if self.kind == SWORD:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in sprites]:
                self.frames += [frame] * 8
            self.frame_amount = 40
            self.lifetime = 40
            self.destroyed_by_walls = False
            self.color = COLORS["red"]

        elif self.kind == FLAMETHROWER:
            self.frames = [pygame.transform.rotate(image, -self.angle) for image in sprites]
            self.frame_amount = 60
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["orange"]

        elif self.kind == AXE:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in sprites]:
                self.frames += [frame] * 6
            self.frame_amount = 66
            self.lifetime = 66
            self.destroyed_by_walls = False
            self.color = COLORS["green"]

        elif self.kind == STAFF:
            for frame in [pygame.transform.rotate(image, -self.angle) for image in sprites]:
                self.frames += [frame] * 5
            self.frame_amount = 25
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["yellow"]

        elif self.kind == HOOK:
            for frame in [pygame.transform.rotate(pygame.transform.flip(image, False, flip),
                                                  -self.angle)
                          for image in sprites]:
                self.frames += [frame] * 4
            self.frame_amount = 68
            self.lifetime = 68
            self.destroyed_by_walls = False
            self.color = COLORS["blue"]

        elif self.kind == GUN:
            for frame in [pygame.transform.rotate(image, -self.angle) for image in sprites]:
                self.frames += [frame] * 5
            self.frame_amount = 50
            self.lifetime = -1
            self.destroyed_by_walls = True
            self.color = COLORS["purple"]

        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect = self.rect.move(x - self.rect.w / 2, y - self.rect.h / 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.image = self.frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.rect.move(self.speed_x, self.speed_y)

        if self.lifetime != -1:
            self.lifetime -= 1
        for index, (target, is_hit) in enumerate(self.targets):
            if not is_hit:
                if pygame.sprite.collide_mask(self, target.hit_box):
                    self.targets[index][1] = True
                    target.get_damage(self.damage)

        if ((pygame.sprite.spritecollide(self, self.walls, dokill=False,
                                         collided=pygame.sprite.collide_mask) and
             self.destroyed_by_walls) or not self.rect.colliderect(self.screen_rect)
                or self.lifetime == 0):
            self.kill()
            del self

