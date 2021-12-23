""""
** Mythrandian Guard **
a game of Heroes and Lackeys
un jeu de Héros et de Laquais

MIT License

project started by: Gaudia Tech Inc.
+ authored by various users see the CONTRIBUTORS file

started in year 2021

contact@kata.games
"""
import time
import pkatagames_sdk as katasdk
import pkatagames_sdk.engine as kataen
from AnimatedSprite import AnimatedSprite
from pkatagames_sdk.ext_gui.Button import ButtonPanel, Button

# the OLD fashion
# pygame = kataen.import_pygame()

# the NEW way
pygame = katasdk.import_pygame()

GAME_TITLE = 'Mythrandian Guard'
MAXFPS = 60

gameover = False
scr = pygame.surface.Surface((0, 0))
clock = pygame.time.Clock()
spr_group = pygame.sprite.Group()
buttons = pygame.sprite.Group()
t_last_update = time.time()
player_spr = None
lizard_spr = None
panel = None


def init_g():
    global scr, clock, spr_group, player_spr, lizard_spr, panel

    # pygame.init()
    # scr = pygame.display.set_mode((640, 480))
    kataen.init(kataen.HD_MODE)
    scr = kataen.get_screen()

    pygame.display.set_caption(GAME_TITLE)

    spr = player_spr = AnimatedSprite('assets/knightye_sheet')
    spr.preload()
    spr.rect.topleft = (256, 0)
    spr2 = lizard_spr = AnimatedSprite('assets/lizardgr_sheet')
    spr2.preload()
    spr2.rect.topleft = (0, 0)

    spr_group.add(spr, spr2)

    tmp_li = [Button(pos=(100, 256), size=(100, 48), label='mon_bouton')]
    panel = ButtonPanel(tmp_li)
    print('on allume')
    panel.turn_on()  # works only if kataen is init

    buttons.add(
        tmp_li[0]
    )


def update_g():  # infot=None:
    global scr, gameover, clock, spr_group, player_spr, t_last_update
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameover = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                player_spr.play('attack')
                lizard_spr.play('attack')
            elif ev.key == pygame.K_RETURN:
                player_spr.play('defend')
                lizard_spr.play('defend')
            elif ev.key == pygame.K_BACKSPACE:
                player_spr.play('getsHit')
                lizard_spr.play('getsHit')

    tmp = time.time()
    dt = (tmp - t_last_update)
    t_last_update = tmp
    spr_group.update(dt)

    # draw
    scr.fill('antiquewhite3')
    spr_group.draw(scr)
    buttons.draw(scr)

    # pygame.display.update()
    kataen.display_update()
    clock.tick(MAXFPS)


if __name__ == '__main__':
    init_g()
    while not gameover:
        update_g()
    kataen.cleanup()
    # pygame.quit()
