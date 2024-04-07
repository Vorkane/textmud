# from evennia.contrib.tutorials.evadventure.npcs import EvAdventureNPC
from random import randint


DUMMY = {
    "typeclass": "typeclasses.characters.NPC",
    "key": "Dummy",
    "name": "Stupid Dummy",
    "desc": "A training dummy.",
    "hp_max": lambda: randint(10, 40),
}
