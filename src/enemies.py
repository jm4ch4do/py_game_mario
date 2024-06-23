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
        self.image_base = _utils.scale_image("snail_1", scale).convert_alpha()
        self.speed = 2
        self.got_point_yet = False

        self.image = self.image_base
        self.rect = self.image.get_rect(midbottom=(world.screen_max_x, world.ground))

    def move_forward(self):
        self.rect.x -= self.speed
        return True if self.rect.right <= 0 else False

    def update(self):
        is_out_of_screen = self.move_forward()
        if is_out_of_screen:
            self.react_to_event("leaving", self)
        self.report_hitting_player()
        self.score_jumped_by_player()

    def report_hitting_player(self):
        if _utils.deep_collision(self.rect, self.player.sprite.rect):
            self.react_to_event("hits_player", self)

    def score_jumped_by_player(self):
        if self.rect.x < self.player.sprite.rect.x and not self.got_point_yet:
            self.got_point_yet = True
            self.status.score += 1
