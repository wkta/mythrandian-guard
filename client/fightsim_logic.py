"""
fight simulator (Game Logic)
this will be used both in mission & PvP (raids).

ONE RULE: keep it simple!
this rule is very important since the game logic will be coded a second time
on the server (PHP lang.)

So the following file works just like a complex MATH function with many parameters.
-> input= Two sets of fighters
<- output= history of the fight so you can "re-play" it and compute the winner
"""
import random

import pygame

from fightsim_view import draw_fighters


# ----------------------
#    brouillon modele fight
# ----------------------
class GenFighter:
    free_id = -1

    def __init__(self, level, power, en, ini, shadow_f_attrib=False):
        """
        ability depends on character class, it's just like "a spell" casted 1 time
        """
        self.__class__.free_id += 1
        self.ident = self.free_id

        self.p, self.e = power, en
        self.level = level
        self.dmg = (level // 2) + 3 * power
        self.hp = self.maxhp = 5 * en + level + 10

        self.ini = ini
        self.ranged = shadow_f_attrib

    def detailled_desc(self):
        tmp = 'x' if self.ranged else ' '
        return 'fighter id#{} . level {} .R{} | dmg,hp={},{} \n pow,en,ini={}, {}, {}'.format(
            self.ident, self.level, tmp, self.dmg, self.maxhp, self.p, self.e, self.ini
        )

    def __str__(self):
        return "F{} .L{} \n{} /{}\ndmg:{} ini:{}".format(
            self.ident, self.level, self.hp, self.maxhp, self.dmg, self.ini
        )

    @classmethod
    def gen_random(cls, b_v_ranged):
        return cls(
            random.randint(1, 59),
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 9),
            b_v_ranged
        )


class Battle:
    """
    What are combat slots?

       -ranged-> |    -other->
      ___.___._3_|___°___°_6_°___
      ___._2_.___|_4_°___°___°_7_
      _1_.___.___|___°_5_°___°___

    Battle logic=
    - RANGED characters are put in the back (3 possible slots), while REGULAR chars are
       put in the front (4 possible slots)

    - both categories get sorted separately, based on their initiative stat.
       for example RANGED fighters with ini. stats 8, 11, 3 would receive slots 2, 1, 3
       while REGULAR fighters with same ini. stats would receive slots

    - a fighter attacks the closest enemy, unless he's using a special attack
    """
    def find_closest_enemy(self, from_slot_n):
        """
        :param from_slot_n:

        :return: pair slot_number, fighter to be hit
        """
        # the larger the abs(number), the closest the enemy is
        candidate = None
        if self._fetch(from_slot_n).team == 0:
            live_en = self.det_idx_live_fighters(True)
            for i in range(-1, -8, -1):
                if i in live_en:
                    candidate = i
        else:
            live_en = self.det_live_fighters(False)
            for i in range(1, 8):
                if i in live_en:
                    candidate = i
        return candidate, self.assoc_slot_idfighter[candidate]

    def _fetch(self, key):
        return self.assoc_slot_idfighter[key]

    # TODO order based on the Initiative stat.

    def __init__(self, teama, teamb):
        # position fighters according to their ini stat + level if its equal
        self.assoc_slot_idfighter = dict()
        print('slot assignment ... ')
        self.inject_proc_sorting(teama, False)
        self.inject_proc_sorting(teamb, True)
        print("done!\n")

    def _tri(self, target_slots, equipe, sorting_ranged_b):
        """
        méthode privée (utile à l'algorithme de inject_proc_sorting...) pour faciliter le tri
        :param target_slots: une liste de positions qq part dans [-7 à -1] ou [1 à 7]
        :param equipe:
        :param sorting_ranged_b: bool
        """
        tripl_list = list()

        # add triples (ini, level, fighter id)
        for fobj in equipe.to_list():
            if fobj.ranged == sorting_ranged_b:
                tripl_list.append((fobj.ini, fobj.level, fobj.ident))
        tripl_list.sort(key=lambda u: (u[0], u[1]), reverse=True)
        cpt = 0

        while cpt < len(tripl_list):
            d = target_slots[cpt]
            self.assoc_slot_idfighter[d] = equipe.get_by_id(tripl_list[cpt][2])
            cpt += 1

    def inject_proc_sorting(self, equipe, right_team):
        # - sort ranged guys
        dest = [-1, -2, -3] if right_team else [1, 2, 3]
        self._tri(dest, equipe, True)

        # - sort non-ranged guys
        dest = [-4, -5, -6, -7] if right_team else [4, 5, 6, 7]
        self._tri(dest, equipe, False)

    def __getitem__(self, item):
        return self.assoc_slot_idfighter[item]

    def det_live_fighters(self, right_team) -> dict:
        dres = dict()
        for k, obj in self.assoc_slot_idfighter.items():
            if right_team and k < 0:
                if obj.hp > 0:
                    dres[k] = obj
            elif not right_team and k > 0:
                if obj.hp > 0:
                    dres[k] = obj
        return dres

    def det_idx_live_fighters(self, right_team) -> list:
        return list(self.det_live_fighters(right_team).keys())

    def is_over(self):
        live_a = self.det_idx_live_fighters(True)
        live_b = self.det_idx_live_fighters(False)
        return len(live_a) == 0 or len(live_b) == 0

    def perform_fight(self, turn_num):
        # TODO implem real combat order based on initiative stat.
        # TODO hits given should (more or less) alternate between 2 teams every round

        live_a = self.det_live_fighters(True)
        live_b = self.det_live_fighters(False)

        # rq : here the ally hits only one guy but the order is random!
        parite = turn_num % 2 == 0
        attackers = live_a if parite else live_b

        for from_slot, atker_obj in attackers.items():
            s, enemy = self.find_closest_enemy(from_slot)
            enemy.hp -= atker_obj.dmg
            print('F#{}  hits  F#{} '.format(atker_obj.ident, enemy.ident), end='')
            if enemy.hp <= 0:
                print('...And F#{} dies!'.format(enemy.ident))
                if self.is_over():
                    break
            else:
                print()

        if self.is_over():
            print('battle has ended at turn {} !!!'.format(turn_num))
        else:
            print('turn {} ends.'.format(turn_num))


class Team:
    """
    ensure the team is valid e.g. no more than 3 shadow fighters etc.

    no two allies where lvl1==lvl2 and ini1==ini2

    etc.
    """
    def __init__(self, fighterset, right_team):
        self._content = list(fighterset)
        for elt in self._content:
            if not right_team:
                elt.team = 0
            else:
                elt.team = 1
        # TODO verifications

    def get_by_id(self, i):
        for obj in self._content:
            if obj.ident == i:
                return obj

    def to_list(self):
        return self._content


def run_simu():
    # model debug
    print('-')
    aa = GenFighter(59, 10, 1, 1)
    print(aa)
    print(aa.detailled_desc())
    print('-')
    bb = GenFighter(59, 1, 10, 1)
    print(bb)
    print(bb.detailled_desc())
    print()

    # init pygame, init real model
    w = pygame.display.set_mode((960, 540))

    prec_a = [GenFighter.gen_random(False) for _ in range(3)]
    prec_a.extend([GenFighter.gen_random(True) for _ in range(2)])
    prec_b = [GenFighter.gen_random(False) for _ in range(2)]
    prec_b.extend([GenFighter.gen_random(True) for _ in range(3)])

    b = Battle(Team(prec_a, False), Team(prec_b, True))

    # game loop
    gameover = False
    turn = 1
    can_update = False
    while not gameover:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameover = True
            elif ev.type == pygame.KEYDOWN and pygame.K_SPACE == ev.key:
                can_update = True

        # logic update
        if can_update:
            can_update = False
            if not b.is_over():
                b.perform_fight(turn)
                turn += 1

        # refresh screen
        w.fill('darkblue')
        draw_fighters(w, True, 'pink', b)
        draw_fighters(w, False, 'orange', b)
        pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    run_simu()
    pygame.quit()
