import pygame as _pyg

from src import actors as _act
from src import player as _pla
from src import status as _st
from src import utils as _utils
from src import world as _world


# ----------------------------- HELPERS -----------------------------
def prepare_level_start():
    status = _st.Status()
    score = _pyg.sprite.Group()
    score.add(_st.MainText(world=world, status=status))
    score.add(_st.Score(world=world, status=status))

    player = _pyg.sprite.GroupSingle()
    player.add(_pla.Player(world=world, status=status))
    enemy_manager = _act.Spawner(world=world, status=status, player=player)

    return status, score, player, enemy_manager


# ------------------------------ SETUP ------------------------------
_pyg.init()
clock = _pyg.time.Clock()
world = _world.World()
screen = _pyg.display.set_mode((world.screen_max_x, world.screen_max_y))
status, score, player, enemy_manager = prepare_level_start()


# ---------------------------- GAME LOOP ----------------------------
while True:
    for event in _pyg.event.get():
        restart_needed = _utils.handle_main_events(event, status)
        if restart_needed:
            status, score, player, enemy_manager = prepare_level_start()

    if not status.gameover:
        world.update(), score.update()
    world.background.draw(screen), score.draw(screen)

    if not status.gameover:
        enemy_manager.update()
    enemy_manager.draw(screen)

    player.update(screen), player.draw(screen)

    _pyg.display.update()
    clock.tick(60)
