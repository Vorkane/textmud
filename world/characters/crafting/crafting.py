from random import randint
from evennia.contrib.game_systems.crafting import CraftingRecipe

"""Spawn Protoypes with quality

e.g. spawn {"prototype_parent": "IRON_PICKAXE", "quality": "Rare"}

Will generate an Iron Pickaxe with Rare quality

Returns:
    _type_: _description_
"""


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
