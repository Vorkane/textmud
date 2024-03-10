from .crafting import SkillRecipe


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
            "key": "iron ingot",
            "desc": "An ingot of iron.",
            "tags": [
                ("iron ingot", "crafting_material"),
                ("ingot", "crafting_material"),
            ],
            "value": 5,
        }
    ]
