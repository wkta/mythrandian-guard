"""
fight simulation

this will be used both in mission & PvP (raids).

ONE RULE: keep it simple
"""


class GenFighter:
    def __init__(self, char_class, level, ini):
        self.char_class = char_class
        self.level = level  # this+class => hpmax, power
        self.ini = ini
        self.hpmax = 2*level if char_class == 'tank' else level
        self.power = 2*level if char_class == 'dd' else level

    @staticmethod
    def perform_fight(gteam1, gteam2):
        # fight algorithm
        hitpoins = {1: dict(), 2: dict()}
        attacklevel = {1: dict(), 2: dict()}

        for k, guy in enumerate(gteam1):
            hitpoins[1][k] = guy.hpmax
            attacklevel[1][k] = guy.power
        for k, guy in enumerate(gteam2):
            hitpoins[2][k] = guy.hpmax
            attacklevel[2][k] = guy.power
        print(hitpoins)
        print(attacklevel)

        # TODO fight order?


if __name__ == '__main__':
    team1 = [
        GenFighter('tank', 13, 5),
        GenFighter('dd', 10, 12),
        GenFighter('supp', 11, 10),
    ]

    team2 = [
        GenFighter('dd', 15, 13),
        GenFighter('dd', 10, 17)
    ]
    GenFighter.perform_fight(team1, team2)
