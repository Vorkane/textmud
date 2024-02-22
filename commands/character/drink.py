from evennia.commands.command import Command
from evennia import InterruptCommand


class CmdFill(Command):

    """
    Fill a container with liquid.

    Usage:
        fill <container> from <liquid source>
    """

    key = "fill"

    def parse(self, debug=True):
        self.args = self.args.strip()
        target_container_entry, *from_container_entry = self.args.split(" from ", 1)

        if not self.args:
            self.caller.msg("Fill what from what?")
            raise InterruptCommand

        self.target_container = self.caller.search(target_container_entry)
        try:
            self.from_container = self.caller.search(from_container_entry[0].strip())
        except IndexError:
            self.caller.msg("Fill from what?")
            raise InterruptCommand

        if debug:
            target_ok = hasattr(self.target_container, "is_liquid_container")
            from_ok = hasattr(self.from_container, "is_liquid_container")
            self.caller.msg(f"Target container: {self.target_container}, {target_ok}")
            self.caller.msg(f"From container: {self.from_container}, {from_ok}")

    def func(self):

        if not hasattr(self.target_container, "is_liquid_container"):
            self.caller.msg(f"You can't fill {self.target_container}.")
            return

        if not hasattr(self.from_container, "is_liquid_container"):
            self.caller.msg(f"You can't fill {self.target_container} from this.")
            return
