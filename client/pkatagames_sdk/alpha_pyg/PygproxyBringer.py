from pkatagames_sdk.alpha_pyg.Singleton import Singleton


_CONST_SDK_VER_STRING = '0.0.7'


@Singleton
class PygproxyBringer:

    def __init__(self):
        self._runs_in_web = '__BRYTHON__' in globals()
        self._cached_pygame = None
        self._cached_gfxdraw = None

    @property
    def framework_version(self):
        return _CONST_SDK_VER_STRING

    @property
    def web_enabled(self):
        return self._runs_in_web

    def pygame(self):
        if self._cached_pygame is None:  # only on 1st call
            if self.web_enabled:
                from .. import pygame_emu as _pygame
            else:
                import pygame as _pygame  # genuine lib
            self._cached_pygame = _pygame

        # exec. this line no matter what
        return self._cached_pygame

    def pygame_gfxdraw(self):
        if self._cached_gfxdraw is None:  # only on 1st call
            if self.web_enabled:
                from ..pygame_emu import gfxdraw as _gfxdraw
            else:
                import pygame.gfxdraw as _gfxdraw
            self._cached_gfxdraw = _gfxdraw

        # exec. this line no matter what
        return self._cached_gfxdraw
