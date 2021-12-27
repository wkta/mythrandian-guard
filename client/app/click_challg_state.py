from pkatagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, import_pygame


pygame = import_pygame()


class ClickChallgCtrl(EventReceiver):
    def __init__(self):
        super().__init__()

    # override
    def proc_event(self, ev, source=None):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_RETURN:
            self.pev(EngineEvTypes.POPSTATE)


class ClickChallgView(EventReceiver):
    def __init__(self):
        super().__init__(self)
        self._bg_color = (50, 255, 60)  # red, green, blue format
        ft = pygame.font.Font(None, 19)
        self.img = ft.render('press enter to go back to the prev. state', True, (0, 0, 0))
        self.img_pos = (200, 180)

    # override
    def proc_event(self, ev, source=None):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(self._bg_color)
            ev.screen.blit(self.img, self.img_pos)


class ClickChallgState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        self.v = ClickChallgView()
        self.v.turn_on()
        self.c = ClickChallgCtrl()
        self.c.turn_on()
        print('  ClickChallgState ENTER')

    def release(self):
        self.c.turn_off()
        self.c = None
        self.v.turn_off()
        self.v = None
        print('  ClickChallgState RELEASE')
