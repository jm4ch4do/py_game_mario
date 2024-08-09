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

class Frog(Enemy):

    def __init__(self, world, status, player, react_to_event, ini_pos, scale=1):
        super().__init__(
            world=world,
            status=status,
            player=player,
            scale=scale,
            react_to_event=react_to_event,
            animations=["frog_1"],
            speed=2,
            ani_speed=0.05,
            ini_pos=ini_pos,
        )

        self.jump_force = -5
        self.gravity = 0
        self.gravity_inc = 0.1
        self.is_jumping = False
        self.prepare_jump_limit = 40
        self.prepare_jump_counter = 0


    def move_forward(self):
        self.rect.x -= self.speed
        self.jump()
        return True if self.rect.right <= 0 else False
    
    def jump(self):
        if not self.status.gameover:
            
            if not self.is_jumping:
                self.prepare_jump_counter += 1
                if self.prepare_jump_counter < self.prepare_jump_limit/2:
                    self.animations = ["frog_1"]
                elif self.prepare_jump_counter > self.prepare_jump_limit/2:
                    self.animations = ["frog_2"]
            
                    if self.prepare_jump_counter >= self.prepare_jump_limit:
                        self.prepare_jump_counter = 0
                        self.gravity = self.jump_force
                        self.is_jumping = True

            elif self.is_jumping:
                if self.rect.bottom >= self.world.ground:
                    self.is_jumping = False

                if self.gravity < 0:
                    self.animations = ["frog_3"]
                else:
                    self.animations = ["frog_4"]

    def apply_gravity(self):
        if self.status.gameover:
            return None
        self.rect.y += self.gravity
        if self.rect.bottom >= self.world.ground:
            self.rect.bottom = self.world.ground
            self.gravity = 0
        else:
            self.gravity += self.gravity_inc

    def update(self):
        super().update()
        self.apply_gravity()