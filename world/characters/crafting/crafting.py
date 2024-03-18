from random import randint
from evennia.contrib.game_systems.crafting import CraftingRecipe
from evennia.contrib.game_systems.crafting import craft
from evennia.contrib.game_systems.crafting import CmdCraft

from evennia.utils.utils import (
    inherits_from,
)

"""Spawn Protoypes with quality

e.g. spawn {"prototype_parent": "IRON_PICKAXE", "quality": "Rare"}

Will generate an Iron Pickaxe with Rare quality

Returns:
    _type_: _description_
"""


class CmdCraftNew(CmdCraft):
    """
    Craft an item using ingredients and tools

    Usage:
      craft <recipe> [from <ingredient>,...] [using <tool>, ...]

    Examples:
      craft snowball from snow
      craft puppet from piece of wood using knife
      craft bread from flour, butter, water, yeast using owen, bowl, roller
      craft fireball using wand, spellbook

    Notes:
        Ingredients must be in the crafter's inventory. Tools can also be
        things in the current location, like a furnace, windmill or anvil.

    """

    def func(self):
        """
        Perform crafting.

        Will check the `craft` locktype. If a consumable/ingredient does not pass
        this check, we will check for the 'crafting_consumable_err_msg'
        Attribute, otherwise will use a default. If failing on a tool, will use
        the `crafting_tool_err_msg` if available.

        """
        caller = self.caller

        if not self.args or not self.recipe:
            self.caller.msg("Usage: craft <recipe> from <ingredient>, ... [using <tool>,...]")
            return

        if self.recipe not in caller.db.learned_recipes:
            self.caller.msg(f"You do not know the recipe for {self.recipe}.")
            return

        ingredients = []
        for ingr_key in self.ingredients:
            if not ingr_key:
                continue
            obj = caller.search(ingr_key, location=self.caller)
            # since ingredients are consumed we need extra check so we don't
            # try to include characters or accounts etc.
            if not obj:
                return
            if (
                not inherits_from(obj, "evennia.objects.models.ObjectDB") or obj.sessions.all() or not obj.access(caller, "craft", default=True)
            ):
                # We don't allow to include puppeted objects nor those with the
                # 'negative' permission 'nocraft'.
                caller.msg(
                    obj.attributes.get(
                        "crafting_consumable_err_msg",
                        default=f"{obj.get_display_name(looker=caller)} can't be used for this.",
                    )
                )
                return
            ingredients.append(obj)

        tools = []
        for tool_key in self.tools:
            if not tool_key:
                continue
            # tools are not consumed, can also exist in the current room
            obj = caller.search(tool_key)
            if not obj:
                return None
            if not obj.access(caller, "craft", default=True):
                caller.msg(
                    obj.attributes.get(
                        "crafting_tool_err_msg",
                        default=f"{obj.get_display_name(looker=caller)} can't be used for this.",
                    )
                )
                return
            tools.append(obj)

        # perform craft and make sure result is in inventory
        # (the recipe handles all returns to caller)
        result = craft(caller, self.recipe, *(tools + ingredients))
        if result:
            for obj in result:
                obj.location = caller


class SkillRecipe(CraftingRecipe):
    """
    The base recipe class for implementing skill checks, modified from the example:

    https://www.evennia.com/docs/latest/Contribs/Contrib-Crafting.html#skilled-crafters
    """

    # The skill requirement for the recipe.
    skill = (None, 0)
    exp_gain = 0

    def craft_xp_gain(self):
        req_skill, difficulty = self.skill

        if self.exp_gain:
            self.crafter.skills[req_skill].xp += self.exp_gain

    def craft(self, **kwargs):
        """The input is ok. Determine if crafting succeeds"""

        # this is set at initialization
        crafter = self.crafter

        # let's assume the skill is stored directly on the crafter
        # - the skill is 0..100.
        # get our skill requirements
        req_skill, difficulty = self.skill

        # if no requirement is set, just craft
        if not req_skill or not difficulty:
            self.craft_xp_gain()
            return super().craft(**kwargs)

        # otherwise, retrieve the skill from the crafter
        crafting_skill = crafter.skills.get(req_skill)
        # if crafter doesn't have the skill
        if not crafting_skill:
            self.msg("You don't know how to make this.")
            return
        # if crafter just isn't good enough
        elif crafting_skill.value < difficulty:
            self.msg(
                "You are not good enough to make this yet. Better keep practicing!"
            )
            return

        success_rate = crafting_skill.value - difficulty

        # at this point the crafting attempt is considered happening, so subtract mental focus
        # crafter.traits.fp.current -= 5
        # you should get the experience reward regardless of success
        # implement some randomness - the higher the difference, the lower the chance of failure
        if not randint(0, success_rate):
            self.msg("It doesn't seem to work out. Maybe you should try again?")
            return

        # all is good, craft away
        return super().craft(**kwargs)
