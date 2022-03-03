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
import glvars
import katagames_sdk.katagames_engine as kengi
from app.battle_state import BattleState
from app.main_screen_state import MainScreenState
from app.shopping_state import ShoppingState
from app.show_collection_state import ShowCollectionState
from game_defs import GameStates

print('Mythrandian Guard demo: /!\\ Current kengi version is: ', kengi.vernum)

CgmEvent = kengi.event.CgmEvent
StackBasedGameCtrl = kengi.event.StackBasedGameCtrl
# CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kengi.core.init()
WIN_CAPTION = 'Mythrandian Guard'
kengi.pygame.display.set_caption(WIN_CAPTION)
# bios_like_st = KataFrameState(-1, 'bios-like', game_defs)

ctrl = StackBasedGameCtrl(
    kengi.core.get_game_ctrl(),
    glvars,
    game_defs.GameStates,
    {
        GameStates.MainScreen: MainScreenState,
        GameStates.Battle: BattleState,
        GameStates.Shopping: ShoppingState,
        GameStates.ShowCollection: ShowCollectionState
    }
)

ctrl.turn_on()
ctrl.loop()
kengi.core.cleanup()
