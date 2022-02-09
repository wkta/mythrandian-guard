import game_defs
import glvars
from katagames_sdk.engine import BaseGameState, EngineEvTypes, EventReceiver, import_pygame


pygame = import_pygame()


# Nota Bene.
# there will be no model for the collection, as the avatar already contains it!
# (in glvars.the_avatar.artifacts)


BASE_Y = 55


class ShowCollectionView(EventReceiver):
    """
    dummy view,
    displays a gray square(=slot) no matter what,
    +displays a steelblue circle inside this slot if the artifact is owned
    """
    def __init__(self):
        super().__init__()
        self._art_names_labels = list()
        ft = pygame.font.Font(None, 25)
        for ac in game_defs.ArtifactCodes.all_codes:
            self._art_names_labels.append(
                ft.render(game_defs.ArtifactNames[ac][0], True, (87, 11, 128))
            )

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            ev.screen.fill(game_defs.BG_COLOR)

            # - draw labels
            given_y = BASE_Y
            for lbl in self._art_names_labels:
                ev.screen.blit(lbl, (50, given_y-32))
                given_y += 88

            # - draw slots
            given_y = BASE_Y
            circle_offset = [40, 25]
            rad = 21
            for art_code in game_defs.ArtifactCodes.all_codes:
                tmp = max(game_defs.ArtifactNames[art_code].keys())
                for num_piece in range(1, tmp+1):  # draw smth for each artifact element
                    tmpx = 50+(num_piece-1)*125
                    pygame.draw.rect(ev.screen, 'darkgray', (tmpx, given_y, 80, 50))
                    if glvars.the_avatar.has_artifact(art_code, num_piece):
                        pygame.draw.circle(ev.screen, 'steelblue',
                                           (tmpx+circle_offset[0], given_y+circle_offset[1]), rad)
                given_y += 88


class ShowCollectionCtrl(EventReceiver):
    def proc_event(self, ev, source):
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            self.pev(EngineEvTypes.POPSTATE)


class ShowCollectionState(BaseGameState):
    def __init__(self, gs_id, name):
        super().__init__(gs_id, name)
        self.m = self.v = self.c = None

    def enter(self):
        self.v = ShowCollectionView()
        self.v.turn_on()
        self.c = ShowCollectionCtrl()
        self.c.turn_on()

    def release(self):
        self.c.turn_off()
        self.v.turn_off()
        self.c = self.v = None
