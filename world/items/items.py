from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
# from evennia.objects.objects import DefaultObject
from evennia.contrib.game_systems.containers import ContribContainer


class Item(ContribRPObject):
    """
    Typeclass for Items.
    Attributes:
        value (int): monetary value of the item in CP
        weight (float): weight of the item
        hardness (int): how susceptible to damage a object is
        durability (int): how much damage an item can sustain before being destroyed
        current (int): how much durability an item currently has remaining
    """
    quality = "Common"
    value = 0
    weight = 0.0
    hardness = 0
    current = 0
    durability = 0

    def get_display_name(self, looker, **kwargs):
        # grab the color code stored in db.color_code,
        # or default to "|w"
        if self.db.quality == "Common":
            self.db.color_code = "|000"
        if self.db.quality == "Uncommon":
            self.db.color_code = "|141"
        if self.db.quality == "Rare":
            self.db.color_code = "|135"
        if self.db.quality == "Unique":
            self.db.color_code = "|210"

        color = self.db.color_code or "|W"
        # use the original get_display_name hook to get our name
        name = super(Item, self).get_display_name(looker, **kwargs)
        # either create a string based on self.db.modifiers, or default to an
        # empty string
        modifiers = " ".join(self.db.modifiers or [])
        return ("{color}{name}|n{modifiers}".format(color=color, name=name, modifiers=modifiers))

    def at_object_creation(self):
        super(Item, self).at_object_creation()
        self.locks.add(";".join(("puppet:perm(Wizards)",
                                 "equip:false()",
                                 "get:true()"
                                 )))
        # self.db.itemid = self.itemid
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.hardness = self.hardness
        self.db.durability = self.durability
        self.db.current = self.current

    def return_appearance(self, looker):
        if not looker:
            return

        looker.msg("%s|/" % self.db.desc)
        # looker.msg("%s %s." % (self.key, item_dura(self)))

    def at_get(self, getter):
        pass

    def at_drop(self, dropper):
        pass


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


class ObjContainer(ContribContainer):
    pass
