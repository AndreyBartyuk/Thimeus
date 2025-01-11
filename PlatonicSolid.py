from ThimeusFunctions import load_image
import pygame


class PlatonicSolid(pygame.sprite.Sprite):
    def __init__(self, group, x, y, size, num):
        super().__init__(group)
        sprite_sheet_ = load_image(f"{num}_spritesheet.png")
        self.frame_amount = 25
        image_w = sprite_sheet_.get_size()[0] // self.frame_amount
        image_h = sprite_sheet_.get_size()[1]
        self.frames = list()
        for frame in [pygame.transform.scale(sprite_sheet_.subsurface(i * image_w, 0,
                                                                      image_w, image_h),
                                             (size, size)) for i in range(self.frame_amount)]:
            self.frames += [frame] * 5
        self.frame_amount *= 5
        self.current_frame = 0
        self.image = self.frames[0]
        self.rect = self.image.get_rect().move(x - size // 2, y - size // 2)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.current_frame = (self.current_frame + 1) % self.frame_amount
        self.image = self.frames[self.current_frame]
        self.mask = pygame.mask.from_surface(self.image)
