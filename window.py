import pygame as _pyg
import sys as _sys

# ----- INIT, SCREEN
_pyg.init()
screen_size = (800, 400)
screen = _pyg.display.set_mode(screen_size)
clock = _pyg.time.Clock()
_pyg.display.set_caption('RaulitoRun')
icon = _pyg.image.load('img/icon.png')
_pyg.display.set_icon(icon)


# ----- CREATE FONTS
test_font = _pyg.font.Font("img/font/Pixeltype.ttf", 50)
text_surface = test_font.render("Let's play Raulito Run!", False, "Black")


# ----- CREATE SURFACES
sky_surface = _pyg.image.load('img/sky.png')
ground_surface = _pyg.image.load('img/ground.png')
snail_surface = _pyg.image.load('img/snail/snail1.png')
#test_surface = _pyg.Surface((100, 200))
#test_surface.fill('Red')


# ----- POSITIONS FOR FIXED ELEMENTS
sky_pos = (0, 0)
ground_pos = (0, 300)
text_pos = (250, 50)


# ----- POSITIONS INI FOR MOVING ELEMENTS
snail_x, snail_y = 600, 265


# ----- GAME LOOP START
while True:
    for event in _pyg.event.get():


    # ----- ACTIONS
        # --- Exit Action
        if event.type == _pyg.QUIT:
            _pyg.quit()
            _sys.exit()


    # -----INSERT FIXED SURFACES
    screen.blit(sky_surface, sky_pos)
    screen.blit(ground_surface, ground_pos)
    screen.blit(text_surface, text_pos)


    # -----INSERT MOVING SURFACES
    screen.blit(snail_surface, (snail_x, snail_y))


    # -----MOVING ELEMENTS
    snail_x -= 0.5


    # ----- GAME LOOP END
    _pyg.display.update()
    clock.tick(60)

