"""
Command sets

All commands in the game must be grouped in a cmdset.  A given command
can be part of any number of cmdsets and cmdsets can be added/removed
and merged onto entities at runtime.

To create new commands to populate the cmdset, see
`commands/command.py`.

This module wraps the default command sets of Evennia; overloads them
to add/remove commands from the default lineup. You can create your
own cmdsets by inheriting from them or directly from `evennia.CmdSet`.

"""

from evennia import default_cmds
from typeclasses.accounts import CharGenAccount
from commands import custom_commands
from commands import sittables
from evennia.contrib.game_systems.containers import ContainerCmdSet
from world.commands.mining import CmdMine

from functools import wraps

from evennia.commands.default import (
    cmdset_character,
    cmdset_account,
    cmdset_session,
    cmdset_unloggedin,
)



def check_errors(func):
    """
    Decorator for catching/printing out any errors in method calls. Designed for safer imports.
    Args:
        func: Function to decorate

    Returns:
        Wrapped function
    """
    # noinspection PyBroadException
    @wraps(func)
    def new_func(*args, **kwargs):
        """Wrapper around function with exception handling"""
        try:
            return func(*args, **kwargs)
        except Exception:
            import traceback

            traceback.print_exc()

    return new_func




class CharacterCmdSet(cmdset_character.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `AccountCmdSet` when an Account puppets a Character.
    """

    key = "DefaultCharacter"
    priority = 101

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        #super().at_cmdset_creation()
        #self.add_standard_cmdsets()
        self.add(custom_commands.CmdLook234())
        self.add(custom_commands.CmdLook())
        self.add(custom_commands.CmdStatus())
        self.add(custom_commands.CmdProf())
        self.add(custom_commands.CmdGain())
        self.add(sittables.CmdSit2)
        self.add(sittables.CmdStand2)
        self.add(ContainerCmdSet)
        self.add(CmdMine())
        #
        # any commands you add below will overload the default ones.
        #


    @check_errors
    def add_standard_cmdsets(self):
        """Add different command sets that all characters should have"""
        #self.add(custom_commands.CmdLook())
        self.add(custom_commands.CmdLook123())


class AccountCmdSet(default_cmds.AccountCmdSet):
    """
    This is the cmdset available to the Account at all times. It is
    combined with the `CharacterCmdSet` when the Account puppets a
    Character. It holds game-account-specific commands, channel
    commands, etc.
    """

    key = "DefaultAccount"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        self.add(CharGenAccount())
        #
        # any commands you add below will overload the default ones.
        #


class UnloggedinCmdSet(default_cmds.UnloggedinCmdSet):
    """
    Command set available to the Session before being logged in.  This
    holds commands like creating a new account, logging in, etc.
    """

    key = "DefaultUnloggedin"

    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #


class SessionCmdSet(default_cmds.SessionCmdSet):
    """
    This cmdset is made available on Session level once logged in. It
    is empty by default.
    """

    key = "DefaultSession"

    def at_cmdset_creation(self):
        """
        This is the only method defined in a cmdset, called during
        its creation. It should populate the set with command instances.

        As and example we just add the empty base `Command` object.
        It prints some info.
        """
        super().at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
