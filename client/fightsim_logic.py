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

    # /!\ in formulas: assuming max level is 59
    # z 5.929723110029351

    def __init__(self, level, ini, en, shadow_f_attrib=False):
        """
        ability depends on character class, it's just like "a spell" casted 1 time
        """
        self.__class__.free_id += 1
        self.ident = self.free_id

        self.slot = None

        # assumptions
        max_dmg = 50
        z = 1.0809965933
        maxlevel = 59

        # display only
        self.en = en

        # sert au placement auto.
        self.ranged = shadow_f_attrib
        self.ini = ini
        self.level = level

        # stats de combat impactantes
        self.dmg = 1 + int(max_dmg - z**(maxlevel-level) / 2)  # flipped exponential func
        print('level{}  -> dmg= {}'.format(level, self.dmg))
        self.hp = self.maxhp = 44 + int(level + en**3/4)

    @property
    def is_dead(self):
        return self.hp <= 0

    def __str__(self):
        tmp = '+' if self.ranged else '-'
        return 'F#{} r{} Lv{}\n ini{} dmg{}\n Hp={}/{}'.format(
            self.ident, tmp, self.level, self.ini, self.dmg, self.hp, self.maxhp,
        )

    @classmethod
    def gen_random(cls, b_v_ranged):
        return cls(
            random.randint(1, 59),
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

    def __init__(self, teama, teamb):
        self.assoc_slot_idfighter = dict()

        # position fighters according to their ini stat + level if its equal
        self.inject_proc_sorting(teama, False)
        self.inject_proc_sorting(teamb, True)

        self.lastactive_fighter = {
            0: None,
            1: None
        }

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
            f_obj = equipe.get_by_id(tripl_list[cpt][2])
            self.assoc_slot_idfighter[d] = f_obj
            f_obj.slot = d
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

    # -------------------------------------------------------
    #  implem logique de combat
    # -------------------------------------------------------
    def _get_top_priority_f(self, teamplayin) -> GenFighter:
        """
        :param teamplayin:
        :return: fighter obj, the guy who has the highest priority for attack
        """
        alpha = -1 if teamplayin else 1
        for i in range(1 * alpha, 8 * alpha, 1 * alpha):
            if not self.assoc_slot_idfighter[i].is_dead:
                return self.assoc_slot_idfighter[i]

    def _get_fighter_after(self, last_f_idx, teamplayin) -> GenFighter:
        """
        :param last_f_idx:
        :param teamplayin:
        :return: fighter obj, the guy who should attack now. Need to ignore dead fighters
        """
        if self.is_over():
            raise NotImplemented

        delta = -1 if teamplayin else +1
        xf = last_f_idx

        def go_next():
            nonlocal xf, delta
            xf += delta
            if xf < -8:
                xf = -1
            elif xf > 8:
                xf = 1

        go_next()
        while (xf not in self.assoc_slot_idfighter) or self.assoc_slot_idfighter[xf].is_dead:
            go_next()
        return self.assoc_slot_idfighter[xf]

    def _get_close_enemy(self, teamplayin) -> GenFighter:
        """
        :param teamplayin:
        :return: fighter who should tank
        """
        # the larger the abs(number), the closest the enemy is
        candidate = None
        if teamplayin:
            live_en = self.det_live_fighters(False)
            for i in range(1, 8):
                if i in live_en:
                    candidate = i
        else:
            live_en = self.det_idx_live_fighters(True)
            for i in range(-1, -8, -1):
                if i in live_en:
                    candidate = i
        return self.assoc_slot_idfighter[candidate]

    def increm_fight(self, turn_num):
        """
        hits given alternate between 2 teams every round
        :param turn_num:
        :return:
        """
        team_playing = turn_num % 2  # => value 0 or 1

        # select who attacks and who defends
        comes_after_f = self.lastactive_fighter[team_playing]
        if comes_after_f is None:
            attacker = self._get_top_priority_f(team_playing)
        else:
            attacker = self._get_fighter_after(comes_after_f, team_playing)
        defender = self._get_close_enemy(team_playing)

        defender.hp -= attacker.dmg
        # save info who played last
        self.lastactive_fighter[team_playing] = attacker.slot

        # - debug
        print('F#{}  hits  F#{} '.format(attacker.ident, defender.ident), end='')
        if defender.hp <= 0:
            print('...And F#{} dies!'.format(defender.ident))
        print('turn {} ends'.format(turn_num))


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
    # model debug test valeurs extremes
    for lvl in (1, 59):
        for en in (1, 10):
            tf = GenFighter(lvl, 1, en)
            print(tf)

    print()
    print('----------- * * * -')

    # init pygame, init real model
    w = pygame.display.set_mode((960, 540))

    prec_a = [GenFighter.gen_random(False) for _ in range(3)]
    prec_a.extend([GenFighter.gen_random(True) for _ in range(2)])  # deux ranged

    prec_b = [GenFighter.gen_random(False) for _ in range(2)]
    prec_b.extend([GenFighter.gen_random(True) for _ in range(3)])  # trois ranged

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
                b.increm_fight(turn)
                if b.is_over():
                    print('battle has ended at turn {} !!!'.format(turn))
                else:
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
