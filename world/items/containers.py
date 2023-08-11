from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject




class Bag(ContribRPObject):
    """
    This class is for a container classified as a bag.
    A bag is an object that can be equipped and/or carried on the player.
    """
    container_type = "bag"
    weight_current = 0
    weight_capacity = 2
    weight_reduction = 0
    item_limit = 2
    current_item = 0

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

    def at_object_creation(self):

        super().at_object_creation()

        self.db.container_type = "canteen"
        self.db.volume_current = 0
        self.db.volume_capacity = 10
        self.db.fluid_type = ""

    def do_fillable(self, fluid):
        """
        Called when trying to fill this object.

        Args:
            canteen (Object): The object being filled.
        """
        
        if self.db.fluid_type != fluid.fluid_type:
            self.caller.msg(f"The liquid in your container is not the same.")
            return False
        return True

    def fill_canteen(self, fluid):

        if self.do_fillable(fluid):
            fluid.move_to(self, quite=True)
            move_to_volume = (self.db.volume_capacity - self.db.volume_current)
            self.db.volume_current = self.db.volume_capacity
            fluid.db.volume_current -= move_to_volume
            return True
        return False
        