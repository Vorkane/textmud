"""

Prototypes for Gather Resources

"""

from random import randint

# Mineral Based Materials and Gather Nodes

IRON_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "iron vein",
    "desc": "An outcroppig of rocks appears to contain raw iron.",
    "spawn_proto": "IRON_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

IRON_ORE = {
    "typeclass": "world.items.mining.IronOre",
    "key": "iron ore",
    "desc": "A clump of raw iron ore.",
    "tags": [("iron ore", "crafting_material")],
    "value": 2,
}

# Wood Based Materials and Gather Nodes
