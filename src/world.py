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

        self.background_components = (
            ("sky", (0, 0)),
            ("sky", (self.screen_max_x, 0)),
            ("surface", (0, self.ground)),
            ("surface", (self.screen_max_x, self.ground)),
        )
        self.moving_background_components = []
        self.moving_background_components_name = ("sky", "surface")
        self.background_speed = 1
        self.background = self.prepare_background()

    def prepare_window(self, title="Raulito Run", icon="window_icon"):
        _pyg.display.set_caption(title=title)
        path = _utils.get_asset_path("window_icon")
        icon = _pyg.image.load(path)
        _pyg.display.set_icon(icon)

    def prepare_font(self, name="default_font"):
        path = _utils.get_asset_path(name, type="font")
        return _pyg.font.Font(path, 50)

    def prepare_background(self):
        background = _pyg.sprite.Group()
        for comp in self.background_components:
            name, pos = comp
            background_item = Background(name, pos)
            background.add(background_item)
            if name in self.moving_background_components_name:
                self.moving_background_components.append(background_item)
        return background

    def move_background(self):
        for background_component in self.moving_background_components:
            background_component.rect.x -= self.background_speed
            if background_component.rect.right < 0:
                background_component.rect.x = self.screen_max_x

    def update(self):
        self.move_background()


class Background(_pyg.sprite.Sprite):

    def __init__(self, image, pos):
        super().__init__()
        self.image = _utils.load_image(image)
        self.rect = self.image.get_rect(topleft=pos)
