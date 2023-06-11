from commands.command import Command
from evennia import default_cmds
import math

class CmdStatus(Command):
    key = "score"

    def func(self):
        _CHAR_STATUS  = (
        f"\n\n"
        f"{'< Details >':=^80}\n"
        f"{'|CName:|w':10}{self.caller.name:25}{'|CRace:|w':10}{self.caller.race.name:20}{'|CGender:|w':12}Male{'':16}|n\n"
        f"{'< Vitals >':=^80}\n"
        f"{'|CHealth:|w' : <12}{self.caller.hp}{'|W('}{self.caller.hp_max}{')|n' : <10}{'|CMana:|w' : <9}{self.caller.mana}{'|W('}{self.caller.mana_max}{')|n' : <10}{'|CStamina:|w' : <13}{(2 / self.caller.stamina_max) * 100}%{'|n' : <5}\n"        
        f"{'< Attributes >':=^80}\n"
        f"{'|CStrength:|w' : <20}{self.caller.strength : <20}\n{'|CDexterity:|w' : <20}{self.caller.dexterity : <20}\n{'|CConstitution:|w' : <20}{self.caller.constitution : <20}\n"
        f"{'|CIntelligence:|w' : <20}{self.caller.intelligence : <20}\n{'|CWisdom:|w' : <20}{self.caller.wisdom : <20}\n{'|CCharisma:|w' : <20}{self.caller.charisma : <20}|n\n"       
        f"{'< Status >':=^80}\n"
        f"{'You have earned a total of '}{self.caller.totalxp}{' experience.'}\n"
        f"{'You have '}{self.caller.currentxp}{' unspent experience.'}\n"
        f"{'|CPri:|w' : <10}({self.caller.level:3}) {self.caller.cclass.name : <10}|n {'|CPri Exp TNL:|w' : <13}{self.caller.pri_xp_tnl - self.caller.currentxp : <15}|n\n"
        f"{'':=^80}\n"
        )

        
        self.caller.msg(_CHAR_STATUS)

