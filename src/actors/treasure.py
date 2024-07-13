import pygame as _pyg

import src.actors.actor as _act
import src.utils as _utils


class Treasure(_act.NPC):

    def __init__(self, world, status, player, react_to_event, scale=1):
        super().__init__(
            world=world,
            status=status,
            ini_pos=(world.screen_max_x, world.ground),
            animations=["treasure", "treasure_opened"],
            player=player,
            speed=1,
            react_to_event=react_to_event,
            scale=scale,
        )
        self.is_open = False

    def animate(self):
        index = 1 if self.is_open else 0
        self.image = self.select_image(self.animations[index])

    def report_hitting_player(self):
        if _utils.deep_collision(self.rect, self.player.sprite.rect):
            self.is_open = True
            self.animate()
            self.react_to_event("found", self)
