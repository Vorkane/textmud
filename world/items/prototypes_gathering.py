"""

Prototypes for Gather Resources

"""

from random import randint

### Mineral Based Materials and Gather Nodes
COPPER_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "copper vein",
    "desc": "An outcroppig of rocks appears to contain raw copper.",
    "spawn_proto": "COPPER_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

TIN_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "tin vein",
    "desc": "An outcroppig of rocks appears to contain raw tin.",
    "spawn_proto": "TIN_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

IRON_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "iron vein",
    "desc": "An outcroppig of rocks appears to contain raw iron.",
    "spawn_proto": "IRON_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

SILVER_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "silver vein",
    "desc": "An outcroppig of rocks appears to contain raw silver.",
    "spawn_proto": "SILVER_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

GOLD_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "gold vein",
    "desc": "An outcroppig of rocks appears to contain raw gold.",
    "spawn_proto": "GOLD_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

MITHRIL_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "mithril vein",
    "desc": "An outcroppig of rocks appears to contain raw mithril.",
    "spawn_proto": "MITHRIL_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

ADAMANTINE_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "adamantine vein",
    "desc": "An outcroppig of rocks appears to contain raw adamantine.",
    "spawn_proto": "ADAMANTINE_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

ORICHALCUM_ORE_NODE = {
    "typeclass": "world.items.mining.OreGatherNode",
    "key": "orichalcum vein",
    "desc": "An outcroppig of rocks appears to contain raw orichalcum.",
    "spawn_proto": "ORICHALCUM_ORE",
    "min_tier": "1",
    "gathers": lambda: randint(2, 10),
}

IRON_ORE = {
    "typeclass": "world.items.mining.Ore",
    "aliases": ["iron ore"],
    "key": "iron ore",
    "desc": "A clump of raw iron ore.",
    "tags": [("iron ore","crafting_material")],
    "value": 2,
    "weight": 0.75,
    "prototype_name": "IRON_ORE",
    "bundle_size": 2,
    "is_stackable": True,
}

IRON_ORE_BUNDLE = {
    "key": "a bundle of iron ore",
    "aliases": ["bundle of iron ore", "bundle iron ore", "iron ore"],
    "typeclass": "world.items.mining.OreBundle",
    "desc": "A bundle of iron ore held together with a thin leather strip.",
    "weight": 10,
    "value": 25,
    "quantity": 20,
    "prototype_name": "IRON_ORE",
}


### Wood Based Materials and Gather Nodes