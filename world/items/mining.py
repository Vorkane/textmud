from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from typeclasses.objects import Object
from random import randint
from evennia.prototypes import spawner, prototypes
from world.commands.professions.blacksmithing import MineCmdSet

class OreGatherNode(ContribRPObject):
    """
    An object which, when mined, allows players to gather a material resource.
    """
    is_mineable = True
    req_material = ""

    def at_object_creation(self):
        self.locks.add("get:false()")
        self.db.is_mineable = self.is_mineable
        self.db.req_material = self.req_material
        #self.cmdset.add(MineCmdSet)

    def get_display_footer(self, looker, **kwargs):
        return "You can |wgather|n from this."
    
    def at_gather(self, chara, **kwargs):
        """
        Creates the actual material object for the player to collect.
        """
        if not (proto_key := self.db.spawn_proto):
            # Somehow this node has not material to spawn
            chara.msg(f"The {self.get_display_name(chara)} disappears in a puff of confusion.")
            # Get rid of ourself, since we're broken
            self.delete()
            return
        
        if not (remaining := self.db.gathers):
            # This node has been used up
            chara.msg(f"There is nothing left.")
            # Get rid of ourself, since we're empty
            self.delete()
            return
        
        # Grab randomized amount to spawn
        amt = randint(1, min(remaining, 3))

        # Spawn the items!
        objs = spawner.spawn(*[proto_key] * amt)
        for obj in objs:
            # Move to the gathering character
            obj.location = chara
        
        if amt == remaining:
            chara.msg(f"You collect the last {obj.get_numbered_name(amt, chara)[1]}.")
            self.delete()
        else:
            chara.msg(f"You collect {obj.get_numbered_name(amt, chara)[1]}.")
            self.db.gathers -= amt


class OreNode(ContribRPObject):
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