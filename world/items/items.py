from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
# from evennia.objects.objects import DefaultObject
from evennia.contrib.game_systems.containers import ContribContainer
from world.rulebook import item_durability
from evennia.utils.evform import EvForm
from evennia.utils.utils import make_iter


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
    curr_dura = 0
    max_dura = 0

    appearance_template = """
        {header}
        |c{name}{extra_name_info}|n
        {desc}
        {exits}
        {characters}
        {things}
        {footer}
            """

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
        self.db.max_dura = self.max_dura
        self.db.curr_dura = self.max_dura

    def return_appearance(self, looker):
        if not looker:
            return

        form = EvForm('commands.templates.itemsheet', align='l')
        form.map(cells={'A': self.get_display_name(self),
                        'B': self.db.curr_dura,
                        'C': self.db.max_dura,
                        'D': self.db.desc,
                        'E': item_durability(self) if (self.max_dura) else "None"})

        # fields = {
        #     'A': self.key,
        #     'B': self.db.curr_dura,
        #     'C': self.db.max_dura,
        #     'D': self.db.desc,
        # }

        # form.map({k: self._format_trait_val(v) for k, v in fields.items()})

        looker.msg(form)

        # looker.msg("%s|/" % self.db.desc)
        # looker.msg("%s %s." % (self.key, item_durability(self)))

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

    def has_obj_type(self, objtype):
        """
        Check if object is of a particular type.

        typeobj_enum (enum.ObjType): A type to check, like enums.TypeObj.TREASURE.

        """
        return objtype.value in make_iter(self.obj_type)

    def get_help(self):
        """
        Get help text for the item.

        Returns:
            str: The help text, by default taken from the `.help_text` property.

        """
        return "No help for this item."

    def at_pre_use(self, *args, **kwargs):
        """
        Called before use. If returning False, usage should be aborted.
        """
        return True

    def use(self, *args, **kwargs):
        """
        Use this object, whatever that may mean.

        """
        raise NotImplementedError

    def at_post_use(self, *args, **kwargs):
        """
        Called after use happened.
        """
        pass


class ObjContainer(ContribContainer):
    pass
