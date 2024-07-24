import math as _math

import pygame as _pyg

import src.utils as _utils


class Actor(_pyg.sprite.Sprite):

    def __init__(
        self, world, status, image, ini_pos, ani_speed=0.1, mask_crop=0, lives=1
    ):
        super().__init__()
        self.world, self.status, self.image = world, status, image
        self.ani_index, self.ani_speed = 0, ani_speed

        self.rect = self.image.get_rect(midbottom=ini_pos)
        self.mask = self.create_mask(mask_crop)

        self.action = None
        self.lives = lives

    def create_mask(self, crop_index: int = 0):
        w, h = self.image.get_size()
        cropped_surface = _pyg.Surface(
            (w - crop_index * 2, h - crop_index * 2), _pyg.SRCALPHA
        )
        cropped_surface.blit(self.image, (-crop_index, -crop_index))
        return _pyg.mask.from_surface(cropped_surface)


class NPC(Actor):
    def __init__(
        self,
        world,
        status,
        ini_pos,
        animations,
        player,
        speed,
        react_to_event,
        scale=1,
        hit_event="hits_player",
        image=None,
        ani_speed=0.1,
        mask_crop=0,
        lives=1,
    ):
        self.scale = scale if scale else 1
        if image is None:
            image = self.select_image(animations[0])

        x = ini_pos[0] if ini_pos[0] else world.screen_max_x
        y = ini_pos[1] if ini_pos[1] else world.ground
        self.ini_pos = (x, y)

        super().__init__(world, status, image, self.ini_pos, ani_speed, mask_crop, lives)

        self.animations = animations
        self.player, self.speed = player, speed
        self.react_to_event = react_to_event
        self.hit_event = hit_event

    def select_image(self, ref=0):
        return _utils.scale_image(ref, self.scale).convert_alpha()

    def move_forward(self):
        self.rect.x -= self.speed
        return True if self.rect.right <= 0 else False

    def animate(self):
        if not self.status.gameover:
            self.ani_index += self.ani_speed
            if self.ani_index > len(self.animations):
                self.ani_index = 0
            selected = self.animations[_math.floor(self.ani_index)]
            self.image = self.select_image(selected)

    def update(self):
        is_out_of_screen = self.move_forward()
        if is_out_of_screen:
            self.react_to_event("leaving", self)
        self.animate()
        self.report_hitting_player()

    def report_hitting_player(self):
        if _pyg.sprite.spritecollide(
            self, self.player, False, _pyg.sprite.collide_mask
        ):
            self.react_to_event(self.hit_event, self)
