"""
interface to the Kata.games game Engine
 alias "kataen"

GAUDIA TECH INC.
 (c) 2018-2021

Author:
 Thomas Iwaszko
"""
import katagames_sdk.en_parts.conf_eng as cgmconf
import katagames_sdk.en_parts.events as kevent
import katagames_sdk.en_parts.legacy as eng_
import katagames_sdk.en_parts.defs as _defs

# import katagames_sdk.events as eventmodule
# from katagames_sdk.capsule.engine_ground.defs import EngineEvTypes
# from katagames_sdk.capsule.engine_ground.defs import enum_for_custom_event_types
# from katagames_sdk.capsule.engine_ground.legacy import retrieve_game_ctrl, tag_multistate, get_manager
# from katagames_sdk.capsule.event import EventReceiver, CgmEvent, CogObject
# ------ junk imports
# from katagames_sdk.capsule.engine_ground.BaseGameState import BaseGameState
# from collections import deque as deque_obj
# import katagames_sdk.capsule.gui as gui
# from katagames_sdk.capsule.bioslike.KataFrameV import BIOS_BG_COL_DESC, BIOS_FG_COL_DESC
# from katagames_sdk.capsule.pygame_provider import import_gfxdraw
# from katagames_sdk.capsule.struct.misc import enum_builder

pygame = None

# --------------------------------------------------
# [  ! ]_FORCE_ expose objects_[ !  ]
# --------------------------------------------------
version = VERSION = _defs.version

from katagames_sdk.en_parts.defs import HD_MODE, OLD_SCHOOL_MODE, SUPER_RETRO_MODE
e = HD_MODE or OLD_SCHOOL_MODE or SUPER_RETRO_MODE

from katagames_sdk.en_parts.events import EventReceiver, EngineEvTypes, CogObject, EventManager, CgmEvent
e = e or EventReceiver or EngineEvTypes or CogObject or EventManager or CgmEvent

from katagames_sdk.en_parts.conf_eng import runs_in_web as _r_web_context
from katagames_sdk.en_parts.conf_eng import import_gfxdraw
e = e or import_gfxdraw


def runs_in_web():  # keep it this way, for retro-compatibility
    return _r_web_context


from katagames_sdk.en_parts.defs import enum_for_custom_event_types
e = e or enum_for_custom_event_types

from katagames_sdk.en_parts.gfx_updater import display_update
e = e or display_update


# improve backward compat' (SDK)
def import_pygame():
    global pygame
    return pygame


# improve backward compat' (SDK)
def embody_lib(givenmodule):
    global pygame
    pygame = givenmodule


# - variables privées du module
_cached_screen = None


def screen_size():
    global _cached_screen
    if _cached_screen is None:
        _cached_screen = cgmconf.screen
    return _cached_screen.get_size()


def target_upscaling(mode):
    return {
        SUPER_RETRO_MODE: 3,
        OLD_SCHOOL_MODE: 2,
        HD_MODE: 1
    }[mode]


def target_w(mode):
    if mode == SUPER_RETRO_MODE:
        return 960 // 3
    if mode == OLD_SCHOOL_MODE:
        return 960 // 2
    return 960


def target_h(mode):
    if mode == SUPER_RETRO_MODE:
        return 540 // 3
    if mode == OLD_SCHOOL_MODE:
        return 540 // 2
    return 540


# +x0x0  dirty trick begins  0x0x+
# it has been put here for ONE sole purpose -> avoid auto-delete significant import lines... -<>>-
# t = (
#     gui, BaseGameState, enum_builder, EventReceiver, EngineEvTypes, CgmEvent, CogObject,
#     enum_for_custom_event_types, retrieve_game_ctrl, tag_multistate, get_manager,
#     BIOS_BG_COL_DESC, BIOS_FG_COL_DESC, import_gfxdraw
# )
# print(str(t)[:1]+'katasdk '+cgmconf.VERSION+' - https://kata.games/developers)')
# del t
# +x0x0  dirty trick ends  0x0x+


# -----------------------------------
# -<>- public procedures: engine -<>-
# -----------------------------------
def init(mode=HD_MODE):
    """
    :param mode: type str, describes what gfx mode we are using
    :return: nothing
    """
    kevent.PygameBridge = pygame.constants
    eng_.init(pygame, mode)


def get_game_ctrl():
    return eng_.retrieve_game_ctrl()


def cleanup():
    eng_.cleanup(pygame)


def get_manager():
    if cgmconf.runs_in_web:
        return pygame.key.linkto_ev_manager
    else:
        return EventManager.instance()


def get_screen():
    return cgmconf.screen


# -----------------------------------
# -<>- public procedures: utils -<>-
# -----------------------------------

def proj_to_vscreen(org_screen_pos):
    return cgmconf.conv_to_vscreen(*org_screen_pos)
