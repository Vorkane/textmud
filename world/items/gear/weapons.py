"""
    Weapon Typeclasses
"""

from world.items.items import Equippable


class Weapon(Equippable):
    """

    Args:
        Equippable (_type_): _description_
    """

    slots = ['wield1', 'wield2']
    multi_slot = False

    damage_roll = ''
    handedness = 1
    range = 'melee'

    def at_object_creation(self):
        super(Weapon, self).at_object_creation()

        self.db.range = self.range
        self.db.damage_roll = self.damage_roll
        self.db.handedness = self.handedness
        self.db.worn = False

    def at_equip(self, character):
        self.db.worn = True
        # character.traits.PDEF.mod += self.db.physical_bonus
        # character.traits.MDEF.mod += self.db.magical_bonus

    def at_remove(self, character):
        self.db.worn = False
        # character.traits.PDEF.mod -= self.db.physical_bonus
        # character.traits.MDEF.mod -= self.db.magical_bonus
