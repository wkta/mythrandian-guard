from game_defs import GameStates
from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, import_pygame


pygame = import_pygame()


class ChallSelectionCtrl(EventReceiver):
    def __init__(self):
        super().__init__()

    # override
    def proc_event(self, ev, source=None):
        if ev.type == pygame.MOUSEBUTTONUP:
            self.pev(EngineEvTypes.PUSHSTATE, state_ident=GameStates.Fighting)


class ChallSelectionView(EventReceiver):
    def __init__(self):
        super().__init__(self)
        self._bg_color = (255, 50, 60)  # red, green, blue format
        ft = pygame.font.Font(None, 19)
        self.img = ft.render('press mouse button to change state', True, (0, 0, 0))
        self.img_pos = (200, 180)

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
            ev.screen.blit(self.img, self.img_pos)


class ChallSelectionState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        self.v = ChallSelectionView()
        self.c = ChallSelectionCtrl()
        print(' MainMenuState ENTER')
        self.v.turn_on()
        self.c.turn_on()

    def release(self):
        print(' MainMenuState RELEASE')
        self.c.turn_off()
        self.v.turn_off()
        self.v = self.c = None

    def pause(self):
        print(' MainMenuState PAUSE')
        self.c.turn_off()
        self.v.turn_off()

    def resume(self):
        print(' MainMenuState RESUME')
        self.v.turn_on()
        self.c.turn_on()
