from .alpha_pyg.PygproxyBringer import PygproxyBringer as _BringerCls

"""
    KataSDK (c) Gaudia Tech Inc. 2018-2021
    
    about the author: www.github.com/wkta
    -------------------
    the SDK's structure
    -------------------
    ext_*
        ~ dep
            ->engine
                ~ dep -
                    ->alpha_pyg
                        ~ dep -
                            ->pygame_emu
    -------------------
"""

version = VERSION = _BringerCls.instance().framework_version


def import_pygame():
    return _BringerCls.instance().pygame()


def import_pygame_gfxdraw():
    return _BringerCls.instance().pygame_gfxdraw()
