""""
** Mythrandian Guard **
a game of Heroes and Lackeys
un jeu de Héros et de Laquais

project started by: wkta-tom (contact@kata.games )
+ authored by various users see the CONTRIBUTORS file
started in Dec. 2021

important notice:
All project files (source-code) that ARE NOT part of katagames_sdk
are licensed under the:
MIT License
"""
import game_defs
import katagames_sdk.engine as kataen
from katagames_sdk.engine.foundation.defs import enum_for_custom_event_types
from game_events import MyEvTypes
from katagames_sdk.engine.foundation.events import CgmEvent
from katagames_sdk.engine.foundation.runners import StackBasedGameCtrl

# import states
from app.main_screen_state import MainScreenState
from app.fighting_state import FightingState
from app.shopping_state import ShoppingState
from app.show_collection_state import ShowCollectionState


CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kataen.init()
WIN_CAPTION = 'Mythrandian Guard'
kataen.pygame.display.set_caption(WIN_CAPTION)
# bios_like_st = KataFrameState(-1, 'bios-like', game_defs)

ctrl = StackBasedGameCtrl(
    kataen.get_game_ctrl(),
    game_defs.GameStates,
    {
        'MainScreenState': MainScreenState,
        'FightingState': FightingState,
        'ShoppingState': ShoppingState,
        'ShowCollectionState': ShowCollectionState
    },
    kataen.pygame,
    katagame_st=None
)

ctrl.turn_on()
ctrl.loop()
kataen.cleanup()
