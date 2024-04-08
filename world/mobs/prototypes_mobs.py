# from evennia.contrib.tutorials.evadventure.npcs import EvAdventureNPC
from random import randint

DUMMY = {
    "typeclass": "typeclasses.characters.Mob",
    "key": "Dummy",
    "name": "Stupid Dummy",
    "desc": "A training dummy.",
    "hp_max": lambda: randint(10, 40),
    "attrs_add": {'HP': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Health'}},
}
