# from evennia.commands.default.muxcommand import MuxCommand, MuxAccountCommand
from evennia.commands.command import Command
from evennia.contrib.rpg.health_bar import display_meter

# from evennia import utils


class DanMachiCommand(Command):
    """Base command for Characters"""

    def at_post_cmd(self):
        "called after self.func()."
        # caller = self.caller

        # health_bar = display_meter(caller.stats.HP.current, caller.stats.HP.max, length=15, align="center")
        # mana_bar = display_meter(caller.stats.MP.current, caller.stats.MP.max, length=15, align="center", fill_color=['R', 'O', 'B'])
        # self.msg(prompt=f"{health_bar} {mana_bar}\n\n")

    # def parse(self):
    #     """
    #     This method is called by the cmdhandler once the command name
    #     has been identified. It creates a new set of member variables
    #     that can be later accessed from self.func() (see below)
    #      The following variables are available for our use when entering this
    #     method (from the command definition, and assigned on the fly by the
    #     cmdhandler):
    #        self.key - the name of this command ('look')
    #        self.aliases - the aliases of this cmd ('l')
    #        self.permissions - permission string for this command
    #        self.help_category - overall category of command
    #         self.caller - the object calling this command
    #         self.cmdstring - the actual command name used to call this
    #                         (this allows you to know which alias was used,
    #                          for example)
    #        self.args - the raw input; everything following self.cmdstring.
    #        self.cmdset - the cmdset from which this command was picked. Not
    #                      often used (useful for commands like 'help' or to
    #                      list all available commands etc)
    #        self.obj - the object on which this command was defined. It is often
    #                     the same as self.caller.
    #      A MUX command has the following possible syntax:
    #        name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]

    #     The 'name[ with several words]' part is already dealt with by the
    #     cmdhandler at this point, and stored in self.cmdname (we don't use
    #     it here). The rest of the command is stored in self.args, which can
    #     start with the switch indicator /.

    #     This parser breaks self.args into its constituents and stores them in the
    #     following variables:
    #       self.switches = [list of /switches (without the /)]
    #       self.raw = This is the raw argument input, including switches
    #       self.args = This is re-defined to be everything *except* the switches
    #       self.lhs = Everything to the left of = (lhs:'left-hand side'). If
    #                  no = is found, this is identical to self.args.
    #       self.rhs: Everything to the right of = (rhs:'right-hand side').
    #                 If no '=' is found, this is None.
    #       self.lhslist - [self.lhs split into a list by comma]
    #       self.rhslist - [list of self.rhs split into a list by comma]
    #       self.arglist = [list of space-separated args (stripped, including '=' if it exists)]

    #       All args and list members are stripped of excess whitespace around the
    #       strings, but case is preserved.
    #     """
    #     raw = self.args
    #     args = raw.strip()

    #     # split out switches
    #     switches = []
    #     if args and len(args) > 1 and args[0] == "/":
    #         # we have a switch, or a set of switches. These end with a space.
    #         switches = args[1:].split(None, 1)
    #         if len(switches) > 1:
    #             switches, args = switches
    #             switches = switches.split('/')
    #         else:
    #             args = ""
    #             switches = switches[0].split('/')
    #     arglist = [arg.strip() for arg in args.split()]
    #     # check for arg1, arg2, ... = argA, argB, ... constructs
    #     lhs, rhs = args, None
    #     lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
    #     if args and '=' in args:
    #         lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
    #         lhslist = [arg.strip() for arg in lhs.split(',')]
    #         rhslist = [arg.strip() for arg in rhs.split(',')]

    #     # save to object properties:
    #     self.raw = raw
    #     self.switches = switches
    #     self.args = args.strip()
    #     self.arglist = arglist
    #     self.lhs = lhs
    #     self.lhslist = lhslist
    #     self.rhs = rhs
    #     self.rhslist = rhslist

    #     # if the class has the account_caller property set on itself, we make
    #     # sure that self.caller is always the account if possible. We also create
    #     # a special property "character" for the puppeted object, if any. This
    #     # is convenient for commands defined on the Account only.
    #     if hasattr(self, "account_caller") and self.account_caller:
    #         if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
    #             # caller is an Object/Character
    #             self.character = self.caller
    #             self.caller = self.caller.account
    #         elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
    #             # caller was already an Account
    #             self.character = self.caller.get_puppet(self.session)
    #         else:
    #             self.character = None


class DanMachiPlayerCommand(Command):
    """Base command for Players/Accounts"""

    pass
