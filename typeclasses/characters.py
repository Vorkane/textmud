"""
Characters

Characters are (by default) Objects setup to be puppeted by Accounts.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""

# from evennia.objects.objects import DefaultCharacter
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils.utils import lazy_property
from evennia.contrib.rpg.traits import TraitHandler
from evennia.server.sessionhandler import SESSIONS
from evennia.contrib.tutorials.evadventure import rules
from evennia import DefaultCharacter
import random

from world.equip import EquipHandler
from world.rules import Ability
from core.misc.ai import AIHandler


stats = {
    # Primary
    "STR": {"trait_type": "static", "base": 8, "mod": 0, "name": "Strength"},
    "END": {"trait_type": "static", "base": 8, "mod": 0, "name": "Endurance"},
    "DEX": {"trait_type": "static", "base": 8, "mod": 0, "name": "Dexterity"},
    "AGI": {"trait_type": "static", "base": 8, "mod": 0, "name": "Agility"},
    "MAG": {"trait_type": "static", "base": 8, "mod": 0, "name": "Magic"},
    "LUK": {"trait_type": "static", "base": 8, "mod": 0, "name": "Luck"},
    # Vitals
    "HP": {"trait_type": "static", "base": 8, "mod": 0, "name": "Health"},
    "MP": {"trait_type": "static", "base": 8, "mod": 0, "name": "Mana"},
    "ST": {"trait_type": "static", "base": 8, "mod": 0, "name": "Stamina"},
    "Thirst": {"trait_type": "static", "base": 100, "max": 100, "name": "Thirst"},
    "Hunger": {"trait_type": "static", "base": 100, "max": 100, "name": "Hunger"},
    # Misc
    "ENC": {
        "trait_type": "static",
        "base": 0,
        "mod": 0,
        "min": 0,
        "name": "Carry Weight",
    },
    "LV": {"trait_type": "static", "base": 1, "mod": 0, "max": 999, "name": "Level"},
    "XP": {
        "trait_type": "counter",
        "base": 0,
        "mod": 0,
        "name": "Experience",
        "extra": {"level_boundaries": (500, 2000, 4500, "unlimited")},
    },
    # Combat
    "PATK": {
        "trait_type": "static",
        "base": 0,
        "mod": 0,
        "min": 0,
        "name": "Physical Attack",
    },
    "PDEF": {
        "trait_type": "static",
        "base": 0,
        "mod": 0,
        "min": 0,
        "name": "Physical Defense",
    },
}

wield_slots = ["wield1", "wield2"]
armor_slots = [
    "helm",
    "neck",
    "cloak",
    "torso",
    "belt",
    "bracers",
    "gloves",
    "ring1",
    "ring2",
    "boots",
]
clothing_slots = [
    "hat",
    "accessory",
    "overtop",
    "bottom",
    "belt2",
    "accessory2",
    "gloves2",
    "accessory3",
    "accessory4",
    "shoes",
]


skills = {
    "BLACKSMITHING": {
        "trait_type": "static",
        "base": 0,
        "xp": 0,
        "xptnl": 100,
        "name": "Blacksmithing",
    },
}

# self.skills.add("hunting", "Hunting Skill", trait_type="counter", base=10, mod=1, min=0, max=100)
# self.skills.add("Prowl", "Prowl Skill", trait_type="counter", base=10, mod=1, min=0, max=100)


class LivingMixin:
    """
    Mixin class to use for all living things.

    """

    is_pc = False

    @property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """
        percent = max(0, min(100, 100 * (self.stats.HP.current / self.stats.HP.max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        elif 80 < percent <= 95:
            return "|gScraped|n"
        elif 60 < percent <= 80:
            return "|GBruised|n"
        elif 45 < percent <= 60:
            return "|yHurt|n"
        elif 30 < percent <= 45:
            return "|yWounded|n"
        elif 15 < percent <= 30:
            return "|rBadly wounded|n"
        elif 1 < percent <= 15:
            return "|rBarely hanging on|n"
        elif percent == 0:
            return "|RCollapsed!|n"

    def heal(self, hp, healer=None):
        """
        Heal by a certain amount of HP.

        """
        damage = self.stats.HP.max - self.stats.HP.current
        healed = min(damage, hp)
        self.stats.HP.current += healed

        if healer is self:
            self.msg(f"|gYou heal yourself for {healed} health.|n")
        elif healer:
            self.msg(f"|g{healer.key} heals you for {healed} health.|n")
        else:
            self.msg(f"You are healed for {healed} health.")

    def at_attacked(self, attacker, **kwargs):
        """
        Called when being attacked / combat starts.

        """
        pass

    def at_damage(self, damage, attacker=None):
        """
        Called when attacked and taking damage.

        """
        self.stats.HP.current -= damage

    def at_defeat(self):
        """
        Called when this living thing reaches HP 0.

        """
        # by default, defeat means death
        self.at_death()

    def at_death(self):
        """
        Called when this living thing dies.

        """
        pass

    def at_pay(self, amount):
        """
        Get coins, but no more than we actually have.

        """
        amount = min(amount, self.coins)
        self.coins -= amount
        return amount

    def at_looted(self, looter):
        """
        Called when being looted (after defeat).

        Args:
            looter (Object): The one doing the looting.

        """
        max_steal = rules.dice.roll("1d10")
        stolen = self.at_pay(max_steal)

        looter.coins += stolen

        self.location.msg_contents(
            f"$You(looter) loots $You() for {stolen} coins!",
            from_obj=self,
            mapping={"looter": looter},
        )

    def pre_loot(self, defeated_enemy):
        """
        Called just before looting an enemy.

        Args:
            defeated_enemy (Object): The enemy soon to loot.

        Returns:
            bool: If False, no looting is allowed.

        """
        pass

    def at_do_loot(self, defeated_enemy):
        """
        Called when looting another entity.

        Args:
            defeated_enemy: The thing to loot.

        """
        defeated_enemy.at_looted(self)

    def post_loot(self, defeated_enemy):
        """
        Called just after having looted an enemy.

        Args:
            defeated_enemy (Object): The enemy just looted.

        """
        pass


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
        exits = [
            o
            for o in location.contents
            if o.location is location and o.destination is destination
        ]
        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self,
                "exit": exits[0] if exits else "somwhere",
                "origin": location or "nowhere",
                "destination": destination or "nowhere",
            }
        )

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
            string = (
                "You now have %s in your possession."
                % self.get_extra_display_name_info(self.location)
            )
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
            exits = [
                o
                for o in destination.contents
                if o.location is destination and o.destination is origin
            ]

        if not mapping:
            mapping = {}

        mapping.update(
            {
                "object": self,
                "exit": exits[0] if exits else "somewhere",
                "origin": origin or "nowhere",
                "destination": destination or "nowhere",
            }
        )

        destination.msg_contents(string, exclude=(self,), mapping=mapping)

    def at_object_creation(self):

        super(Character, self).at_object_creation()

        self.db.gender = "ambiguous"
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

    def at_post_puppet(self):
        # self.location.msg_contents("%s has connected" % self.key)
        loginmsg = (
            "\n\n[************--Rumour Monger--************]|/"
            "\t %s arrives in Orario.|/"
            "[*****************************************]|/" % self.key
        )
        SESSIONS.announce_all(loginmsg)
        # tickerhandler.add(interval=randint(10, 15), callback=self.at_regen, persistent=True)
        self.execute_cmd("look")

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("character:sheet", kwargs={"object_id": self.id})

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


class Player(LivingMixin, Character):

    is_pc = True

    def at_object_creation(self):
        super(Player, self).at_object_creation()
        self.tags.add("player", category="group")


class NPC(LivingMixin, Character):

    is_pc = False

    hp_max = AttributeProperty(default=1, autocreate=False)

    @property
    def hurt_level(self):
        """
        String describing how hurt this character is.
        """
        # percent = max(0, min(100, 100 * (self.hp / self.hp_max)))
        percent = max(0, min(100, 100 * (self.stats.HP.current / self.stats.HP.max)))
        if 95 < percent <= 100:
            return "|gPerfect|n"
        elif 80 < percent <= 95:
            return "|gScraped|n"
        elif 60 < percent <= 80:
            return "|GBruised|n"
        elif 45 < percent <= 60:
            return "|yHurt|n"
        elif 30 < percent <= 45:
            return "|yWounded|n"
        elif 15 < percent <= 30:
            return "|rBadly wounded|n"
        elif 1 < percent <= 15:
            return "|rBarely hanging on|n"
        elif percent == 0:
            return "|RCollapsed!|n"

    def basetype_posthook_setup(self):

        self.stats.HP.max = self.hp_max
        self.stats.HP.current = self.stats.HP.max

    def at_object_creation(self):
        super(NPC, self).at_object_creation()

        self.tags.add("npcs", category="group")


class Mob(NPC):
    """
    Mob (mobile) NPC; this is usually an enemy.

    """

    # change this to make the mob more or less likely to perform different actions
    combat_probabilities = {
        "hold": 0.0,
        "attack": 0.85,
        "stunt": 0.05,
        "item": 0.0,
        "flee": 0.05,
    }

    @lazy_property
    def ai(self):
        return AIHandler(self)

    def ai_idle(self):
        """
        Do nothing.

        """
        pass

    def ai_combat(self):
        """
        Manage the combat/combat state of the mob.

        """
        if combathandler := self.nbd.combathandler:
            # already in combat
            allies, enemies = combathandler.get_sides(self)
            action = self.ai.random_probability(self.combat_probabilities)

            match action:
                case "hold":
                    combathandler.queue_action({"key": "hold"})
                case "combat":
                    combathandler.queue_action(
                        {"key": "attack", "target": random.choice(enemies)}
                    )
                case "stunt":
                    # choose a random ally to help
                    combathandler.queue_action(
                        {
                            "key": "stunt",
                            "recipient": random.choice(allies),
                            "advantage": True,
                            "stunt": Ability.STR,
                            "defense": Ability.DEX,
                        }
                    )
                case "item":
                    # use a random item on a random ally
                    target = random.choice(allies)
                    valid_items = [
                        item for item in self.contents if item.at_pre_use(self, target)
                    ]
                    combathandler.queue_action(
                        {
                            "key": "item",
                            "item": random.choice(valid_items),
                            "target": target,
                        }
                    )
                case "flee":
                    self.ai.set_state("flee")

        elif not (targets := self.ai.get_targets()):
            self.ai.set_state("roam")
        else:
            target = random.choice(targets)
            self.execute_cmd(f"attack {target.key}")

    def ai_roam(self):
        """
        roam, moving randomly to a new room. If a target is found, switch to combat state.

        """
        if targets := self.ai.get_targets():
            self.ai.set_state("combat")
            self.execute_cmd(f"attack {random.choice(targets).key}")
        else:
            exits = self.ai.get_traversable_exits()
            if exits:
                exi = random.choice(exits)
                self.execute_cmd(f"{exi.key}")

    def ai_flee(self):
        """
        Flee from the current room, avoiding going back to the room from which we came. If no exits
        are found, switch to roam state.

        """
        current_room = self.location
        past_room = self.attributes.get("past_room", category="ai_state", default=None)
        exits = self.ai.get_traversable_exits(exclude_destination=past_room)
        if exits:
            self.attributes.set("past_room", current_room, category="ai_state")
            exi = random.choice(exits)
            self.execute_cmd(f"{exi.key}")
        else:
            # if in a dead end, roam will allow for backing out
            self.ai.set_state("roam")

    # def at_death(self):
    #     """
    #     Called when this living thing dies.

    #     """
    #     self.delete()

    def at_defeat(self):
        """
        Mobs die right away when defeated, no death-table rolls.

        """
        self.at_death()
