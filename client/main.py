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
spr = AnimatedSprite('assets/knightye_sheet')
t_last_update = time.time()


def init_g():
    global scr, clock, spr
    pygame.init()
    scr = pygame.display.set_mode((640, 480))
    pygame.display.set_caption(GAME_TITLE)
    spr.load_data()


def update_g():  # infot=None:
    global scr, gameover, clock, spr, t_last_update
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameover = True
        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                spr.play('attack')

    tmp = time.time()
    dt = (tmp - t_last_update)
    t_last_update = tmp
    spr.update_anim(dt)

    # draw
    scr.fill('antiquewhite3')
    scr.blit(spr.image, (0, 0))
    pygame.display.update()
    clock.tick(MAXFPS)


if __name__ == '__main__':
    init_g()
    while not gameover:
        update_g()
    pygame.quit()
