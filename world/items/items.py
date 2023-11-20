from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from evennia.objects.objects import DefaultObject
from evennia import create_object
from evennia.prototypes.spawner import spawn


class Item(DefaultObject):
    """
    Typeclass for Items.
    Attributes:
        value (int): monetary value of the item in CP
        weight (float): weight of the item
        hardness (int): how susceptible to damage a object is
        durability (int): how much damage an item can sustain before being destroyed
        current (int): how much durability an item currently has remaining
    """

    value = 0
    weight = 0.0
    hardness = 0
    current = 0
    durability = 0


    def at_object_creation(self):
        super(Item, self).at_object_creation()
        self.locks.add(";".join(("puppet:perm(Wizards)",
                                 "equip:false()",
                                 "get:true()"
                                 )))
        #self.db.itemid = self.itemid
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.hardness = self.hardness
        self.db.durability = self.durability
        self.db.current = self.current

    def return_appearance(self,looker):
        if not looker:
            return

        looker.msg("%s|/" % self.db.desc)
        #looker.msg("%s %s." % (self.key, item_dura(self)))

    def at_get(self, getter):
        pass

    def at_drop(self, dropper):
        pass

class Bundlable(Item):
    """Typeclass for items that can be bundled."""
    def at_object_creation(self):
        super(Bundlable, self).at_object_creation()
        self.db.bundle_size = 999
        self.db.prototype_name = None

    def at_get(self, getter):
        super(Bundlable, self).at_get(getter)
        bundle_key = self.aliases.all()[0]
        others = [obj for obj in getter.contents
                  if obj.is_typeclass('typeclasses.items.Bundlable')
                  and bundle_key in obj.aliases.all()]

        if len(others) >= self.db.bundle_size \
                and self.db.prototype_name and self.aliases.all():

            # we have enough to create a bundle

            bundle = create_object(
                typeclass='typeclasses.items.Bundle',
                key='a bundle of {}s'.format(bundle_key),
                aliases=['bundle {}'.format(bundle_key)],
                location=self.location
            )
            bundle.db.desc = ("A bundle of {item}s held together "
                              "with a thin leather strap.").format(
                item=bundle_key
            )
            bundle.db.value = self.db.bundle_size * self.db.value
            bundle.db.weight = self.db.bundle_size * self.db.weight
            bundle.db.quantity = self.db.bundle_size
            bundle.db.prototype_name = self.db.prototype_name
            for obj in others[:self.db.bundle_size]:
                obj.delete()


class Bundle(Item):
    """Typeclass for bundles of Items."""
    def expand(self):
        """Expands a bundle into its component items."""
        for i in range(self.db.quantity):
            spawn(dict(prototype=self.db.prototype_name,
                       location=self.location))
        self.delete()

class Equippable(Item):
    """
    Typeclass for equippable Items.
    Attributes:
        slots (str, list[str]): list of slots for equipping
        multi_slot (bool): operator for multiple slots. False equips to
            first available slot; True requires all listed slots available.
    """
    slots = None
    multi_slot = False

    def at_object_creation(self):
        super(Equippable, self).at_object_creation()
        self.locks.add("puppet:false();equip:true()")
        self.db.slots = self.slots
        self.db.multi_slot = self.multi_slot
        self.db.used_by = None

    def at_equip(self, character):
        """
        Hook called when an object is equipped by character.
        Args:
            character: the character equipping this object
        """
        pass

    def at_remove(self, character):
        """
        Hook called when an object is removed from character equip.
        Args:
            character: the character removing this object
        """
        pass

    def at_drop(self, dropper):
        super(Equippable, self).at_drop(dropper)
        if self in dropper.equip:
            dropper.equip.remove(self)
            self.at_remove(dropper)