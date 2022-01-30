from artifacts import *
from pkatagames_sdk.capsule.struct.misc import enum_builder_nplus

# all global constants
BASE_LIMIT_LACKEYS = 5
MAX_MANA_PTS = 8

# listing of gamestates
GameStates = enum_builder(
    'MainScreen',
    'Fighting',
    'Shopping'
)


LackeyCodes = enum_builder(
    'CaveTroll',
    'MountainTroll',
    'FriendlySpider',
    'SmallOrc',
    'Slime'
)

EnchantmentCodes = enum_builder(
    'Archmage',  # incr. mana regen
    'Blacksmith',  # (temp) lower price on the next armor
    'GoldenTouch',  # incr. gold loot
    'Rooted',  # incr. hp regen
    'SwiftLearner',  # incr. xp
    'Warlord'  # +1 mission slot
)

# - 4 defs here maybe deprecated? Was imported from old codebase
ASSETS_DIR = 'assets'

AvLooks = enum_builder_nplus(
    3,
    'OldMan',
    'no4',
    'RiceFarmer',
    'no6',
    'no7',
    'no8',
    'no9',
    'no10',
    'no11',
    'no12',
    'Smith',
    'no14',
    'no15',
    'GrandPa',
    'Amazon',
    'no18',
    'no19',
    'GoldenKnight',
    'no21',
    'no22',
    'Skeleton'
)

SUPPORTED_LOOKS = (
    AvLooks.OldMan,
    AvLooks.RiceFarmer,
    AvLooks.Smith,
    AvLooks.GrandPa,
    AvLooks.Amazon,
    AvLooks.Skeleton,
    AvLooks.GoldenKnight
)

ASSOC_IDPORTRAIT_FILENAME = {
    2: 'portrait3.png',
    3: 'portrait3.png',
    5: 'portrait5.png',
    13: 'portrait13.png',
    16: 'portrait16.png',
    17: 'portrait17.png',
    20: 'portrait20.png',
    23: 'portrait23.png'
}
