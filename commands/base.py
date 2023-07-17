from evennia.commands.default.muxcommand import MuxCommand, MuxAccountCommand
from evennia import default_cmds
from evennia.contrib.rpg.health_bar import display_meter

class DanMachiCommand(default_cmds.MuxCommand):
    """Base command for Characters"""

    def at_post_cmd(self):
        "called after self.func()."
        caller = self.caller

        health_bar = display_meter(caller.db.hp, caller.db.hp_max, length=15, align="center")
        mana_bar = display_meter(caller.db.mana, caller.db.mana_max, length=15, align="center", fill_color=['R','O','B'])
        self.msg(prompt = f"{health_bar} {mana_bar}\n\n")
        

class DanMachiPlayerCommand(MuxAccountCommand):
    """Base command for Players/Accounts"""

    pass
