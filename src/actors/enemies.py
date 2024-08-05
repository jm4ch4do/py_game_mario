import math as _math

import pygame as _pyg

import src.actors.actor as _act


class Enemy(_act.NPC):

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
        super().__init__(
            world=world,
            status=status,
            ini_pos=ini_pos,
            animations=animations,
            player=player,
            speed=speed,
            react_to_event=react_to_event,
            scale=scale,
            ani_speed=ani_speed,
        )
        self.got_point_yet = False

    def update(self):
        super().update()
        self.score_jumped_by_player()

    def score_jumped_by_player(self):
        if self.rect.x < self.player.sprite.rect.x and not self.got_point_yet:
            self.got_point_yet = True
            self.status.score += 1


class Snail(Enemy):

    def __init__(self, world, status, player, react_to_event, ini_pos, scale=1):
        super().__init__(
            world=world,
            status=status,
            player=player,
            scale=scale,
            react_to_event=react_to_event,
            animations=["snail_1", "snail_2"],
            speed=2,
            ani_speed=0.05,
            ini_pos=ini_pos,
        )


class Bird(Enemy):

    def __init__(self, world, status, player, react_to_event, ini_pos, scale=1):
        super().__init__(
            world=world,
            status=status,
            player=player,
            scale=scale,
            react_to_event=react_to_event,
            animations=["bird_1", "bird_2"],
            speed=2,
            ani_speed=0.05,
            ini_pos=(world.screen_max_x, 120),
        )
