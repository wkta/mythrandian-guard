from artifacts import *


# listing of gamestates
GameStates = enum_builder(
    'MenuAventures',
    'Fighting',
    'Shopping'
)

# shared variables
username = ''
acc_id = None
the_avatar = None  # to be shared with other game states (local avatar's model)

# other game elements, except artifacts
BASE_LIMIT_LACKEYS = 5
MAX_MANA_PTS = 8

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
