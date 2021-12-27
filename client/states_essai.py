import pkatagames_sdk.engine as kataen
from app import ClickChallgState, MainMenuState
from game_defs import GameStates
from pkatagames_sdk.engine.foundation.defs import enum_for_custom_event_types
from pkatagames_sdk.engine.foundation.events import CgmEvent
from pkatagames_sdk.engine.foundation.runners import StackBasedGameCtrl


# custom events
MyEvTypes = enum_for_custom_event_types(
    'ChallengeStarts',
)
CgmEvent.inject_custom_names(MyEvTypes)

# - main program
kataen.init(kataen.HD_MODE)
WIN_CAPTION = 'How the stack works'
kataen.import_pygame().display.set_caption(WIN_CAPTION)

ctrl = StackBasedGameCtrl(kataen.get_game_ctrl(), GameStates,
                          {'MainMenuState': MainMenuState, 'ClickChallgState': ClickChallgState},
                          kataen.import_pygame())
# - run the game
ctrl.turn_on()
ctrl.loop()

kataen.cleanup()
