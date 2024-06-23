import json as _json
import sys as _sys

import pygame as _pyg


def load_image(name):
    path = get_asset_path(name)
    return _pyg.image.load(path)


def get_asset_path(name, type="image"):
    sources = {
        "image": "data/image_paths.json",
        "sound": "data/sound_paths.json",
        "font": "data/font_paths.json",
    }
    source = sources.get(type, "image")
    with open(source) as f:
        paths = _json.load(f)
    return paths[name]


def deep_collision(rect1, rect2, depth_x=20, dept_y=10):
    if not rect1.colliderect(rect2):
        return False

    overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
    overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)
    return overlap_x >= depth_x and overlap_y >= dept_y


def scale_image(image, scale=1.5):
    image = load_image(image)
    size = image.get_size()
    new_size = (int(size[0] * scale), int(size[1] * scale))
    return _pyg.transform.scale(image, new_size)


def handle_main_events(event, status):
    if event.type == _pyg.QUIT:
        _pyg.quit(), _sys.exit()  # exit
    if event.type == _pyg.KEYUP:  # restart
        if event.key == _pyg.K_SPACE:
            if status.gameover:
                return True
