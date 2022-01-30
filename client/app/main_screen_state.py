import random
import time

import glvars
import pkatagames_sdk as katasdk
from app.main_screen.AvatarView import AvatarView
from app.main_screen.MissionSetView import MissionSetView
from app.main_screen.models import Avatar
from app.main_screen.models_mission import MissionSetModel
from game_defs import GameStates
from game_events import MyEvTypes
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver


kataen = katasdk.engine
pygame = katasdk.import_pygame()


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


class MainScreenState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None
        self.vavatar = None
        self._avatar = None

    def enter(self):
        if self._avatar:
            pass
        else:
            self._avatar = Avatar('AmumuTester', 0, random.randint(11, 37))  # random gold pieces aka GP
            self._avatar.add_xp(random.randint(872, 13125))

            glvars.the_avatar = self._avatar  # shared with other game states
        self.m = MissionSetModel()
        self.v = MissionSetView(self.m)
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
