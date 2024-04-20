# Python Imports
import random

# Evennia Imports
from evennia.typeclasses.attributes import AttributeProperty
from evennia.typeclasses.tags import TagProperty
from evennia.utils.utils import lazy_property
from evennia import TICKER_HANDLER as tickerhandler

# Custom Imports
from .characters import LivingMixin
from .characters import Character
from world.rules import Ability
from core.misc.ai import AIHandler
from world.characters.races import Races2


class NPC(LivingMixin, Character):

    is_pc = False

    hp_max = AttributeProperty(default=1, autocreate=False)
    is_idle = AttributeProperty(default=False, autocreate=False)
    ai_state = AttributeProperty(default="idle", autocreate=False)

    # if this npc is attacked, everyone with the same tag in the current location will also be
    # pulled into combat.
    group = TagProperty("npcs")

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
        self.db.is_idle = self.is_idle
        self.db.slots = Races2.slots
        self.db.limbs = Races2.limbs
        self.ai_state = self.ai.get_state()
        # self.db.size = self.size

        tickerhandler.add(5, self.at_tick)
        # print(self.ai.get_state())

    def at_object_creation(self):
        super(NPC, self).at_object_creation()

        self.tags.add("npcs", category="group")

    def at_attacked(self, attacker, **kwargs):
        """
        Called when being attacked and combat starts.

        """
        pass

    def ai_next_action(self, **kwargs):
        """
        The combat engine should ask this method in order to
        get the next action the npc should perform in combat.

        """
        pass

    def at_tick(self):
        self.execute_cmd(f"say Testing AI Tick")
        self.ai.run()
        self.execute_cmd(f"say My State: {self.ai.get_state()}")


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
