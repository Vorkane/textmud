from evennia.commands.command import Command
from commands.base import DanMachiCommand
from evennia import InterruptCommand

class CmdFill(Command):
    """
    Fill a container with liquid.

    Usage:
        fill <container> <liquid source>
    """

    key = "fill"

    def parse(self):
        self.args = self.args.strip()
        if not self.args:
            self.caller.msg("Fill what with what?")
            raise InterruptCommand
        
    def func(self):
        fillable = self.caller.search(self.args)
        if not fillable:
            return
        try:
            fillable.fill_canteen(self.caller)
        except AttributeError:
            self.caller.msg("You cannot fill that!")