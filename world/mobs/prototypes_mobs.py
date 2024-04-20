# from evennia.contrib.tutorials.evadventure.npcs import EvAdventureNPC
from random import randint

DUMMY = {
    "typeclass": "typeclasses.npcs.Mob",
    "key": "Dummy",
    "name": "Stupid Dummy",
    "desc": "A training dummy.",
    "hp_max": lambda: randint(10, 40),
    "is_idle": True,
}
