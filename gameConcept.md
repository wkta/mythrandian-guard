# Mythrandian Guard: game concept

the game is a mix between the idle game & management game genres.


## Avatar stats

there are 7 (or 11, it depends on how you count it) dynamic stats related to the Player's avatar:
* passive gold income 
* max mana
* mana regen
* max hp
* level
* power (a triplet)
* armor (a triplet)


## Lackey attributes

Differences relative to the avatar. Lackeys have:
* a "universal" level of power, and no armor
* a special stat called "initiative". It determines the order of turns during fights.
* a role "damage dealer", "tank", "support"


## Resources

there are 5 resources that can be collected by players:
* gold pieces
* mana points (represented by potions)
* lackeys
* artifacts
* avatar's equipment

Bonuses (=stats buff) can be acquired via avatar's gear *Or* enchantments:
* temporary enchantments (from spells) 
* permanent ones (complete collections)


## Enchantments

* Spells
  * *Fury* you can send a minimum of 2 fighters to attempt a mission (instead of 3)
  * *Focus* your mana regen gets +2
* Enchanments
  * *Archmage* your mana regen gets +1
  * *Gold Touch* passive gold income +20%
  * *Grounded* max hp +10%

## Combat
this part should describe rules that determines the outcome of a fight.
for missions usually you can send 3-6 fighters if you are not trying anything
fancy, just sending the team: DD + Tank + Support should give a good
probability of success. Doubling this should give 100% success rate.

Check `fight_sim.py` for more detailled infos.
