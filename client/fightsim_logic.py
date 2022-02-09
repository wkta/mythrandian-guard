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
import time

import pygame

from fightsim_view import draw_fighters


# ----------------------
#    brouillon modele fight
# ----------------------
class GenFighter:
    free_id = -1

    def __init__(self, level, power, en, ini, ability=None):
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
        self.ability = ability

    def detailled_desc(self):
        return 'fighter id#{} . level {} | dmg,hp={},{} \n pow,en,ini={}, {}, {}'.format(
            self.ident, self.level, self.dmg, self.maxhp, self.p, self.e, self.ini
        )

    def __str__(self):
        return "F{}\n {} /{}\ndmg:{} ini:{}".format(
            self.ident, self.hp, self.maxhp, self.dmg, self.ini
        )

    @classmethod
    def gen_random(cls):
        return cls(
            random.randint(1, 59),
            random.randint(1, 10),
            random.randint(1, 10),
            random.randint(1, 9)
        )


class Battle:
    # TODO order based on the Initiative stat.

    def __init__(self, teama, teamb):
        # position fighters according to .ini
        self.assoc_slot_idfighter = dict()
        cpt = 1
        for elt in teama:
            self.assoc_slot_idfighter[cpt] = elt
            cpt += 1
        cpt = -1
        for elt in teamb:
            self.assoc_slot_idfighter[cpt] = elt
            cpt -= 1

    def det_live_fighters(self, left_team) -> dict():
        dres = dict()
        for k, obj in self.assoc_slot_idfighter.items():
            if left_team and k > 0:
                if obj.hp > 0:
                    dres[k] = obj
            elif not left_team and k < 0:
                if obj.hp > 0:
                    dres[k] = obj
        return dres

    def det_idx_live_fighters(self, left_team) -> list:
        return list(self.det_live_fighters(left_team).keys())

    def is_over(self):
        live_a = self.det_idx_live_fighters(True)
        live_b = self.det_idx_live_fighters(False)
        return len(live_a) == 0 or len(live_b) == 0

    def perform_fight(self, turn_num):
        # TODO implem real combat order based on initiative stat.
        # TODO hits given should (more or less) alternate between 2 teams every round

        live_a = self.det_live_fighters(True)
        live_b = self.det_live_fighters(False)
        forder = {
            1: (live_a.values(), live_b.values()),
            0: (live_b.values(), live_a.values())
        }
        #while len(live_a) > 0 and len(live_b) > 0:
        #for turn in range(2):
        attackers, defenders = forder[turn_num % 2]
        for obj_atk in attackers:
            for enemy in defenders:
                if enemy.hp > 0:
                    enemy.hp -= obj_atk.dmg
                    print('F#{}  hits  F#{} '.format(obj_atk.ident, enemy.ident), end='')
                    if enemy.hp <= 0:
                        print('...And F#{} dies!'.format(enemy.ident))
                    else:
                        print()
                    break  # hit one guy only

        if self.is_over():
            print('battle has ended at turn {} !!!'.format(turn_num))
        else:
            print('turn {} ends.'.format(turn_num))


if __name__ == '__main__':
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
    pygame.init()
    w = pygame.display.set_mode((960, 540))

    team_a, team_b = [GenFighter.gen_random() for _ in range(5)], [GenFighter.gen_random() for _ in range(5)]

    b = Battle(team_a, team_b)

    # game loop
    gameover = False
    turn = 1

    while not gameover:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                gameover = True

        # refresh screen
        w.fill('darkblue')
        draw_fighters(w, b.det_idx_live_fighters(True), True, 'pink', team_a)
        draw_fighters(w, b.det_idx_live_fighters(False), False, 'orange', team_b)
        pygame.display.update()
        time.sleep(2)

        # logic update
        if not b.is_over():
            b.perform_fight(turn)
            turn += 1
    pygame.quit()
