from evennia.contrib.game_systems.containers import ContribContainer
# from random import randint
# from evennia.prototypes import spawner


class Fountain(ContribContainer):

    fluid_type = ""

    def at_object_creation(self):
        super().at_object_creation()

        self.locks.add("get:false()")

    @property
    def is_liquid_container(self):
        return True

    def at_fill(self, chara, caller, **kwargs):
        """
        Creates the actual material object for the player to collect.
        """
        if not (proto_key := self.db.fluid_type):
            # Somehow this node has not material to spawn
            caller.msg(f"The {self.get_display_name(chara)} disappears in a puff of confusion.")
            # Get rid of ourself, since we're broken
            self.delete()
            return

        if not (remaining := self.db.volume_current):
            # This node has been used up
            caller.msg("There is nothing left.")
            # Get rid of ourself, since we're empty
            self.delete()
            return

        # Grab randomized amount to spawn
        # amt = randint(1, min(remaining, 3))
        amt = chara.db.volume_max - chara.db.volume_current

        chara.msg(amt)

        # Spawn the items!
        # objs = spawner.spawn(*[proto_key] * amt)
        # for obj in objs:
        #     # Move to the gathering character
        #     obj.location = chara

        if amt == remaining:
            caller.msg("You collect the last .")
            self.delete()
        else:
            caller.msg(f"You fill your {chara} with {self.db.fluid_type}.")
            self.db.volume_current -= amt
            chara.db.volume_current = chara.db.volume_max
            chara.db.fluid_type = self.db.fluid_type
