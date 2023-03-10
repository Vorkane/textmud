from commands.command import Command
from evennia import default_cmds
import math

class CmdStatus(Command):
    key = "status"

    def func(self):
        _CHAR_STATUS  = (
        f"\n\n"
        f"{'< Details >' :=^99}\n"
        f"{'|CName:|w' : <15}{self.caller.name : <25}{'|CRace:|w' : <20}{self.caller.race.name : <20}{'|CGender:|w' : <20}Male{'': <16}|n\n"
         f"{'< Vitals >' :=^99}\n"
        f"{'|CHealth:|w' : <20}{self.caller.hp}{' |W['}{self.caller.hp_max}{']|n' : <18}{'|CMana:|w' : <20}{self.caller.mana}{' |W['}{self.caller.mana_max}{']|n' : <18}{'|CStamina:|w' : <20}{(2 / self.caller.stamina_max) * 100}%{'|n' : <5}\n"        
        f"{'< Attributes >' :=^99}\n"
        f"{'|CStrength:|w' : <20}{self.caller.strength : <20}{'|CDexterity:|w' : <20}{self.caller.dexterity : <20}{'|CConstitution:|w' : <20}{self.caller.constitution : <20}\n"
        f"{'|CIntelligence:|w' : <20}{self.caller.intelligence : <20}{'|CWisdom:|w' : <20}{self.caller.wisdom : <20}{'|CCharisma:|w' : <20}{self.caller.charisma : <20}|n\n"       
        f"{'< Status >' :=^99}\n"
        f"{'You have earned a total of '}{self.caller.xp}{' exp.'}\n"
        f"{'|CClass:|w' : <20}{self.caller.cclass.name : <20}|n {'|CLevel:|w' : <15}{self.caller.level : <30}{'|CExp TNL:|w' : <20}{self.caller.xp_tnl : <15}|n\n"
        f"{'' :=^99}\n"
        )

        
        self.caller.msg(_CHAR_STATUS)

