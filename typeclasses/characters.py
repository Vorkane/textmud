"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
#from evennia.objects.objects import DefaultCharacter
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPCharacter
from evennia.typeclasses.attributes import AttributeProperty, NAttributeProperty
from evennia.utils.evform import EvForm
from evennia.utils.evtable import EvTable
from evennia.utils.logger import log_trace
from evennia.utils.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler

from world.characters.classes import CharacterClasses
from world.characters.races import Races

from .objects import ObjectParent


class Character(ContribRPCharacter):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_post_move(source_location) - Launches the "look" command after every move.
    at_post_unpuppet(account) -  when Account disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Account has disconnected"
                    to the room.
    at_pre_puppet - Just before Account re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "AccountName has entered the game" to the room.

    """

    def at_pre_move(self, destination, **kwargs):
        """
        Called by self.move_to when trying to move somewhere. If this returns
        False, the move is immediately cancelled.
        """
        if self.db.is_sitting:
            self.msg("You need to stand up first.")
            return False
        return True

    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self)
    
    @lazy_property
    def stats(self):
        # this adds the handler as .stats
        return TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def skills(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="skills")
    
    @lazy_property
    def proficiencies(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="proficiencies")
    
    def at_object_creation(self):
        self.skills.add("hunting", "Hunting Skill", trait_type="counter", base=10, mod=1, min=0, max=100)
        self.skills.add("Prowl", "Prowl Skill", trait_type="counter", base=10, mod=1, min=0, max=100)

        # Add proficiencies
        self.proficiencies.add("sword", "Sword Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("dagger", "Dagger Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("spear", "Spear Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("axe", "Axe Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("blunt", "Blunt Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("archery", "Archery Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        self.proficiencies.add("throwing", "Throwing Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})

    is_pc = True

    # these are the ability bonuses. Defense is always 10 higher
    strength = AttributeProperty(default=1) #brawn
    dexterity = AttributeProperty(default=1) #deftness or nimbleness
    constitution = AttributeProperty(default=1) #vitality
    intelligence = AttributeProperty(default=1) #brilliance
    wisdom = AttributeProperty(default=1) #insight
    charisma = AttributeProperty(default=1) #allure

    cclass_key =  AttributeProperty()
    race_key = AttributeProperty()

    hp = AttributeProperty(default=4)
    hp_max = AttributeProperty(default=4)
    mana = AttributeProperty(default=4)
    mana_max = AttributeProperty(default=4)
    stamina = AttributeProperty(default=2)
    stamina_max = AttributeProperty(default=4)


    level = AttributeProperty(default=1)  # Just a bragging stat, for now.
    coins = AttributeProperty(default=0)  # copper coins

    totalxp = AttributeProperty(default=1)
    currentxp = AttributeProperty = 1
    pri_xp_tnl = AttributeProperty = 1000
    
    @lazy_property
    def pri_class(self):
        pri_class = self.ndb.pri_class
        if pri_class is None:
            pri_class = CharacterClasses.get(self.db.pri_class_key)
            self.ndb.pri_class = pri_class

        return pri_class

    @lazy_property
    def race(self):
        race = self.ndb.race
        if race is None:
            race = Races.get(self.db.race_key)
            self.ndb.race = race

        return race

    pass
