import pygame as _pyg

from src import utils as _utils


class Status:

    def __init__(self):
        self.gameover = False
        self.victory = False
        self.score = 0
        self.start_time = _pyg.time.get_ticks()


class Score(_pyg.sprite.Sprite):
    def __init__(self, world, status, color="#404040"):
        super().__init__()
        self.world, self.status, self.color = world, status, color
        self.pos = (world.screen_max_x / 2, world.screen_max_y / 4)
        self.message, self.image, self.rect = None, None, None
        self.update_message()

    def update_message(self):
        self.message = f"Score: {self.status.score}"
        self.image = self.world.font.render(self.message, False, self.color)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self):
        self.update_message()


class MainText(_pyg.sprite.Sprite):
    msg = {
        "intro": "Let's play Raulito Run!",
        "end": "Game over! Press Space to retry",
    }

    def __init__(self, world, status, color="#404040"):
        super().__init__()
        self.world, self.status, self.color = world, status, color
        self.pos = (world.screen_max_x / 2, world.screen_max_y / 8)
        self.message, self.image, self.rect = None, None, None
        self.update()

    def update_message(self):
        return self.msg["end"] if self.status.gameover else self.msg["intro"]

    def update(self):
        self.message = self.update_message()
        self.image = self.world.font.render(self.message, False, self.color)
        self.rect = self.image.get_rect(center=self.pos)
