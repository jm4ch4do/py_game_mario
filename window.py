import pygame as _pyg
import sys as _sys


# ----- CONSTANTS
GROUND_BOTTOM_Y = 300
SCREEN_X, SCREEN_Y = 800, 400


# ----- INIT, SCREEN
_pyg.init()
screen_size = (SCREEN_X, SCREEN_Y)
screen = _pyg.display.set_mode(screen_size)
clock = _pyg.time.Clock()
_pyg.display.set_caption('RaulitoRun')
icon = _pyg.image.load('img/icon.png')
_pyg.display.set_icon(icon)


# ----- CREATE FONTS
test_font = _pyg.font.Font("img/font/Pixeltype.ttf", 50)


# ----- CREATE SURFACES
sky_surface = _pyg.image.load('img/sky.png').convert()
ground_surface = _pyg.image.load('img/ground.png').convert()

text_surface = test_font.render("Let's play Raulito Run!", False, (64, 64, 64))
score_surface = test_font.render("Score: 123", False, "#c0e8ec")

snail_surface = _pyg.image.load('img/snail/snail1.png').convert_alpha()
player_surface = _pyg.image.load('img/player/player_walk_1.png').convert_alpha()


# ----- POSITIONS FOR FIXED ELEMENTS
sky_pos = (0, 0)
ground_pos = (0, GROUND_BOTTOM_Y)
text_pos = (250, 25)
score_rect = score_surface.get_rect(center=(SCREEN_X/2, SCREEN_Y/5))


# ----- INI POSITIONS FOR MOVING ELEMENTS
snail_x, snail_y = 600, GROUND_BOTTOM_Y
player_x, player_y = 80, GROUND_BOTTOM_Y
snail_rect = snail_surface.get_rect(midbottom = (snail_x, snail_y))
player_rect = player_surface.get_rect(midbottom = (player_x, player_y))


# ----- GAME LOOP START
while True:
    for event in _pyg.event.get():


    # ----- CAPTURE ACTIONS
        # --- Exit Action
        if event.type == _pyg.QUIT:
            _pyg.quit()
            _sys.exit()

        # --- Key Press
        if event.type == _pyg.KEYDOWN:
            if event.key == _pyg.K_SPACE:
                print('JUMP NOW')

        if event.type == _pyg.KEYUP:
            print('KEY UP')


    # -----INSERT FIXED SURFACES
    screen.blit(sky_surface, sky_pos)
    screen.blit(ground_surface, ground_pos)
    screen.blit(text_surface, text_pos)
    screen.blit(score_surface, score_rect)


    # -----INSERT MOVING SURFACES
    screen.blit(snail_surface, snail_rect)
    screen.blit(player_surface, player_rect)


    # -----MOVING ELEMENTS
    snail_rect.x -= 1
    if snail_rect.right <= 0: snail_rect.left = SCREEN_X


    # # -----CAPTURE KEYS
    keys = _pyg.key.get_pressed()
    if keys[_pyg.K_SPACE]:
        print('still holding space')  

    # ----- GAME LOOP END
    _pyg.display.update()
    clock.tick(60)

