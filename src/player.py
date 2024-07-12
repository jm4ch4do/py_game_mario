import math as _math

import pygame as _pyg

from src import utils as _utils


class Actor(_pyg.sprite.Sprite):
    def __init__(self, world, status, image):
        super().__init__()
        self.world, self.status, self.image = world, status, image


class Player(Actor):

    def __init__(self, world, status):
        self.images = {
            "walk1": _utils.load_image("player_walk1").convert_alpha(),
            "walk2": _utils.load_image("player_walk2").convert_alpha(),
            "jump": _utils.load_image("player_jump").convert_alpha(),
            "stand": _utils.load_image("player_stand").convert_alpha(),
            "hit": _utils.load_image("player_hit").convert_alpha(),
            "happy": _utils.load_image("player_happy").convert_alpha(),
            "run1": _utils.load_image("player_run1").convert_alpha(),
            "run2": _utils.load_image("player_run2").convert_alpha(),
        }
        super().__init__(world, status, self.images["walk1"])

        self.rect = self.image.get_rect(midbottom=world.player_start)
        self.mask = self.create_cropped_mask()
        self.jump_force = -6
        self.gravity = 0
        self.gravity_inc = 0.1
        self.ani_index = 0
        self.ani_speed = 0.1
        self.run_faster_speed = 2
        self.run_slower_speed = 2
        self.action = None

    def handle_input(self):
        self.action = None
        keys = _pyg.key.get_pressed()
        if keys[_pyg.K_SPACE] or keys[_pyg.K_UP]:
            self.jump()
        elif keys[_pyg.K_RIGHT]:
            self.run_faster()
            self.action = "running_faster"
        elif keys[_pyg.K_LEFT]:
            self.run_slower()
            self.action = "running_slower"

    def create_cropped_mask(self, crop_index: int = 1):
        w, h = self.image.get_size()
        cropped_surface = _pyg.Surface(
            (w - crop_index * 2, h - crop_index * 2), _pyg.SRCALPHA
        )
        cropped_surface.blit(self.image, (-crop_index, -crop_index))
        return _pyg.mask.from_surface(cropped_surface)

    def jump(self):
        if not self.status.gameover:
            if self.rect.bottom >= self.world.ground:
                self.gravity = self.jump_force

    def run_faster(self):
        if not self.status.gameover:
            if self.rect.bottom >= self.world.ground:
                if self.rect.right < self.world.screen_max_x:
                    self.rect.x += self.run_faster_speed

    def run_slower(self):
        if not self.status.gameover:
            if self.rect.bottom >= self.world.ground:
                if self.rect.left > 0:
                    self.rect.x -= self.run_slower_speed

    def victory_jump(self):
        if self.rect.bottom >= self.world.ground:
            self.gravity = self.jump_force / 3

    def apply_gravity(self):
        if self.status.gameover and not self.status.victory:
            return None
        self.rect.y += self.gravity
        if self.rect.bottom >= self.world.ground:
            self.rect.bottom = self.world.ground
            self.gravity = 0
        else:
            self.gravity += self.gravity_inc

    def animate(self):
        if self.status.victory:
            self.image = self.images["happy"]
            self.victory_jump()
        elif self.status.gameover:
            self.image = self.images["hit"]
        elif self.rect.bottom < self.world.ground:
            self.image = self.images["jump"]
        else:
            self.animate_running()

    def animate_running(self):
        if self.action == "running_faster":
            action, ani_speed = "run", self.ani_speed * 1.5
        elif self.action == "running_slower":
            action, ani_speed = "walk", self.ani_speed / 2
        else:
            action, ani_speed = "walk", self.ani_speed
        self.ani_index += ani_speed
        if self.ani_index >= 2:
            self.ani_index = 0
        self.image = self.images[f"{action}{_math.floor(self.ani_index) + 1}"]

    def update(self, screen):
        self.handle_input()
        self.apply_gravity()
        self.animate()
