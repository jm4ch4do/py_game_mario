import pygame as _pyg

from src import utils as _utils


class World:

    def __init__(
        self,
        ground=300,
        player_start_x=80,
        enemy_start_x=600,
        screen_max_x=800,
        screen_max_y=400,
        background=("sky", "surface"),
    ):
        self.ground = ground
        self.screen_max_x = screen_max_x
        self.screen_max_y = screen_max_y
        self.font = self.prepare_font()

        self.player_start = (player_start_x, self.ground)
        self.enemy_start = (enemy_start_x, self.ground)
        self.sky_pos = (0, 0)
        self.surface_pos = (0, ground)

        self.prepare_window()
        self.background = self.prepare_background(background)

    def prepare_window(self, title="Raulito Run", icon="window_icon"):
        _pyg.display.set_caption(title=title)
        path = _utils.get_asset_path("window_icon")
        icon = _pyg.image.load(path)
        _pyg.display.set_icon(icon)

    def prepare_font(self, name="default_font"):
        path = _utils.get_asset_path(name, type="font")
        return _pyg.font.Font(path, 50)

    def prepare_background(self, components):
        backgrounds = [
            Background(comp, getattr(self, f"{comp}_pos")) for comp in components
        ]
        background_group = _pyg.sprite.Group()
        for background in backgrounds:
            background_group.add(background)
        return background_group


class Background(_pyg.sprite.Sprite):

    def __init__(self, image, pos):
        super().__init__()
        self.image = _utils.load_image(image)
        self.rect = self.image.get_rect(topleft=pos)
