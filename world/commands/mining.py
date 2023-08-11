from evennia import Command, create_object
from evennia.utils import delay

class CmdMine(Command):
    key = "mine"
    help_category = "Mining"

    def func(self):
        caller = self.caller
        location = caller.location

        # Check if the player is in a location with mineable ore nodes
        mineable_nodes = [obj for obj in location.contents if obj.db.is_mineable]
        if not mineable_nodes:
            caller.msg("There are no mineable ore nodes here.")
            return

        # Assuming a player can mine only one node at a time, choose the first node found
        ore_node = mineable_nodes[0]

        # Check if the ore node is ready to be mined
        if ore_node.ndb.mined:
            caller.msg("This ore node has already been mined and will respawn soon.")
            return

        # Mining process (you can customize this based on your game mechanics)
        ore_type = ore_node.db.ore_type
        mined_ore_amount = 1  # Change this to the amount of ore the player receives per mining action

        # Add the mined ore to the player's inventory
        # Assuming you have an inventory system in place
        caller.msg(f"You mine {mined_ore_amount} {ore_type} ore.")

        # Create the ore object and place it in the player's inventory
        """ ore_object = create_object(
            typeclass="typeclasses.orenodes.OreNode",
            key=f"{ore_type} ore",
            location=caller,
            home=caller,
        ) """

        if ore_type == "iron":
            ore_object = create_object(
                typeclass="world.items.mining.IronOre",
                key=f"{ore_type} ore",
                location=caller,
                home=caller
            )
        elif ore_type == "copper":
            ore_object = create_object(
                typeclass="world.items.mining.CooperOre",
                key=f"{ore_type} ore",
                location=caller,
                home=caller
            )
        caller.msg(f"{mined_ore_amount} {ore_type} ore added to your inventory.")


        #caller.db.iron += 1
        # Add mined_ore_amount of ore to the player's inventory here

        # Mark the ore node as mined and schedule its respawn
        ore_node.ndb.mined = True
        delay(ore_node.db.respawn_time, self.reset_mine_status, ore_node)

    def reset_mine_status(self, ore_node):
        ore_node.ndb.mined = False
        self.caller.msg(f"The {ore_node.db.ore_type} ore node has respawned and is ready to be mined again.")
