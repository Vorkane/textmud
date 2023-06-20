from evennia.contrib.rpg.traits import StaticTrait

class RageTrait(StaticTrait):

    trait_type = "rage"
    default_keys = {
        "rage": 0
    }

    def berserk(self):
        self.mod = 100

    def sedate(self):
        self.mod = 0