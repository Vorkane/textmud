from evennia import default_cmds
from commands.base import DanMachiCommand
import math

class CmdLook(default_cmds.CmdLook, DanMachiCommand):
    pass

class CmdLook234(default_cmds.CmdLook, DanMachiCommand):
    key = "look1"
    aliases = ["l1", "ls1"]


class CmdLook123(DanMachiCommand):
    """
    look test text

    Usage:
      look
      look <obj>
      look *<player>

    Observes your location or objects in your vicinity.
    """

    key = "look1"
    aliases = ["l1", "ls1"]
    locks = "cmd:all()"
    arg_regex = r"\s.*?|$"

    def func(self):
        """
        Handle the looking.
        """
        caller = self.caller
        args = self.args
        if args:
            # Use search to handle duplicate/nonexistent results.
            looking_at_obj = caller.search(args, use_nicks=True)
            if not looking_at_obj:
                return
        else:
            looking_at_obj = caller.location
            if not looking_at_obj:
                caller.msg("You have no location to look at!")
                return

        if not hasattr(looking_at_obj, "return_appearance"):
            # this is likely due to us having a player instead
            looking_at_obj = looking_at_obj.character
        if not looking_at_obj.access(caller, "view"):
            caller.msg("Could not find '%s'." % args)
            return
        # get object's appearance
        caller.msg(looking_at_obj.return_appearance(caller))
        # the object's at_desc() method.
        looking_at_obj.at_desc(looker=caller)

class CmdStatus(DanMachiCommand):
    key = "status"
    aliases = "score"

    def func(self):
        _CHAR_STATUS  = (
        f"\n\n"
        f"{'< Details >':=^80}\n"
        f"{'|CName:|w':10}{self.caller.name:25}\n"
        f"{'|CRace:|w':10}{self.caller.race.name:20}{'|CGender:|w':12}Male{'':16}|n\n"
        f"{'< Vitals >':=^80}\n"
        f"{'|CHealth:|w' : <12}{self.caller.hp}{'|W('}{self.caller.hp_max}{')|n' : <10}{'|CMana:|w' : <10}{self.caller.mana}{'|W('}{self.caller.mana_max}{')|n' : <10}{'|CStamina:|w' : <13}{(2 / self.caller.stamina_max) * 100}%{'|n' : <5}\n"        
        f"{'< Attributes >':=^80}\n"
        f"{'|CStrength:|w' : <20}{self.caller.strength : <20}\n{'|CEndurance:|w' : <20}{self.caller.endurance : <20}\n{'|CDexterity:|w' : <20}{self.caller.dexterity : <20}\n"
        f"{'|CAgility:|w' : <20}{self.caller.agility : <20}\n{'|CMagic:|w' : <20}{self.caller.magic : <20}\n{'|CLuck:|w' : <20}{self.caller.luck : <20}|n\n"       
        f"{'< Status >':=^80}\n"
        f"{'You have earned a total of '}{self.caller.totalxp}{' experience.'}\n"
        f"{'You have '}{self.caller.currentxp}{' unspent experience.'}\n"
        f"{'You have '}{self.caller.iron}{ ' Iron.'}\n"
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