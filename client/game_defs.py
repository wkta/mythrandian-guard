from pkatagames_sdk.engine.foundation.structures import enum_builder

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
