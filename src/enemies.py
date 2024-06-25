import math as _math

import pygame as _pyg

import src.utils as _utils
import src.world as _world


class EnemyManager:
    def __init__(self, world, status, player):
        self.enemies = _pyg.sprite.Group()
        self.world, self.status, self.player = world, status, player

    def spawn_snail(self, scale=1):
        snail = Snail(
            world=self.world,
            status=self.status,
            player=self.player,
            react_to_event=self.react_to_event,
            scale=scale,
        )
        self.enemies.add(snail)

    def react_to_event(self, event, enemy):
        if event == "leaving":
            new_scale = enemy.scale * enemy.scale_inc
            self.enemies.remove(enemy)
            self.spawn_snail(new_scale)
        if event == "hits_player":
            self.status.gameover = True

    def update(self):
        self.enemies.update()

    def draw(self, screen):
        self.enemies.draw(screen)


class Snail(_pyg.sprite.Sprite):
    scale_inc = 1.2

    def __init__(self, world, status, player, react_to_event, scale=1):
        super().__init__()
        self.world, self.status, self.player = world, status, player
        self.react_to_event = react_to_event
        self.scale = scale
        self.animations = ["snail_1", "snail_2"]
        self.speed = 2
        self.got_point_yet = False
        self.ani_index = 0
        self.ani_speed = 0.05

        self.image = self.select_image(self.animations[0])
        self.rect = self.image.get_rect(midbottom=(world.screen_max_x, world.ground))

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

    def select_image(self, ref=0):
        return _utils.scale_image(ref, self.scale).convert_alpha()

    def update(self):
        is_out_of_screen = self.move_forward()
        if is_out_of_screen:
            self.react_to_event("leaving", self)
        self.animate()
        self.report_hitting_player()
        self.score_jumped_by_player()

    def report_hitting_player(self):
        if _utils.deep_collision(self.rect, self.player.sprite.rect):
            self.react_to_event("hits_player", self)

    def score_jumped_by_player(self):
        if self.rect.x < self.player.sprite.rect.x and not self.got_point_yet:
            self.got_point_yet = True
            self.status.score += 1
