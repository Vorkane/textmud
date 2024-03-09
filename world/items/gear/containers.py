from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
from evennia.contrib.game_systems.containers import ContribContainer


class Bag(ContribContainer):

    # container_type = "bag"
    # weight_current = 0
    # weight_capacity = 2
    # weight_reduction = 0
    # item_limit = 2
    # current_item = 0
    pass


class Chest(ContribRPObject):
    """
    This class is for a container classified as a chest.
    A chest is an object that is placed on the floor and can be locked or shared.
    """
    container_type = "chest"
    weight_current = 0
    weight_capacity = 5
    weight_reduction = 0
    item_limit = 5
    current_item = 0


class Canteen(ContribRPObject):
    """
    This class is for a container classified as a canteen.
    A canteen is an object that contains liquids and is carried by the player.
    """

    fluid_type = ""
    volume_current = 0
    volume_max = 10

    @property
    def is_liquid_container(self):
        return True

    def get_display_footer(self, looker, **kwargs):
        if (self.db.volume_current == self.db.volume_max):
            return """This {container} is full of {fluid}""".format(container=self.name, fluid=self.db.fluid_type)
        if (self.db.volume_current == (self.db.volume_max * 0.5)):
            return """This {container} is half full of {fluid}""".format(container=self.name, fluid=self.db.fluid_type)
        if (self.db.volume_current <= 0):
            return """This {} is empty""".format(self.name)
