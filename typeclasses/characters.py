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

from evennia.contrib.rpg.health_bar import display_meter
from math import floor
from evennia import TICKER_HANDLER as tickerhandler
from evennia.server.sessionhandler import SESSIONS
from random import randint

# Custom World Classes
from world.characters.races import Races
from world.characters.races import Races2

from world.equip import EquipHandler

from .objects import ObjectParent

stats = {
    # Primary
    'STR': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Strength'},
    'END': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Endurance'},
    'DEX': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Dexterity'},
    'AGI': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Agility'},
    'MAG': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Magic'},
    'LUK': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Luck'},
    # Vitals
    'HP': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Health'},
    'MP': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Mana'},
    'ST': {'trait_type': 'static', 'base': 8, 'mod': 0, 'name': 'Stamina'},
    # Misc
    'ENC': {'trait_type': 'counter', 'base': 0, 'mod': 0, 'min': 0, 'name': 'Carry Weight'},
    'LV': {'trait_type': 'static', 'base': 1, 'mod': 0, 'name': 'Level'},
    'XP': {'trait_type': 'counter', 'base': 0, 'mod': 0, 'name': 'Experience', 'extra': {'level_boundaries': (500, 2000, 4500, 'unlimited')}},
}

wield_slots = ['wield1', 'wield2']
armor_slots = ['helm', 'neck', 'cloak', 'torso', 'belt', 'bracers', 'gloves', 'ring1', 'ring2', 'boots']
clothing_slots = ['hat', 'accessory', 'overtop', 'bottom', 'belt2', 'accessory2', 'gloves2', 'accessory3', 'accessory4', 'shoes']





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
    
    def announce_move_from(self, destination, msg=None, mapping=None):
        """
        Called if the move is to be announced. This is
        called while we are still standing in the old
        location.

        Args:
            destination (Object): The place we are going to.
            msg (str, optional): a replacement message.
            mapping (dict, optional): additional mapping objects.

        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.

        """
        if not self.location:
            return
        if msg:
            string = msg
        else:
            string = "{object} leaves {exit}."

        location = self.location
        exits = [o for o in location.contents if o.location is location and o.destination is destination]
        if not mapping:
            mapping = {}

        mapping.update({
            "object": self,
            "exit": exits[0] if exits else "somwhere",
            "origin": location or "nowhere",
            "destination": destination or "nowhere",
        })

        location.msg_contents(string, exclude=(self,), mapping=mapping)

    def announce_move_to(self, source_location, msg=None, mapping=None):
        """
        Called after the move if the move was not quiet. At this point
        we are standing in the new location.

        Args:
            source_location (Object): The place we came from
            msg (str, optional): the replacement message if location.
            mapping (dict, optional): additional mapping objects.

        You can override this method and call its parent with a
        message to simply change the default message.  In the string,
        you can use the following as mappings (between braces):
            object: the object which is moving.
            exit: the exit from which the object is moving (if found).
            origin: the location of the object before the move.
            destination: the location of the object after moving.

        """

        if not source_location and self.location.has_account:
            # This was created from nowhere and added to an account's
            # inventory; it's probably the result of a create command.
            string = "You now have %s in your possession." % self.get_display_name(self.location)
            self.location.msg(string)
            return

        if source_location:
            if msg:
                string = msg
            else:
                string = "{object} arrives from the {exit}."
        else:
            string = "{object} arrives to {destination}."

        origin = source_location
        destination = self.location
        exits = []
        if origin:
            exits = [o for o in destination.contents if o.location is destination and o.destination is origin]

        if not mapping:
            mapping = {}

        mapping.update({
            "object": self,
            "exit": exits[0] if exits else "somewhere",
            "origin": origin or "nowhere",
            "destination": destination or "nowhere",
        })

        destination.msg_contents(string, exclude=(self,), mapping=mapping)
    
    def at_object_creation(self):

        super(Character, self).at_object_creation()

        self.db.gender = 'ambiguous'
        self.db.title = ""
        self.db.race = "Human"
        self.db.permadeath = False
        self.db.wallet = {'PP': 0, 'GP': 0, 'SP': 0, 'CP': 0}

        for key, kwargs in stats.items():
            self.stats.add(key, **kwargs)


        self.stats.STR.carry_factor = 10
        self.stats.STR.lift_factor = 20
        self.stats.ENC.current = 0
        self.stats.ENC.max = self.stats.STR.lift_factor * self.stats.STR


        # self.skills.add("hunting", "Hunting Skill", trait_type="counter", base=10, mod=1, min=0, max=100)
        # self.skills.add("Prowl", "Prowl Skill", trait_type="counter", base=10, mod=1, min=0, max=100)

        # # Add proficiencies
        # self.proficiencies.add("sword", "Sword Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("dagger", "Dagger Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("spear", "Spear Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("axe", "Axe Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("blunt", "Blunt Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("archery", "Archery Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})
        # self.proficiencies.add("throwing", "Throwing Proficiency", trait_type="counter", base=5, mod=0, min=0, max=100, descs={0: "unskilled", 10: "neophyte", 50: "trained", 70: "expert", 90: "master"})

    def at_post_puppet(self):
        #self.location.msg_contents("%s has connected" % self.key)
        loginmsg = "\n\n[************--Rumour Monger--************]|/" \
                   "\t %s arrives in Orario.|/" \
                   "[*****************************************]|/" % self.key
        SESSIONS.announce_all(loginmsg)
        tickerhandler.add(interval=randint(10, 15), callback=self.at_regen, persistent=True)
        self.execute_cmd("look")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('character:sheet', kwargs={'object_id':self.id})
    
    def at_object_receive(self, obj, source):
        if not obj.db.weight:
            return
        else:
            self.traits.ENC.current += obj.db.weight
            #self.traits.EP.mod = \
            #    int(-(self.traits.ENC.actual // (2 * self.traits.STR.actual)))

    def at_object_leave(self, obj, source):
        if not obj.db.weight:
            return
        else:
            self.traits.ENC.current -= obj.db.weight
            #self.traits.EP.mod = \
            #    int(+(self.traits.ENC.actual // (2 * self.traits.STR.actual)))

    @lazy_property
    def stats(self):
        # this adds the handler as .stats
        return TraitHandler(self, db_attribute_key="stats")

    @lazy_property
    def traits(self):
        # this adds the handler as .traits
        return TraitHandler(self, db_attribute_key="traits")

    @lazy_property
    def skills(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="skills")
    
    @lazy_property
    def proficiencies(self):
        # this adds the handler as .skills
        return TraitHandler(self, db_attribute_key="proficiencies")    
    
    is_pc = True

    @lazy_property
    def equip(self):
        """Handler for equipped items."""
        return EquipHandler(self)

    def at_regen(self):
        self.traits.HP.current += int(floor(0.1 * self.traits.HP.max))
        self.traits.MP.current += int(floor(0.1 * self.traits.MP.max))
        self.traits.ST.current += int(floor(0.1 * self.traits.ST.max))


    # these are the ability bonuses. Defense is always 10 higher
    # strength = AttributeProperty(default=1) #brawn
    # endurance = AttributeProperty(default=1)
    # dexterity = AttributeProperty(default=1) #deftness or nimbleness
    # agility = AttributeProperty(default=1) #vitality
    # magic = AttributeProperty(default=1) #brilliance
    # luck = AttributeProperty(default=1) #insight

    # cclass_key =  AttributeProperty()
    race = AttributeProperty()

    hp = AttributeProperty(default=4)
    hp_max = AttributeProperty(default=4)
    mana = AttributeProperty(default=4)
    mana_max = AttributeProperty(default=4)
    stamina = AttributeProperty(default=2)
    stamina_max = AttributeProperty(default=4)

    # Resources
    copper = AttributeProperty(default=0)
    iron = AttributeProperty(default=0)


    level = AttributeProperty(default=1)  # Just a bragging stat, for now.
    coins = AttributeProperty(default=0)  # copper coins

    totalxp = AttributeProperty(default=1)
    currentxp = AttributeProperty = 1
    pri_xp_tnl = AttributeProperty = 1000
    
    # @lazy_property
    # def pri_class(self):
    #     pri_class = self.ndb.pri_class
    #     if pri_class is None:
    #         pri_class = CharacterClasses.get(self.db.pri_class_key)
    #         self.ndb.pri_class = pri_class

    #     return pri_class

    # @lazy_property
    # def race(self):
    #     race = self.ndb.race
    #     if race is None:
    #         race = Races.get(self.db.race)
    #         self.ndb.race = race

    #     return race

    # pass
