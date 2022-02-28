import game_defs
import glvars
import katagames_sdk.katagames_engine as kengi
from app.main_screen.models import Artifact
from game_defs import GameStates
from game_events import MyEvTypes


pygame = kengi.pygame
EngineEvTypes = kengi.event.EngineEvTypes
CgmEvent = kengi.event.CgmEvent
EventReceiver = kengi.event.EventReceiver


class MissionSetView(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__(self)

        # small red squares to tell the mission is ongoing
        self._squares = dict()
        self._model = ref_mod
        self.img_pos = (200, 180)

        self._scr_size = kengi.core.get_screen().get_size()

        # - create mission buttons
        fixed_size = (150, 48)
        cls = self.__class__
        self._buttons = {
            'm1': kengi.gui.Button(pos=cls.position_m_square(1), size=fixed_size, label='mission1'),
            'm2': kengi.gui.Button(pos=cls.position_m_square(2), size=fixed_size, label='mission2'),
            'm3': kengi.gui.Button(pos=cls.position_m_square(3), size=fixed_size, label='mission3')
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

    @staticmethod
    def position_m_square(index):
        return 200 * index, 50

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
