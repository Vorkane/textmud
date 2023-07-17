from typeclasses.objects import Object
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject

class OreNode(ContribRPObject):
    def at_object_creation(self):
        self.db.ore_type = "iron"  # You can change this to other ore types
        self.db.respawn_time = 5  # Respawn time in seconds (e.g., 3600 seconds = 1 hour)
        self.db.is_mineable = True
