import random

import game_defs
import pkatagames_sdk
from app.AvatarModel import AvatarModel
from game_defs import GameStates
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, EventManager, import_pygame, CgmEvent
from pkatagames_sdk.ext_gui import Button
from app.AvatarView import AvatarView


kataen = pkatagames_sdk.engine
pygame = import_pygame()


# -- to be bound to GUI buttons --
def click_shop():
    EventManager.instance().post(
        CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Shopping)
    )


def click_fight():
    EventManager.instance().post(
        CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)
    )


class ChallSelectionView(EventReceiver):
    def __init__(self):
        super().__init__(self)
        self._bg_color = 'antiquewhite3'  # or smth like (255, 50, 60) if we choose the red, green, blue format
        ft = pygame.font.Font(None, 19)
        # self.img = ft.render('press mouse button to change state', True, (0, 0, 0))
        self.img_pos = (200, 180)

        self._scr_size = kataen.get_screen().get_size()

        self.bt_shop = Button(pos=(228 * 1, self._scr_size[1]-64), size=(150, 48), label='go to the shop')
        self.bt_shop.callback = click_shop
        self.bt_fight = Button(pos=(228 * 2, self._scr_size[1]-64), size=(150, 48), label='take a fight')
        self.bt_fight.callback = click_fight

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)

            for bt_obj in (self.bt_shop, self.bt_fight):
                ev.screen.blit(bt_obj.image, bt_obj.rect.topleft)
            # impression txt
            # ev.screen.blit(self.img, self.img_pos)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for bt_obj in (self.bt_shop, self.bt_fight):
                if bt_obj.rect.collidepoint(ev.pos):
                    bt_obj.callback()


class ChallSelectionCtrl(EventReceiver):
    def __init__(self):
        super().__init__()

    def proc_event(self, ev, source=None):
        pass
        # if ev.type == pygame.MOUSEBUTTONUP:
        #     self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)


class ChallSelectionState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None
        self.vavatar = None
        self._avatar = None

    def enter(self):
        if self._avatar:
            pass
        else:
            self._avatar = AvatarModel('AmumuTester', 0, random.randint(11, 37))  # random gold pieces aka GP
            self._avatar.add_xp(random.randint(872, 13125))

            game_defs.the_avatar = self._avatar  # shared with other game states

        self.v = ChallSelectionView()
        self.vavatar = AvatarView(self._avatar)

        self.c = ChallSelectionCtrl()
        print(' MainMenuState ENTER')
        self.v.turn_on()
        self.vavatar.turn_on()
        self.c.turn_on()

    def release(self):
        print(' MainMenuState RELEASE')
        self.c.turn_off()
        self.v.turn_off()
        self.vavatar.turn_off()
        self.v = self.c = None

    def pause(self):
        print(' MainMenuState PAUSE')
        self.c.turn_off()
        self.vavatar.turn_off()
        self.v.turn_off()

    def resume(self):
        print(' MainMenuState RESUME')
        self.v.turn_on()
        self.vavatar.turn_on()
        self.c.turn_on()
