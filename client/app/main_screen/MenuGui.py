import glvars
import katagames_sdk.katagames_engine as kengi
from app.main_screen.models import Artifact
from game_defs import GameStates
from game_events import MyEvTypes


pygame = kengi.pygame
EngineEvTypes = kengi.event.EngineEvTypes
CgmEvent = kengi.event.CgmEvent
EventReceiver = kengi.event.EventReceiver


# - effect for buttons that can be clicked
def click_shop():
    ev_manager = kengi.core.get_manager()
    e = CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Shopping)
    ev_manager.post(e)


def click_fight():
    ev_manager = kengi.core.get_manager()
    e = CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)
    ev_manager.post(e)


def click_loot_arti():
    tmp = Artifact.gen_random()
    print(str(tmp))
    glvars.the_avatar.add_artifact(tmp)


def click_collection():
    ev_manager = kengi.core.get_manager()
    e = CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.ShowCollection)
    ev_manager.post(e)


class MenuGui(EventReceiver):
    """
    stores buttons, etc.
    that are not related to a mission
    """
    LABEL_COL = (211, 15, 127)

    def __init__(self, refmod):
        super().__init__()
        self._avatar = refmod

        self._scr_size = kengi.core.get_screen().get_size()

        # button size & locations
        fixed_size = (150, 48)
        bpos = list()
        for index in range(0, 5):
            bpos.append((200 * index, self._scr_size[1] - 50))

        # create buttons
        self._buttons = {
            'shop': kengi.gui.Button(pos=bpos[1], size=fixed_size, label='go to the shop'),
            'fight': kengi.gui.Button(pos=bpos[2], size=fixed_size, label='take a fight'),
            'get_arti': kengi.gui.Button(pos=bpos[3], size=fixed_size, label='(cheat) loot artifact'),
            'collection': kengi.gui.Button(pos=bpos[4], size=fixed_size, label='check collection')
        }
        self._buttons['shop'].callback = click_shop
        self._buttons['fight'].callback = click_fight
        self._buttons['get_arti'].callback = click_loot_arti
        self._buttons['collection'].callback = click_collection

        tmp_img = pygame.image.load('assets/small-coin.png')
        self._wealth_spr = pygame.sprite.Sprite()
        tmp2 = pygame.transform.scale(tmp_img, (60, 60))
        tmp2.set_colorkey((255, 0, 255))
        self._wealth_spr.image = tmp2
        self._wealth_spr.rect = tmp2.get_rect()
        self._wealth_spr.rect.center = (self._scr_size[0] - 80, 80)  # move

        # self._tmp_wealth = 2*10**6+28*1000+721  # placeholder
        self._med_font = pygame.font.Font(None, 34)
        self._small_font = pygame.font.Font(None, 25)
        self._label_wealth = None
        self._pos_wealth_lbl = None
        self.update_labels()

    def update_labels(self, couleur=None):
        if couleur is None:
            couleur = self.LABEL_COL
        pesos_act = self._avatar.gold
        texte = "{:,}".format(pesos_act)

        if pesos_act >= 10 ** 5:
            fonte_adhoc = self._small_font
        else:
            fonte_adhoc = self._med_font

        self._label_wealth = fonte_adhoc.render(texte, False, couleur)
        isize = self._label_wealth.get_size()
        x, y = self._wealth_spr.rect.center
        self._pos_wealth_lbl = (x-(isize[0]//2), y-44)

    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            for bt_obj in self._buttons.values():
                ev.screen.blit(bt_obj.image, bt_obj.rect.topleft)
            ev.screen.blit(self._wealth_spr.image, self._wealth_spr.rect.topleft)

            ev.screen.blit(self._label_wealth, self._pos_wealth_lbl)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for bt_obj in self._buttons.values():
                if bt_obj.rect.collidepoint(ev.pos):
                    if bt_obj.callback:
                        bt_obj.callback()

        elif ev.type == MyEvTypes.AvatarUpdate:
            self.update_labels()
