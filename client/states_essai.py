import pkatagames_sdk.engine as kataen
from app import ClickChallgState, MainMenuState
import game_defs
from pkatagames_sdk.engine.foundation.defs import enum_for_custom_event_types
from pkatagames_sdk.engine.foundation.events import CgmEvent
from pkatagames_sdk.engine.foundation.runners import StackBasedGameCtrl


# custom events
from pkatagames_sdk.ext_kata_svc.bios_like_state import KataFrameState

MyEvTypes = enum_for_custom_event_types(
    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kataen.init(kataen.HD_MODE)
WIN_CAPTION = 'How the stack works'
kataen.import_pygame().display.set_caption(WIN_CAPTION)

# bios_like_st = KataFrameState(-1, 'bios-like', game_defs)

ctrl = StackBasedGameCtrl(kataen.get_game_ctrl(), game_defs.GameStates,
                          {'MainMenuState': MainMenuState, 'ClickChallgState': ClickChallgState},
                          kataen.import_pygame(), katagame_st=None)
# - run the game
ctrl.turn_on()
ctrl.loop()

kataen.cleanup()
