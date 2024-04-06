from .crafting import SkillRecipe


class SmeltCopperRecipe(SkillRecipe):
    """
    Smelting iron ore into ingots
    """

    skill = ('BLACKSMITH', 0)
    exp_gain = 1

    name = "copper ingot"
    # tool_tags = ["furnace"]
    consumable_tags = ["copper ore", "copper ore"]
    output_prototypes = [
        {
            "prototype_parent": "COPPER_INGOT",
            "name": "copper ingot",
            "key": "copper ingot"
        }
    ]


class SmeltIronRecipe(SkillRecipe):
    """
    Smelting iron ore into ingots
    """

    skill = ('BLACKSMITH', 0)
    exp_gain = 1

    name = "iron ingot"
    # tool_tags = ["furnace"]
    consumable_tags = ["iron ore", "iron ore"]
    output_prototypes = [
        {
            "prototype_parent": "IRON_INGOT",
            "name": "iron ingot",
            "key": "iron ingot"
        }
    ]
