from commands.command import Command
from evennia import default_cmds
import math

class CmdStatus(Command):
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
        f"{'|CStrength:|w' : <20}{self.caller.strength : <20}\n{'|CDexterity:|w' : <20}{self.caller.dexterity : <20}\n{'|CConstitution:|w' : <20}{self.caller.constitution : <20}\n"
        f"{'|CIntelligence:|w' : <20}{self.caller.intelligence : <20}\n{'|CWisdom:|w' : <20}{self.caller.wisdom : <20}\n{'|CCharisma:|w' : <20}{self.caller.charisma : <20}|n\n"       
        f"{'< Status >':=^80}\n"
        f"{'You have earned a total of '}{self.caller.totalxp}{' experience.'}\n"
        f"{'You have '}{self.caller.currentxp}{' unspent experience.'}\n"
        f"{'|CPri:|w' : <10}({self.caller.level:3}) {self.caller.pri_class.name : <10}|n {'|CPri Exp TNL:|w' : <13}{self.caller.pri_xp_tnl - self.caller.currentxp : <15}|n\n"
        f"{'':=^80}\n"
        )

        
        self.caller.msg(_CHAR_STATUS)


class CmdProf(Command):
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

class CmdGain(Command):
    key = "gain"

    def func(self):

        caller = self.caller

        f"{'Test output'}"
        if self.caller.currentxp >= self.caller.pri_xp_tnl:
            caller.msg("You leveled up")
        elif self.caller.currentxp < self.caller.pri_xp_tnl:
            caller.msg("You did not level up")