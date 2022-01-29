import random
import time
import pkatagames_sdk as katasdk
import game_defs
from app.AvatarModel import AvatarModel
from app.AvatarView import AvatarView
from app.BelongingsModel import Artifact
from app.Loot import Loot
from game_defs import GameStates
from game_events import MyEvTypes
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, EventManager, CgmEvent, CogObject
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


def click_gen_element():
    # EventManager.instance().post(
    # CgmEvent(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)
    # )
    tmp = Artifact.gen_random()
    print(str(tmp))


class ChallSelectionModel(CogObject):  # it holds the state of missions
    """
    3 missions at the same time
    """

    def __init__(self):
        super().__init__()
        self._ongoing_missions = {
            1: 0,
            2: 0,
            3: 0
        }
        self._difficulties = {
            1: 1.1,
            2: 1.5,
            3: 2.25
        }
        self._temp_loots = dict()

    def start_mission(self, index):
        print('mission {} starts!'.format(index))
        self._ongoing_missions[index] = 1
        self.pev(MyEvTypes.MissionStarts, t=time.time(), idx=index)

    def flag_mission_done(self, index):
        print('mission {} done!'.format(index))
        self._ongoing_missions[index] = -1

        self._temp_loots[index] = obj_loot = Loot.gen_random(self._difficulties[index])
        self._difficulties[index] *= 1.07

        if obj_loot.is_choice_less():
            if obj_loot.has_gold():
                self.pev(MyEvTypes.NotifyAutoloot, is_gold=True, amount=obj_loot.gold)
            else:
                self.pev(MyEvTypes.NotifyAutoloot, is_gold=False, amount=obj_loot.xp)
            self.claim_reward(index)
        else:
            self.pev(MyEvTypes.MissionEnds, idx=index)

    def is_m_open(self, index):
        return 0 == self._ongoing_missions[index]

    def is_m_locked(self, index):
        return 1 == self._ongoing_missions[index]

    def is_m_over(self, index):
        return -1 == self._ongoing_missions[index]

    def _reset_m_state(self, idx):
        if not self.is_m_over(idx):
            raise Exception
        self._ongoing_missions[idx] = 0  # reset state
        del self._temp_loots[idx]

    def claim_reward(self, index):
        print(self._temp_loots[index])
        self._temp_loots[index].claim()

        self._reset_m_state(index)
        self.pev(MyEvTypes.MissionFree, idx=index)


class ChallSelectionView(EventReceiver):

    def __init__(self, ref_mod):
        super().__init__(self)

        # small red squares to tell the mission is ongoing
        self._squares = dict()

        self._model = ref_mod

        self._bg_color = 'antiquewhite3'  # or smth like (255, 50, 60) if we choose the red, green, blue format
        ft = pygame.font.Font(None, 19)
        # self.img = ft.render('press mouse button to change state', True, (0, 0, 0))
        self.img_pos = (200, 180)

        self._scr_size = kataen.get_screen().get_size()

        # - set all buttons
        fixed_size = (150, 48)
        bpos = list()
        for index in range(0, 5):
            bpos.append((228 * index, self._scr_size[1] - 50))

        cls = self.__class__
        self._buttons = {
            'm1': Button(pos=cls.position_m_square(1), size=fixed_size, label='mission1'),
            'm2': Button(pos=cls.position_m_square(2), size=fixed_size, label='mission2'),
            'm3': Button(pos=cls.position_m_square(3), size=fixed_size, label='mission3'),

            'shop': Button(pos=bpos[1], size=fixed_size, label='go to the shop'),
            'fight': Button(pos=bpos[2], size=fixed_size, label='take a fight'),
            'reward': Button(pos=bpos[3], size=fixed_size, label='gen reward'),
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
        self._buttons['reward'].callback = click_gen_element

    @staticmethod
    def position_m_square(index):
        return 228 * index, 50

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
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
            adj_pos = list(ChallSelectionView.position_m_square(ev.idx))
            adj_pos[1] += 30  # y
            self._squares[ev.idx] = (tmp, adj_pos)

        elif ev.type == pygame.MOUSEBUTTONDOWN:
            for bt_obj in self._buttons.values():
                if bt_obj.rect.collidepoint(ev.pos):
                    if bt_obj.callback:
                        bt_obj.callback()


class ChallSelectionCtrl(EventReceiver):

    MISSION_DELAY = 2.0

    def __init__(self, mod):
        super().__init__()
        self._modele = mod
        self._timers = dict()

    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.LOGICUPDATE:
            if len(self._timers) > 0:
                defunct_set = set()
                for mission_idx, v in self._timers.items():
                    dt = time.time() - v
                    if dt > ChallSelectionCtrl.MISSION_DELAY:
                        defunct_set.add(mission_idx)

                for targ_idx in defunct_set:
                    del self._timers[targ_idx]
                    self._modele.flag_mission_done(targ_idx)

        elif ev.type == MyEvTypes.FightStarts:
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)

        elif ev.type == MyEvTypes.MissionStarts:
            self._timers[ev.idx] = ev.t


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
        self.m = ChallSelectionModel()
        self.v = ChallSelectionView(self.m)
        self.vavatar = AvatarView(self._avatar)

        self.c = ChallSelectionCtrl(self.m)
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
