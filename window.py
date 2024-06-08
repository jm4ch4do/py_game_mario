import pygame as _pyg
import sys as _sys


# ----- HELPER FUNCTIONS
def deep_collision(rect1, rect2, depth_x=20, dept_y=10):
    if not rect1.colliderect(rect2):
        return False
    
    overlap_x = min(rect1.right, rect2.right) - max(rect1.left, rect2.left)
    overlap_y = min(rect1.bottom, rect2.bottom) - max(rect1.top, rect2.top)
    return overlap_x >= depth_x and overlap_y >= dept_y


def scale_image(image, scale=1.5):
    image = _pyg.image.load(path_img_snail).convert_alpha()
    size = image.get_size()
    new_size = (int(size[0] * scale), int(size[1] * scale))
    return _pyg.transform.scale(image, new_size)
    


# ----- CONSTANTS
GROUND_BOTTOM_Y = 300
SCREEN_X, SCREEN_Y = 800, 400
SKY_POS = (0, 0)
GROUND_POS = (0, GROUND_BOTTOM_Y)

path_img_snail = 'img/snail/snail1.png'


# ----- INIT, SCREEN
_pyg.init()
screen_size = (SCREEN_X, SCREEN_Y)
screen = _pyg.display.set_mode(screen_size)
clock = _pyg.time.Clock()
_pyg.display.set_caption('RaulitoRun')
icon = _pyg.image.load('img/icon.png')
_pyg.display.set_icon(icon)
test_font = _pyg.font.Font("img/font/Pixeltype.ttf", 50)


# ----- STATUS
game_active = True
score = 0
snail_scale = 1
snail_scale_inc = 0.1
got_point_yet = False


# ----- CREATE SURFACES
sky_surface = _pyg.image.load('img/sky.png').convert()
ground_surface = _pyg.image.load('img/ground.png').convert()

text_start_surface = test_font.render("Let's play Raulito Run!", False, (64, 64, 64))
text_end_surface = test_font.render("Game over! Press Space to retry", False, (64, 64, 64))

score_surface = test_font.render(f"Score: {score}", False, "#404040")

snail_surface = _pyg.image.load(path_img_snail).convert_alpha()
player_surface = _pyg.image.load('img/player/player_walk_1.png').convert_alpha()
player_hit_surface = _pyg.image.load('img/player/player_walk_1_hit.png').convert_alpha()


# ----- POSITIONS FOR FIXED ELEMENTS
text_start_rect = text_start_surface.get_rect(center=(SCREEN_X/2, SCREEN_Y/8))
text_end_rect = text_end_surface.get_rect(center=(SCREEN_X/2, SCREEN_Y/8))
score_rect = score_surface.get_rect(center=(SCREEN_X/2, SCREEN_Y/4))


# ----- INI POSITIONS FOR VARIABLE ELEMENTS
snail_x, snail_y = 600, GROUND_BOTTOM_Y
player_x, player_y = 80, GROUND_BOTTOM_Y
snail_rect = snail_surface.get_rect(midbottom = (snail_x, snail_y))
snail_speed = 2

player_rect = player_surface.get_rect(midbottom = (player_x, player_y))
player_gravity = 0
gravity_increase = 0.1


# ----- GAME LOOP START
while True:

    for event in _pyg.event.get():


    # ----- CAPTURE ACTIONS
        # --- Exit Action
        if event.type == _pyg.QUIT:
            _pyg.quit()
            _sys.exit()

        # --- Keyboard Events
        if event.type == _pyg.KEYDOWN :
            # - Jump and Restart with space
            if event.key == _pyg.K_SPACE:
                if game_active:
                    if player_rect.bottom >= GROUND_BOTTOM_Y: player_gravity = -6
                elif not game_active:
                    score, snail_scale = 0, 1
                    game_active = True
                    snail_rect.x = snail_x
                    player_gravity = -1
                    snail_surface = _pyg.image.load(path_img_snail).convert_alpha()
                    snail_rect = snail_surface.get_rect(midbottom = (snail_x, snail_y))
                    screen.blit(snail_surface, snail_rect)
                    score_surface = test_font.render(f"Score: {score}", False, "#404040")
                    screen.blit(score_surface, score_rect)
                    break


        # --- Mouse Events
        if event.type == _pyg.MOUSEBUTTONDOWN and event.button == 1:
            # - Jump with clic on player
            if player_rect.collidepoint(event.pos):
                if player_rect.bottom >= GROUND_BOTTOM_Y: player_gravity = -6
        
    if game_active:
        # -----INSERT FIXED SURFACES
        screen.blit(sky_surface, SKY_POS)
        screen.blit(ground_surface, GROUND_POS)
        screen.blit(text_start_surface, text_start_rect)
        screen.blit(score_surface, score_rect)


        # -----INSERT MOVING SURFACES
        screen.blit(snail_surface, snail_rect)
        screen.blit(player_surface, player_rect)


        # -----CONFIG MOVING ENEMIES
        # snail moving
        snail_rect.x -= snail_speed

        # snail restarts
        if snail_rect.right <= 0:
            snail_scale += snail_scale_inc
            snail_surface = scale_image(path_img_snail, snail_scale)
            snail_rect = snail_surface.get_rect(midbottom = (snail_x, snail_y))
            snail_rect.left = SCREEN_X
            got_point_yet = False
            
        

        # -----CONFIG PLAYER RESPONSE
        # player gravity effect
        player_rect.y += player_gravity
        if player_rect.bottom >= GROUND_BOTTOM_Y: 
            player_rect.bottom = GROUND_BOTTOM_Y
            player_gravity = 0
        else:
            player_gravity += gravity_increase 

        # player hits snail
        #if snail_rect.colliderect(player_rect): game_active = False
        p, s = player_rect.centerx, snail_rect.centerx
        if deep_collision(snail_rect, player_rect): game_active = False

        # player jumps over snail
        elif abs(player_rect.centerx - snail_rect.centerx) < 5 and not got_point_yet:
            got_point_yet
            score += 1
            got_point_yet = True
            score_surface = test_font.render(f"Score: {score}", False, "#404040")
            

    elif not game_active:
        screen.blit(sky_surface, SKY_POS)
        screen.blit(ground_surface, GROUND_POS)
        screen.blit(player_hit_surface, player_rect)
        screen.blit(text_end_surface, text_end_rect)
        score_surface = test_font.render(f"Score: {score}", False, "#404040")
        screen.blit(snail_surface, snail_rect)
        screen.blit(score_surface, score_rect)
        

    # ----- GAME LOOP END
    _pyg.display.update()
    clock.tick(60)
