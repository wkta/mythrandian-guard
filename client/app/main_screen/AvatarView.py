import katagames_sdk
from game_events import MyEvTypes
from katagames_sdk.engine import EngineEvTypes, EventReceiver
import katagames_sdk.engine as kataen


pygame = kataen.pygame


class AvatarView(EventReceiver):
    """
    repr graphique avatar dans l'écran principal du jeu
    """
    def __init__(self, refmod):
        super().__init__()
        self._avatar = refmod
        self._scr_size = kataen.get_screen().get_size()

        self._x_BASEPOS = self._scr_size[0] // 2
        self._y_BASEPOS = 100

        self._labels = self._lblsizes = None
        self.refresh_disp()

    def refresh_disp(self):
        # two temp variables
        ft = pygame.font.Font(None, 19)
        txtcolor = (16, 16, 128)

        self._labels = list()
        self._lblsizes = list()
        alltexts = [
            '{}:'.format(self._avatar.name),
            'level={} (xp: {} / {})'.format(self._avatar.level, self._avatar.curr_xp, self._avatar.xp_next_level),
            'gp={}'.format(self._avatar.gold),
        ]
        alltexts.extend(self._avatar.get_team_desc().split('\n'))
        for txt in alltexts:
            tmp = ft.render(txt, True, txtcolor)
            self._labels.append(tmp)
            self._lblsizes.append(
                tmp.get_size()
            )

    def proc_event(self, ev, source):
        if ev.type == EngineEvTypes.PAINT:
            mx_y = float('-inf')
            for k, lbl in enumerate(self._labels):
                t = self._lblsizes[k]
                ev.screen.blit(lbl, (self._x_BASEPOS - t[0], self._y_BASEPOS+24*k))
                if self._y_BASEPOS+24*k > mx_y:
                    mx_y = self._y_BASEPOS+24*k
            pygame.draw.rect(ev.screen, 'steelblue', ((self._x_BASEPOS-136, self._y_BASEPOS), (150, mx_y+16)), 2)

        elif ev.type == MyEvTypes.AvatarUpdate:
            self.refresh_disp()
