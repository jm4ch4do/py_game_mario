import math as _math

import pygame as _pyg

from src import utils as _utils


class Player(_pyg.sprite.Sprite):

    def __init__(self, world, status):
        super().__init__()
        self.world, self.status = world, status
        self.images = {
            "walk1": _utils.load_image("player_walk1").convert_alpha(),
            "walk2": _utils.load_image("player_walk2").convert_alpha(),
            "jump": _utils.load_image("player_jump").convert_alpha(),
            "stand": _utils.load_image("player_stand").convert_alpha(),
            "hit": _utils.load_image("player_hit").convert_alpha(),
        }
        self.jump_force = -6

        self.image = self.images["walk1"]
        self.rect = self.image.get_rect(midbottom=world.player_start)
        self.gravity = 0
        self.gravity_inc = 0.1
        self.ani_index = 0
        self.ani_speed = 0.1

    def handle_input(self):
        keys = _pyg.key.get_pressed()
        if keys[_pyg.K_SPACE]:
            self.jump()

    def jump(self):
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

    def animate(self):
        if self.status.gameover:
            self.image = self.images["hit"]
        elif self.rect.bottom < self.world.ground:
            self.image = self.images["jump"]
        else:
            self.ani_index += self.ani_speed
            if self.ani_index > 2:
                self.ani_index = 0
            self.image = self.images[f"walk{_math.floor(self.ani_index) + 1}"]

    def update(self, screen):
        self.handle_input()
        self.apply_gravity()
        self.animate()
