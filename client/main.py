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

import pygame

import pkatagames_sdk as katasdk
from AnimatedSprite import AnimatedSprite


kataen = katasdk.engine

GAME_TITLE = 'Mythrandian Guard'
MAXFPS = 60

gameover = False
scr = pygame.surface.Surface((0, 0))
clock = pygame.time.Clock()
spr_group = pygame.sprite.Group()
t_last_update = time.time()
player_spr = None
lizard_spr = None


def init_g():
    global scr, clock, spr_group, player_spr, lizard_spr
    pygame.init()
    scr = pygame.display.set_mode((640, 480))
    pygame.display.set_caption(GAME_TITLE)

    spr = player_spr = AnimatedSprite('assets/knightye_sheet')
    spr.preload()
    spr.rect.topleft = (256, 0)
    spr2 = lizard_spr = AnimatedSprite('assets/lizardgr_sheet')
    spr2.preload()
    spr2.rect.topleft = (0, 0)

    spr_group.add(spr, spr2)


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

    pygame.display.update()
    clock.tick(MAXFPS)


if __name__ == '__main__':
    init_g()
    while not gameover:
        update_g()
    pygame.quit()
