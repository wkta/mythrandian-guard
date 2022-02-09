import time

import game_defs
import katagames_sdk.engine as kataen
from katagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, import_pygame
from katagames_sdk.ext_gui.Button import ButtonPanel, Button


pygame = import_pygame()


class FightingState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        print('entree - MenuAventuresState')
        self.v = VueHeros()
        self.c = CustomListener()
        self.v.turn_on()
        self.c.turn_on()

    def release(self):
        print('sortie - MenuAventuresState')
        self.v.turn_off()
        self.c.turn_off()


player_spr = None
lizard_spr = None
panel = None


class VueHeros(EventReceiver):

    def _init_logic(self):
        global player_spr, lizard_spr, panel
        spr = player_spr = kataen.AnimatedSprite('assets/knightye_sheet')
        spr.preload()
        spr.rect.topleft = (256, 0)

        spr2 = lizard_spr = kataen.AnimatedSprite('assets/lizardgr_sheet')
        spr2.preload()
        spr2.rect.topleft = (0, 0)

        self.spr_group.add(spr, spr2)

        tmp_li = list()
        actions = ['attack(space)', 'defend(return)', 'getsHit(backspc)']
        for k, action in enumerate(actions):
            tmp_li.append(
                Button(pos=(100 + 228 * k, 256), size=(150, 48), label=action)
            )

        panel = ButtonPanel(
            tmp_li, {
                tmp_li[0].ident: anim_attack,
                tmp_li[1].ident: anim_defend,
                tmp_li[2].ident: anim_hit,
            }
        )
        print('on allume')
        panel.turn_on()  # works only if kataen is init

        self.buttons.add(
            tmp_li[0], tmp_li[1], tmp_li[2]
        )

    def __init__(self):
        super().__init__()
        self.t_last_update = time.time()

        self.spr_group = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self._init_logic()

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            tmp = time.time()
            dt = (tmp - self.t_last_update)
            self.t_last_update = tmp
            self.spr_group.update(dt)

        elif ev.type == EngineEvTypes.PAINT:
            scr = ev.screen
            scr.fill(game_defs.BG_COLOR)
            self.spr_group.draw(scr)
            self.buttons.draw(scr)


# -- to be bound to GUI buttons --
def anim_attack():
    global player_spr, lizard_spr
    player_spr.play('attack')
    lizard_spr.play('attack')


def anim_defend():
    global player_spr, lizard_spr
    player_spr.play('defend')
    lizard_spr.play('defend')


def anim_hit():
    global player_spr, lizard_spr
    player_spr.play('getsHit')
    lizard_spr.play('getsHit')


class CustomListener(kataen.EventReceiver):
    def proc_event(self, ev, source):
        global player_spr, lizard_spr

        if ev.type == kataen.EngineEvTypes.BTCLICK:
            print(ev)

        elif ev.type == pygame.QUIT:
            self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)

        elif ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_SPACE:
                anim_attack()
            elif ev.key == pygame.K_RETURN:
                anim_defend()
            elif ev.key == pygame.K_BACKSPACE:
                anim_hit()
