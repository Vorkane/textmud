from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from world.items.items import Equippable
from typeclasses.objects import Object
from world.commands.mining import CmdMine

from commands.custom_commands import CmdSetBlackSmithA
from commands.custom_commands import CmdSetBlackSmithR

class CraftingTool(Equippable):
    """
    Typeclass for Ore Objects.
    Attributes:
        value (int): monetary value
        weight (float): weight of the item

    """

    slots = ['wield1', 'wield2']
    multi_slot = False
    handedness = 1
    value = 0
    weight = 0.0
    material = ""

    def at_object_creation(self):
        super(CraftingTool, self).at_object_creation()
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.handedness = self.handedness
    
    def at_equip(self, character):
        """character.traits.MAB.mod += self.db.damage"""
        pass

    def at_remove(self, character):
        """character.traits.MAB.mod -= self.db.damage"""
        pass


class PickAxe(CraftingTool):

    slots = ['wield1']
    multi_slot = False
    handedness = 1
    weight = 2.0

    def at_object_creation(self):
        super(PickAxe, self).at_object_creation()
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.handedness = self.handedness
        
    def at_equip(self, character):
        pass

    def at_remove(self, character):
        pass