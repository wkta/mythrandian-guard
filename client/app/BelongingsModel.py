from game_defs import create_artifact_storage, ArtifactCodes, ArtifactNames
from game_defs import LackeyCodes, MAX_MANA_PTS, BASE_LIMIT_LACKEYS
import random


class Artifact:
    def __init__(self, acode, element):
        if acode not in ArtifactCodes.all_codes:
            raise ValueError('non-valid artifact code ({})'.format(acode))
        if (not isinstance(element, int)) or (element not in ArtifactNames[acode]):
            raise ValueError('non-valid artifact element ({}, code={})'.format(element, acode))
        self._code = acode
        self._elt = element

    @classmethod
    def gen_random(cls):
        c = random.choice(ArtifactCodes.all_codes)
        omega_elt = list(ArtifactNames[c].keys())
        omega_elt.remove(0)
        return cls(c, random.choice(omega_elt))

    def __str__(self):
        res = '[{}]\n'.format(ArtifactNames[self._code][0])
        res += '{}'.format(ArtifactNames[self._code][self._elt])
        return res


class BelongingsModel:
    """
    Modelise tt ce que l'avatar peut collectionner/posséder.
    Dans le game design on a imaginé 7 ressources:

    - Xp

    - gold pieces
    - items héros
    - artifacts (collectibles)
    - mana points, potion of mana
    - lackeys (up to 5)
    - enchantments (-> progrès temporaire/permanent)

    A part l'Xp tout est modélisé via cette classe
    """

    def __init__(self, gp, lackey_list=None):
        self.gp = gp
        self._eq_items = {
            'head': None, 'hands': None, 'torso': None, 'legs': None
        }
        self._artifacts = create_artifact_storage()
        self._mp = MAX_MANA_PTS
        if lackey_list:
            self.lackeys = lackey_list
        else:
            self.lackeys = [None for _ in range(BASE_LIMIT_LACKEYS)]
            self._init_random_lackeys()
        self._enchantments = set()

    def _init_random_lackeys(self):
        self.lackeys[0] = LackeyCodes.SmallOrc
        if random.random() < 0.6:
            self.lackeys[1] = LackeyCodes.FriendlySpider
            if random.random() < 0.6:
                self.lackeys[2] = LackeyCodes.Slime
                if random.random() < 0.5:
                    self.lackeys[3] = LackeyCodes.MountainTroll

    def describe_lackeys(self):
        res = ''
        cpt = 0
        for t in self.lackeys:
            if t:
                cpt += 1
        res += '{} lackeys'.format(cpt)
        if cpt:
            res += ':\n'
        for ii in range(cpt):
            # lackey code, to str
            res += ' - {}'.format(LackeyCodes.inv_map[self.lackeys[ii]])
            if ii != cpt-1:
                res += '\n'
        return res
