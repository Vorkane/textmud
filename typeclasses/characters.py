"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler
from evennia.server.sessionhandler import SESSIONS


from world.equip import EquipHandler


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
    'Thirst': {'trait_type': 'static', 'base': 100, 'max': 100, 'name': 'Thirst'},
    'Hunger': {'trait_type': 'static', 'base': 100, 'max': 100, 'name': 'Hunger'},
    # Misc
    'ENC': {'trait_type': 'static', 'base': 0, 'mod': 0, 'min': 0, 'name': 'Carry Weight'},
    'LV': {'trait_type': 'static', 'base': 1, 'mod': 0, 'max': 999, 'name': 'Level'},
    'XP': {'trait_type': 'counter', 'base': 0, 'mod': 0, 'name': 'Experience', 'extra': {'level_boundaries': (500, 2000, 4500, 'unlimited')}},
}

wield_slots = ['wield1', 'wield2']
armor_slots = ['helm', 'neck', 'cloak', 'torso', 'belt', 'bracers', 'gloves', 'ring1', 'ring2', 'boots']
clothing_slots = ['hat', 'accessory', 'overtop', 'bottom', 'belt2', 'accessory2', 'gloves2', 'accessory3', 'accessory4', 'shoes']


skills = {
    'BLACKSMITH': {'trait_type': 'static', 'base': 0, 'xp': 0, 'xptnl': 100, 'name': 'Blacksmithing'},
}

# self.skills.add("hunting", "Hunting Skill", trait_type="counter", base=10, mod=1, min=0, max=100)
# self.skills.add("Prowl", "Prowl Skill", trait_type="counter", base=10, mod=1, min=0, max=100)


class Character(DefaultCharacter):
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

    def get_display_desc(self, looker, **kwargs):
        """
        Get the 'desc' component of the object description. Called by `return_appearance`.

        Args:
            looker (Object): Object doing the looking.
            **kwargs: Arbitrary data for use when overriding.
        Returns:
            str: The desc display string.
        """
        desc = self.db.desc

        return desc

    def at_pre_move(self, destination, **kwargs):
        """
        Called by self.move_to when trying to move somewhere. If this returns
        False, the move is immediately cancelled.
        """
        if self.db.is_sitting:
            self.msg("You need to stand up first.")
            return False
        elif self.db.is_immobile:
            self.msg("You are immobile.")
            return False
        return True

    def announce_move_from(self, destination, msg=None, mapping=None, **kwargs):
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

    def announce_move_to(self, source_location, msg=None, mapping=None, **kwargs):
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
        self.db.currency_gold = 0
        self.db.learned_recipes = []

        for key, kwargs in stats.items():
            self.stats.add(key, **kwargs)

        for key, kwargs in skills.items():
            self.skills.add(key, **kwargs)

        self.stats.STR.carry_factor = 10
        self.stats.STR.lift_factor = 20
        self.stats.ENC.current = 0
        self.stats.XP.total = 0
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
        # self.location.msg_contents("%s has connected" % self.key)
        loginmsg = "\n\n[************--Rumour Monger--************]|/" \
                   "\t %s arrives in Orario.|/" \
                   "[*****************************************]|/" % self.key
        SESSIONS.announce_all(loginmsg)
        # tickerhandler.add(interval=randint(10, 15), callback=self.at_regen, persistent=True)
        self.execute_cmd("look")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('character:sheet', kwargs={'object_id': self.id})

    def at_object_receive(self, obj, source, **kwargs):
        if not obj.db.weight:
            return
        else:
            self.stats.ENC.current += obj.db.weight
            # self.traits.EP.mod = \
            #    int(-(self.traits.ENC.actual // (2 * self.traits.STR.actual)))

    def at_object_leave(self, obj, source, **kwargs):
        if not obj.db.weight:
            return
        else:
            self.stats.ENC.current -= obj.db.weight
            # self.traits.EP.mod = \
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
        # This adds the handler as .proficiencies
        return TraitHandler(self, db_attribute_key="proficiencies")

    @lazy_property
    def reputation(self):
        # This add the handler for .reputation
        return TraitHandler(self, db_attribute_key="reputation")

    @lazy_property
    def equip(self):
        """Handler for equipped items."""
        return EquipHandler(self)

    # def at_regen(self):
    #     self.stats.HP.current += int(floor(0.1 * self.stats.HP.max))
    #     self.stats.MP.current += int(floor(0.1 * self.stats.MP.max))
    #     self.stats.ST.current += int(floor(0.1 * self.stats.ST.max))

    race = AttributeProperty()


class Player(Character):

    is_pc = True

    pass


class NPC(Character):
    pass
