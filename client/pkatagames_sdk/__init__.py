from .alpha_pyg.PygproxyBringer import PygproxyBringer as _BringerCls
"""
    IMPORTANT NOTICE:
    files inside this module are not realeased under the MIT License
    
    this module will be removed from the "Mythrandian Guard" at some point,
    as the game development reaches completion.
    
    KataSDK (c) Gaudia Tech Inc. 2018-2021
    about:
    www.github.com/wkta
    www.github.com/gaudiatech
    
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
