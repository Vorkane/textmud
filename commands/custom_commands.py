from evennia import default_cmds, CmdSet
from evennia.commands.command import Command
from commands.base import DanMachiCommand
from evennia.utils.evform import EvForm
from evennia.contrib.game_systems.containers.containers import CmdContainerLook
from evennia.utils import utils
from evennia.contrib.rpg.health_bar import display_meter
from typeclasses.characters import wield_slots
from typeclasses.characters import armor_slots
from typeclasses.characters import clothing_slots

import math

class CmdSheet(DanMachiCommand):

    key = "sheet"
    aliases = ["sh"]
    locks = "cmd:all()"

    def func(self):

        #if len(self.caller.traits.all) == 0:
        #    return
        
        form = EvForm('world.commands.templates.charsheet', align='l')
        fields = {
            'A': self.caller.name,
            'B': self.caller.db.title,
            'C': self.caller.db.race,
            'L': self.caller.stats.STR.base,
            'M': self.caller.stats.END.base,
            'N': self.caller.stats.DEX.base,
            'O': self.caller.stats.AGI.base,
            'P': self.caller.stats.MAG.base,
            'Q': self.caller.stats.LUK.base,
        }
        form.map({k: self._format_trait_val(v) for k, v in fields.items()})

        self.caller.msg(str(form))
    
    def _format_trait_val(self, val):
        """Format trait values as bright white."""
        return "|w{}|n".format(val)



class CmdStatus(DanMachiCommand):
    key = "status"
    aliases = "score"

    def func(self):

        _CHAR_STATUS  = (
        f"\n\n"
        f"{'< Details >':=^80}\n"
        f"{'|CName:|w':10}{self.caller.name:25}\n"
        f"{'|CRace:|w':10}{self.caller.race:20}{'|CGender:|w':12}Male{'':16}|n\n"
        f"{'< Vitals >':=^80}\n"
        f"{'|CHealth:|w' : <12}{self.caller.stats.HP.current}{'|W('}{self.caller.stats.HP.max}{')|n' : <10}{'|CMana:|w' : <10}{self.caller.mana}{'|W('}{self.caller.mana_max}{')|n' : <10}{'|CStamina:|w' : <13}{(2 / self.caller.stamina_max) * 100}%{'|n' : <5}\n"        
        f"{'< Attributes >':=^80}\n"
        f"{'|CStrength:|w' : <20}{self.caller.stats.STR.base : <20}\n{'|CEndurance:|w' : <20}{self.caller.stats.END.base : <20}\n{'|CDexterity:|w' : <20}{self.caller.stats.DEX.base : <20}\n"
        f"{'|CAgility:|w' : <20}{self.caller.stats.AGI.base : <20}\n{'|CMagic:|w' : <20}{self.caller.stats.MAG.base : <20}\n{'|CLuck:|w' : <20}{self.caller.stats.LUK.base : <20}|n\n"       
        f"{'< Status >':=^80}\n"
        f"{'You have earned a total of '}{self.caller.totalxp}{' experience.'}\n"
        f"{'You have '}{self.caller.currentxp}{' unspent experience.'}\n"
        #f"{'You have '}{self.caller.iron}{ ' Iron.'}\n"
        #f"{'|CPri:|w' : <10}({self.caller.level:3}) {self.caller.pri_class.name : <10}|n {'|CPri Exp TNL:|w' : <13}{self.caller.pri_xp_tnl - self.caller.currentxp : <15}|n\n"
        f"{'':=^80}\n"
        )        
        self.caller.msg(_CHAR_STATUS)


class CmdProf(DanMachiCommand):
    key = "proficiency"
    aliases = "prof"

    def func(self):
        _CHAR_STATUS  = (
        f"\n\n"
        f"{'< Details >':=^80}\n"
        f"{'|CSword:|w ':12}{math.trunc(self.caller.proficiencies.sword.value):5}{self.caller.proficiencies.sword.desc() : >15}\n"
        f"{'|CDagger:|w ':12}{math.trunc(self.caller.proficiencies.dagger.value):5}{self.caller.proficiencies.dagger.desc() : >15}\n"
        f"{'|CSpear:|w ':12}{math.trunc(self.caller.proficiencies.spear.value):5}{self.caller.proficiencies.spear.desc() : >15}\n"
        f"{'|CAxe:|w ':12}{math.trunc(self.caller.proficiencies.axe.value):5}{self.caller.proficiencies.axe.desc() : >15}\n"      
        f"{'':=^80}\n"
        )

        
        self.caller.msg(_CHAR_STATUS)

class CmdGain(DanMachiCommand):
    key = "gain"

    def func(self):

        caller = self.caller

        f"{'Test output'}"
        if self.caller.currentxp >= self.caller.pri_xp_tnl:
            caller.msg("You leveled up")
        elif self.caller.currentxp < self.caller.pri_xp_tnl:
            caller.msg("You did not level up")


class CmdInventoryExtended(Command):
    """
    View inventory

    Usage:
        inventory
        inv

    Shows your inventory.
    """

    key = "inventory"
    aliases = ["inv", "i"]
    locks = "cmd:all()"
    arg_regex = r"$"

    def func(self):
        """check inventory"""
        caller = self.caller
        if not caller.contents:
            caller.msg("You are not carrying or wearing anything.")
            return
        
        items = caller.contents
        tr = caller.traits
        equip_message = """
|015=================================|n
            |035Inventory
        Weight {current_weight}/{max_weight}|n   
|015=================================|n
Wielding: {wielding}
  Armors: {armor}
Clothing: {clothing}
Carrying: 
      {carrying}

|015=================================|n""".format(
            current_weight="".join(str([caller.stats.ENC.current])),
            max_weight="".join(str([caller.stats.ENC.max])),
            #wielding="\n\tSword",
            #armor="\n\tLeather Armor",
            #clothing="\n\tDress shirt",
            wielding="\n\t  ".join([caller.equip.get(slot).get_display_name(caller) for slot in wield_slots if caller.equip.get(slot)]),
            armor="\n\t".join([caller.equip.get(slot).get_display_name(caller) for slot in armor_slots if caller.equip.get(slot)]),
            clothing="\n\t".join([caller.equip.get(slot).get_display_name(caller) for slot in clothing_slots if caller.equip.get(slot)]),
            carrying="\n\t  ".join([item.get_display_name(caller) for item in items if not item in caller.equip]))
            #carrying="\n\t  ".join([item.get_display_name(caller) for item in items]))

        caller.msg(equip_message)

class CmdExtendedLook(CmdContainerLook, DanMachiCommand):
    """
    look

    Usage:
      look
      look <obj>
      look <room detail>
      look *<account> Test

    Observes your location, details at your location or objects in your vicinity.
    """
    def func(self):
        """
        Handle the looking - add fallback to details.
        """
        caller = self.caller
        args = self.args
        if args:
            looking_at_obj = caller.search(args,
                                           candidates=caller.location.contents + caller.contents,
                                           use_nicks=True,
                                           quiet=True)
            if not looking_at_obj:
                # no object found. Check if there is a matching
                # detail at location.
                location = caller.location
                if location and hasattr(location, "return_detail") and callable(location.return_detail):
                    detail = location.return_detail(args)
                    if detail:
                        # we found a detail instead. Show that.
                        caller.msg(detail)
                        return
                # no detail found. Trigger delayed error messages
                #_AT_SEARCH_RESULT(looking_at_obj, caller, args, quiet=False)
                return
            else:
                # we need to extract the match manually.
                looking_at_obj = utils.make_iter(looking_at_obj)[0]
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("You have no location to look at!")
                return

        if not hasattr(looking_at_obj, 'return_appearance'):
            # this is likely due to us having an account instead
            looking_at_obj = looking_at_obj.character
        if not looking_at_obj.access(caller, "view"):
            caller.msg("Could not find '%s'." % args)
            return
        # get object's appearance
        caller.msg(looking_at_obj.return_appearance(caller))
        # the object's at_desc() method.
        looking_at_obj.at_desc(looker=caller)

    def at_post_cmd(self):
        "called after self.func()."
        caller = self.caller

        health_bar = display_meter(caller.stats.HP.current, caller.stats.HP.max, length=15, align="center")
        mana_bar = display_meter(caller.stats.MP.current, caller.stats.MP.max, length=15, align="center", fill_color=['R','O','B'])
        self.msg(prompt = f"{health_bar} {mana_bar}\n\n")

    # def at_post_cmd(self):
    #     """
    #     This hook is called after the command has finished executing
    #     (after self.func()).
    #     """
    #     "called after self.func()."
    #     caller = self.caller
    #     prompt = ">"
    #     caller.msg("", prompt=prompt)


class CmdExtendedGet(default_cmds.CmdGet):
    """
   pick up something
   Usage:
     get <obj>
     get all
     
   Picks up an object from your location and puts it in
   your inventory. Alternatively if all is used will pick 
   up everything in the room that can be picked up  and 
   placed into your inventory.
   
   """
    key = "get"
    aliases = "grab"
    locks = "cmd:all()"

    def func(self):
        """implements the command."""

        caller = self.caller

        if 'all' in self.args:
            for obj in caller.location.contents:
                if not obj.access(caller, 'get'):
                    if obj.db.get_err_msg:
                        caller.msg(obj.db.get_err_msg)
                    else:
                        caller.msg("You can't get that.")
                    return

                obj.move_to(caller, quiet=True)
                caller.msg("You pick up %s." % obj.name)
                caller.location.msg_contents("%s picks up %s." % (caller.name, obj.name), exclude=caller)

                obj.at_get(caller)

        if not self.args:
            caller.msg("Get what?")
            return

        result = caller.search(self.args,
                               location=caller.location,
                               quiet=True)
        if not result:
            caller.msg("{} not found".format(self.args))
            return
        else:
            obj = result[0]

        if caller == obj:
            caller.msg("You can't get yourself.")
            return

        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        obj.move_to(caller, quiet=True)
        caller.msg("You pick up %s." % obj.name)
        caller.location.msg_contents("%s picks up %s." %
                                     (caller.name,
                                      obj.name),
                                     exclude=caller)
        # calling hook method
        obj.at_get(caller)

    def at_post_cmd(self):
        """
        This hook is called after the command has finished executing
        (after self.func()).
        """
        "called after self.func()."
        caller = self.caller
        prompt = ">"
        caller.msg("", prompt=prompt)


class CmdExtendedDrop(default_cmds.CmdDrop, DanMachiCommand):
    """
    drop something

    Usage:
      drop <obj>
      droppity drop

    Lets you drop an object from your inventory into the
    location you are currently in.
    """

    key = "drop"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        """Implement command"""

        caller = self.caller

        if 'all' in self.args:
            for obj in caller.contents:
                obj.move_to(caller.location, quiet=True)
                caller.msg('you drop %s' % (obj.name,))
                caller.location.msg_contents("%s drops %s." % (caller.name, obj.name), exclude=caller)
                obj.at_drop(caller)

        if not self.args:
            caller.msg("Drop what?")
            return

        # Because the DROP command by definition looks for items
        # in inventory, call the search function using location = caller
        result = caller.search(self.args, location=caller, nofound_string="You aren't carrying %s." % self.args,
                               quiet=True)
        if not result:
            return
        else:
            obj = result[0]

        obj.move_to(caller.location, quiet=True)
        caller.msg("You drop %s." % (obj.name,))
        caller.location.msg_contents("%s drops %s." %
                                     (caller.name, obj.name),
                                     exclude=caller)
        # Call the object script's at_drop() method.
        # obj.at_drop(caller)