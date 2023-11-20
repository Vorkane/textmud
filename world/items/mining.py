from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPObject
import evennia
from typeclasses.objects import Object
from random import randint
from evennia.prototypes import spawner, prototypes
from world.commands.professions.blacksmithing import MineCmdSet
from evennia import create_object
from evennia.prototypes.spawner import spawn
from icecream import ic


class OreGatherNode(ContribRPObject):
    """
    An object which, when mined, allows players to gather a material resource.
    """
    is_mineable = True
    req_material = ""

    def at_object_creation(self):
        self.locks.add("get:false()")
        self.db.is_mineable = self.is_mineable
        self.db.req_material = self.req_material
        #self.cmdset.add(MineCmdSet)

    def get_display_footer(self, looker, **kwargs):
        return "You can |wgather|n from this."
    
    def at_gather(self, chara, **kwargs):
        """
        Creates the actual material object for the player to collect.
        """
        if not (proto_key := self.db.spawn_proto):
            # Somehow this node has not material to spawn
            chara.msg(f"The {self.get_display_name(chara)} disappears in a puff of confusion.")
            # Get rid of ourself, since we're broken
            self.delete()
            return
        
        if not (remaining := self.db.gathers):
            # This node has been used up
            chara.msg(f"There is nothing left.")
            # Get rid of ourself, since we're empty
            self.delete()
            return
        
        # Grab randomized amount to spawn
        amt = randint(1, min(remaining, 3))

        # Spawn the items!
        objs = spawner.spawn(*[proto_key] * amt)
        for obj in objs:
            # Move to the gathering character
            obj.location = chara
        
        if amt == remaining:
            chara.msg(f"You collect the last {obj.get_numbered_name(amt, chara)[1]}.")
            self.delete()
        else:
            chara.msg(f"You collect {obj.get_numbered_name(amt, chara)[1]}.")
            self.db.gathers -= amt


class OreNode(ContribRPObject):
    """
    Typeclass for Ore Node Objects.
    Attributes:
        ore_type (string): type of ore for the node
        respawn_time (int): time in seconds for the node to respawn (e.g., 3600 = 1 hour)
        is_mineable (boolean): boolean if the node is available to mine
    """
    def at_object_creation(self):
        super(OreNode, self).at_object_creation()
        self.db.ore_type = self.ore_type
        self.db.respawn_time = self.respawn_time
        self.db.is_mineable = self.is_mineable

    ore_type = ""
    respawn_time = 0
    is_mineable = True

class Ore(ContribRPObject):
    """
    Typeclass for Ore Objects.
    Attributes:
        value (int): monetary value
        weight (float): weight of the item

    """
    def at_object_creation(self):
        super(Ore, self).at_object_creation()
        self.db.value = self.value
        self.db.weight = float(self.weight)
        self.db.bundle_size = 999
        self.db.quantity = 1
        self.db.prototype_name = None
        self.db.is_stackable = False
    
    quantity = 1
    value = 0
    weight = 0.0
    
    def at_get(self, getter):
        super(Ore, self).at_get(getter)
        #stack_key = self.aliases.all()[0]
        stack_key = self.tags.all()[0]

        others_stacked = [obj for obj in getter.contents
                          if obj.is_typeclass('world.items.mining.Ore')
                          and stack_key in obj.tags.all()]
        
        getter.msg(f'others_stacked: {others_stacked}')

        if not others_stacked:
            getter.msg("Nothing Here")
        elif len(others_stacked) > 1:
            #getter.msg(ic(others_stacked[0]))
            getter.msg(f'others_stacked: {range(len(others_stacked))}')

            i = 0

            list_length = len(others_stacked)

            getter.msg(f'list_length: {list_length}')

            for i in range(list_length):

                getter.msg(f'current i value: {i}')
                getter.msg(f'current i quantity: {others_stacked[i].db.quantity}')
                getter.msg(f'current i bundle_size: {others_stacked[i].db.bundle_size}')


               
                if others_stacked[i].db.quantity < others_stacked[i].db.bundle_size:
                    getter.msg(f'inloop i quantity: {others_stacked[i].db.quantity}')
                    getter.msg(f'inloop i bundle_size: {others_stacked[i].db.bundle_size}')
                    if others_stacked[i].db.quantity == 1:
                        getter.msg(f'\tunder_limit_loop: {i} : Quantity = 1')
                        break
                    else:
                        others_stacked[i].db.quantity += 1
                        others_stacked[i].key = stack_key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
                        getter.msg(f'\tunder_limit_loop: {i}')
                        self.delete()
                        break                
                elif others_stacked[i].db.quantity >= others_stacked[i].db.bundle_size:
                    i += 1
                    # others_stacked[i].db.quantity = 1
                    # others_stacked[i].db.quantity += 1                
                    # others_stacked[i].key = stack_key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
                    getter.msg(f'\tover_limit_loop: {i}')
                    # self.delete()
                    # break
                elif others_stacked[i].db.quantity == 1:
                    getter.msg(f'\tFinal Else statement')
                    break
                
                    

            # while i in range(list_length):
            #     getter.msg(f'quantity: {others_stacked[i].db.quantity}')
            #     getter.msg(f'bundle_size: {others_stacked[i].db.bundle_size}')

            # if others_stacked[i].db.quantity >= others_stacked[i].db.bundle_size:                    
            #         getter.msg(others_stacked[i])
            #         #others_stacked[i].db.quantity = 1                    
            #         #others_stacked[i].key = self.key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
            #         getter.msg(f'\tover_limit_loop: {i}')
            # else:# others_stacked[i].db.quantity < others_stacked[i].db.bundle_size:
            #     others_stacked[i].db.quantity += 1
            #     others_stacked[i].key = self.key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
            #     getter.msg(f'\tunder_limit_loop: {i}')
            #     self.delete()



        #matching_item = getter.search(stack_key, candidates=getter.contents)

        #getter.msg(matching_item)
        #getter.msg(others_stacked)
        #getter.msg(ic(getter.contents))


        ###### Working stacking of items ######
        # others_stacked[i].db.quantity += 1
        # others_stacked[i].key = stack_key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
        # self.delete()

                # getter.msg(f'others_stacked len: {(len(others_stacked))}')
                # getter.msg(f'before increment: {i}')
                # while i <= len(others_stacked):
                #     getter.msg(f'others_stacked: {others_stacked}')
                #     getter.msg(f'before quantity: {others_stacked[i].db.quantity}')
                #     i += 1
                #     getter.msg(f'after increment: {i}')
                #     getter.msg(f'after quantity: {others_stacked[i].db.quantity}')
                #     others_stacked[i].db.quantity = 1                    
                #     others_stacked[i].key = stack_key + ' x{quantity} '.format(quantity=others_stacked[i].db.quantity)
                #     #self.delete()

        # if not matching_item:
        #     getter.msg("Nothing")
        # elif len(matching_item) > 1:
        #     getter.msg(ic(matching_item))
        #     matching_item.quantity += 1
        #     matching_item.key = matching_item.key + ' x{quantity} '.format(quantity=matching_item.quantity)

        # getter.msg(ic(stack_key))
        # others_stacked = [obj in getter.contents
        #                   if obj.is_typeclass('world.items.mining.Ore')
        #                   and stack_key in obj.aliases.all()]
        
        # getter.msg(ic(others_stacked))
        
        # if others_stacked:
        #     getter.msg(ic(others_stacked[0].key))
        #     others_stacked[0].db.quantity += 1
        #     others_stacked[0].db.key = '{item} x{quantity} '.format(item=stack_key, quantity=others_stacked[0].db.quantity)

        


    # def at_get(self, getter):
    #     super(Ore, self).at_get(getter)
    #     bundle_key = self.aliases.all()[0]
    #     getter.msg(ic(bundle_key))
        # others = [obj for obj in getter.contents
        #           if obj.is_typeclass('world.items.mining.Ore')
        #           and bundle_key in obj.aliases.all()]
    #     len_others=len(others)
    #     if len(others) >= self.db.bundle_size \
    #             and self.db.prototype_name and self.aliases.all():
            
    #         # we have enough to create a bundle

    #         bundle = create_object(
    #             typeclass='world.items.mining.OreBundle',
    #             key='a bundle of {item}s x{quantity} '.format(item=bundle_key, quantity=len_others),
    #             aliases=['bundle {}'.format(bundle_key)],
    #             location=self.location
    #         )
    #         bundle.db.desc = ("A bundle of {item}s held together "
    #                           "with a thin leather strap.").format(
    #             item=bundle_key
    #         )
    #         bundle.db.value = self.db.bundle_size * self.db.value
    #         bundle.db.weight = self.db.bundle_size * self.db.weight
    #         bundle.db.quantity = self.db.bundle_size
    #         bundle.db.prototype_name = self.db.prototype_name
    #         for obj in others[:self.db.bundle_size]:
    #             obj.delete()

class OreBundle(ContribRPObject):
    """Typeclass for bundles of Items."""
    def expand(self):
        """Expands a bundle into its component items."""
        for i in range(self.db.quantity):
            spawn(dict(prototype=self.db.prototype_name,
                       location=self.location))
        self.delete()