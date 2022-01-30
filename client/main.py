""""
** Mythrandian Guard **
a game of Heroes and Lackeys
un jeu de Héros et de Laquais

project started by: wkta-tom (contact@kata.games )
+ authored by various users see the CONTRIBUTORS file
started in Dec. 2021

important notice:
All project files (source-code) that ARE NOT part of pkatagames_sdk
are licensed under the:
MIT License

the presence of the pkatagames_sdk is temporary in this project,
and it shall be removed at some point of game development.
"""
import game_defs
import pkatagames_sdk.engine as kataen
from app import *
from pkatagames_sdk.engine.foundation.defs import enum_for_custom_event_types
from pkatagames_sdk.engine.foundation.events import CgmEvent
from pkatagames_sdk.engine.foundation.runners import StackBasedGameCtrl


MyEvTypes = enum_for_custom_event_types(
    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kataen.init(kataen.HD_MODE)
WIN_CAPTION = 'Mythrandian Guard'
kataen.import_pygame().display.set_caption(WIN_CAPTION)
# bios_like_st = KataFrameState(-1, 'bios-like', game_defs)
ctrl = StackBasedGameCtrl(
    kataen.get_game_ctrl(),
    game_defs.GameStates,
    {
        'MainScreenState': MainScreenState,
        'FightingState': FightingState,
        'ShoppingState': ShoppingState
    },
    kataen.import_pygame(),
    katagame_st=None
)

ctrl.turn_on()
ctrl.loop()
kataen.cleanup()
