import pygame as _pyg

from src import utils as _utils


class Player(_pyg.sprite.Sprite):

    def __init__(self, world, status):
        super().__init__()
        self.world, self.status = world, status
        self.image_base = _utils.load_image("player_1").convert_alpha()
        self.image_hit = _utils.load_image("player_hit").convert_alpha()
        self.jump_force = -6

        self.image = self.image_base
        self.rect = self.image.get_rect(midbottom=world.player_start)
        self.gravity = 0
        self.gravity_inc = 0.1

    def player_input(self):

        keys = _pyg.key.get_pressed()
        if keys[_pyg.K_SPACE]:

            if not self.status.gameover:
                if self.rect.bottom >= self.world.ground:
                    self.gravity = self.jump_force

    def apply_gravity(self):
        self.rect.y += self.gravity
        if self.rect.bottom >= self.world.ground:
            self.rect.bottom = self.world.ground
            self.gravity = 0
        else:
            self.gravity += self.gravity_inc

    def update(self):
        self.player_input()
        self.apply_gravity()
