from katagames_sdk.capsule.struct.Singleton import Singleton


@Singleton
class ProxyFactory:

    def __init__(self):
        self._runs_in_web = '__BRYTHON__' in globals()
        self._cached_gfxdraw = None
        self._cached_pygame = None

    def uses_web_ctx(self):
        return self._runs_in_web

    def build(self):
        if self._cached_pygame is None:
            if self._runs_in_web:  # runs in web ctx
                import katagames_sdk.pygame_emu as _pygame
            else:
                import pygame as _pygame  # genuine pygame
            self._cached_pygame = _pygame
        return self._cached_pygame

    def build_gfxdraw(self):
        if self._cached_gfxdraw is None:
            if self._runs_in_web:
                import katagames_sdk.pygame_emu.gfxdraw as _gfxdraw
            else:
                import pygame.gfxdraw as _gfxdraw
            self._cached_gfxdraw = _gfxdraw
        return self._cached_gfxdraw
