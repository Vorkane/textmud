from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from typeclasses.objects import Object

class OreNode(Object):
    """
    Typeclass for Ore Node Objects.
    Attributes:
        ore_type (string): type of ore for the node
        respawn_time (int): time in seconds for the node to respawn (e.g., 3600 = 1 hour)
        is_mineable (boolean): boolean if the node is available to mine
    """
    def at_object_creation(self):
        super(OreNode, self).at_object_creation()
        self.db.ore_type = self.ore_type
        self.db.respawn_time = self.respawn_time
        self.db.is_mineable = self.is_mineable

    ore_type = ""
    respawn_time = 0
    is_mineable = True

class Ore(ContribRPObject):
    """
    Typeclass for Ore Objects.
    Attributes:
        value (int): monetary value
        weight (float): weight of the item

    """
    def at_object_creation(self):
        super(Ore, self).at_object_creation()
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.ore_type = self.ore_type

    value = 0
    weight = 0.0
    ore_type = ""

class CopperOreNode(OreNode):

    def at_object_creation(self):
        super(IronOreNode, self).at_object_creation()
        self.key = "copper node"
        self.name = "|Ocopper node|n"
        self.db.desc = "A copper node sits here."
        self.db.ore_type = "copper"
        self.db.respawn_time = 5
        self.db.is_mineable = True

class IronOreNode(OreNode):

    def at_object_creation(self):
        super(IronOreNode, self).at_object_creation()
        self.key = "iron node"
        self.db.color_code = "|R"
        self.name = "iron node"
        self.db.desc = "A |Riron node|n sits here."
        self.db.ore_type = "iron"
        self.db.respawn_time = 5
        self.db.is_mineable = True

class CopperOre(Ore):

    def at_object_creation(self):
        super(CopperOre, self).at_object_creation()
        self.key = "copper ore"
        self.name = "|228copper ore|n"
        self.db.desc = "A piece of copper ore."
        self.db.weight = 0.5
        self.db.ore_type = "copper"

class IronOre(Ore):

    def at_object_creation(self):
        super(IronOre, self).at_object_creation()
        self.key = "iron ore"
        self.name = "|Riron ore|n"
        self.db.desc = "A piece of iron ore."
        self.db.weight = 0.75
        self.db.ore_type = "iron"  # You can change this to other ore type.