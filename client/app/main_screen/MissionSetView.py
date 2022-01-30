import game_defs
import glvars
import pkatagames_sdk as katasdk
from app.main_screen.models import Artifact
from game_defs import GameStates
from game_events import MyEvTypes
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, EventManager, CgmEvent
from pkatagames_sdk.ext_gui import Button


kataen = katasdk.engine
pygame = katasdk.import_pygame()


# -- to be bound to GUI buttons --
def click_shop():
    EventManager.instance().post(
        CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Shopping)
    )


def click_fight():
    EventManager.instance().post(
        CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)
    )


def click_loot_art():
    tmp = Artifact.gen_random()
    print(str(tmp))
    glvars.the_avatar.add_artifact(tmp)


class MissionSetView(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__(self)

        # small red squares to tell the mission is ongoing
        self._squares = dict()
        self._model = ref_mod

        ft = pygame.font.Font(None, 19)
        # self.img = ft.render('press mouse button to change state', True, (0, 0, 0))
        self.img_pos = (200, 180)

        self._scr_size = kataen.get_screen().get_size()

        # - set all buttons
        fixed_size = (150, 48)
        bpos = list()
        for index in range(0, 5):
            bpos.append((200 * index, self._scr_size[1] - 50))

        cls = self.__class__
        self._buttons = {
            'm1': Button(pos=cls.position_m_square(1), size=fixed_size, label='mission1'),
            'm2': Button(pos=cls.position_m_square(2), size=fixed_size, label='mission2'),
            'm3': Button(pos=cls.position_m_square(3), size=fixed_size, label='mission3'),

            'shop': Button(pos=bpos[1], size=fixed_size, label='go to the shop'),
            'fight': Button(pos=bpos[2], size=fixed_size, label='take a fight'),
            'get_arti': Button(pos=bpos[3], size=fixed_size, label='(cheat) loot artifact'),
            'collection': Button(pos=bpos[4], size=fixed_size, label='check collection')
        }

        # dupe 3x same kind of callback func.
        def effetm1():
            if not self._model.is_m_locked(1):
                if self._model.is_m_over(1):
                    self._model.claim_reward(1)
                else:  # therefore its open
                    self._model.start_mission(1)

        def effetm2():
            if not self._model.is_m_locked(2):
                if self._model.is_m_over(2):
                    self._model.claim_reward(2)
                else:  # therefore its open
                    self._model.start_mission(2)

        def effetm3():
            if not self._model.is_m_locked(3):
                if self._model.is_m_over(3):
                    self._model.claim_reward(3)
                else:  # therefore its open
                    self._model.start_mission(3)

        self._buttons['m1'].callback = effetm1
        self._buttons['m2'].callback = effetm2
        self._buttons['m3'].callback = effetm3

        self._buttons['shop'].callback = click_shop
        self._buttons['fight'].callback = click_fight
        self._buttons['get_arti'].callback = click_loot_art

        def effet_collection():
            EventManager.instance().post(
                CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.ShowCollection)
            )
        self._buttons['collection'].callback = effet_collection

    @staticmethod
    def position_m_square(index):
        return 200 * index, 50

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(game_defs.BG_COLOR)
            for bt_obj in self._buttons.values():
                ev.screen.blit(bt_obj.image, bt_obj.rect.topleft)
            for k in range(1, 4):
                if k in self._squares:
                    surf, pos = self._squares[k]
                    ev.screen.blit(surf, pos)

        elif ev.type == MyEvTypes.MissionEnds:
            self._squares[ev.idx][0].fill((0, 255, 0))

        elif ev.type == MyEvTypes.MissionFree:
            del self._squares[ev.idx]

        elif ev.type == MyEvTypes.MissionStarts:
            # self._model.is_m_locked(ev.idx):
            tmp = pygame.Surface((80, 80))
            tmp.fill((255, 0, 0))
            adj_pos = list(MissionSetView.position_m_square(ev.idx))
            adj_pos[1] += 30  # y
            self._squares[ev.idx] = (tmp, adj_pos)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for bt_obj in self._buttons.values():
                if bt_obj.rect.collidepoint(ev.pos):
                    if bt_obj.callback:
                        bt_obj.callback()
