import katagames_sdk.katagames_engine as kengi


MyEvTypes = kengi.struct.enum(
    'ChallengeStarts',  # is it useful in this project?

    'LackeyBought',  # contains idx

    'PlayerBuysItem',
    'WannaBuySkin',  # deprec
    'EquipOwnedSkin',  # deprec

    'FightStarts',

    'MissionStarts',  # contains t, idx
    'MissionEnds',  # contains idx

    'MissionFree',  # only for the view, contains idx

    'AvatarUpdate',  # only here to force view refresh itself
    'NotifyAutoloot'  # contains is_gold, amount
)
