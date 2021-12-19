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

import pygame

GAME_TITLE = 'Mythrandian Guard'
MAXFPS = 60

gameover = False
scr = pygame.surface.Surface((0, 0))
clock = pygame.time.Clock()


def init_g():
    global scr, clock
    pygame.init()
    scr = pygame.display.set_mode((640, 480))
    pygame.display.set_caption(GAME_TITLE)


def update_g():  # infot=None:
    global scr, gameover, clock
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            gameover = True
    scr.fill('antiquewhite3')
    pygame.display.update()
    clock.tick(MAXFPS)


if __name__ == '__main__':
    init_g()
    while not gameover:
        update_g()
    pygame.quit()
