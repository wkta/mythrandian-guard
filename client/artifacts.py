"""
Definition file for artifacts only
IMPORTANT REMARK:
    this file is not meant to be imported directly, preferably use -> import game_defs
"""

from pkatagames_sdk.capsule.struct.misc import enum_builder


ArtifactCodes = enum_builder(
    'KingsPlate',
    'Relics',
    'StaffNin',
)

ArtifactNames = {
    ArtifactCodes.KingsPlate: {
        0: 'Plate Armour of the forgotten king',  # 0 -> artifact's name, always

        1: 'Breastplate',
        2: 'Greaves',
        3: 'Spaulders',
        4: 'Sallet',
        5: 'Visor'
    },
    ArtifactCodes.Relics: {
        0: 'Relics of Matangi',

        1: 'Loincloth',
        2: 'Club',
        3: 'Shield',
        4: 'Necklace'
    },
    ArtifactCodes.StaffNin: {
        0: 'Antique Staff of Nin',

        1: 'The head',
        2: 'Ash wood stick'
    }
}


def create_artifact_storage():
    global ArtifactNames
    """
    Aims at easing specific info. (about the artifacts collection) storage
    
    :return: an objects whose precise format is
        {
            ArtifactCodes.KingsPlate: {
                1: False,  # part 1 -> Breastplate
                2: False,  # part 2... etc
                3: False, 
                4: False,  
                5: False,
            },
            ...
        }
    :rtype: dict
    """
    res = dict()
    for code in ArtifactNames.keys():
        res[code] = dict()
        for idx in ArtifactNames[code].keys():
            if idx:
                res[code][idx] = False
    return res
