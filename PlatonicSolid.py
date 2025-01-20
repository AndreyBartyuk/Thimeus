from ThimeusFunctions import load_image
import pygame


class PlatonicSolid(pygame.sprite.Sprite):
    def __init__(self, group, x, y, size, num):
        super().__init__(group)
        sprite_sheet_ = load_image(f"{num}_spritesheet.png")
        self.frame_amount = 25
        if num == 0:
            self.frame_amount = 50
        image_w = 500
        image_h = 500
        self.frames = list()
        mult = 4 # 5
        if num == 0:
            for frame in [pygame.transform.scale(sprite_sheet_.subsurface(i * image_w, j * image_h,
                                                                          image_w, image_h),
                                                 (size, size)) for j in range(5) for i in range(10)]:
                self.frames += [frame] * mult
        else:
            for frame in [pygame.transform.scale(sprite_sheet_.subsurface(i * image_w, 0,
                                                                          image_w, image_h),
                                                 (size, size)) for i in range(self.frame_amount)]:
                self.frames += [frame] * mult
        self.frame_amount *= mult
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(x, y)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.image = self.frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)

    def interact(self):
        pass
