from pkatagames_sdk.engine import enum_for_custom_event_types

MyEvTypes = enum_for_custom_event_types(
    'PlayerBuysItem',
    'WannaBuySkin',  # deprec
    'EquipOwnedSkin'  # deprec
)
