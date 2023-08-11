from evennia.contrib.base_systems.building_menu import BuildingMenu
from commands.base import DanMachiCommand
from commands.command import Command

class RoomBuildingMenu(BuildingMenu):

    """
    Building menu to edit a room.
    """

    def init(self, room):
        self.add_choice("title", key="t", attr="key", glance="{obj.key}", text="""
                -------------------------------------------------------------------------------
                Editing the title of {{obj.key}}(#{{obj.id}})

                You can change the title simply by entering it.
                Use |y{back}|n to go back to the main menu.

                Current title: |c{{obj.key}}|n
        """.format(back="|n or |y".join(self.keys_go_back)))
        self.add_choice_edit("description", "d")
        self.add_choice("exits", "e", glance=glance_exits, text=text_exits,
on_nomatch=nomatch_exits)


# Menu functions
def glance_exits(room):
    """Show the room exits."""
    if room.exits:
        glance = ""
        for exit in room.exits:
            glance += f"\n  |y{exit.key}|n"

        return glance

    return "\n  |gNo exit yet|n"

def text_exits(caller, room):
    """Show the room exits in the choice itself."""
    text = "-" * 79
    text += "\n\nRoom exits:"
    text += "\n Use |y@c|n to create a new exit."
    text += "\n\nExisting exits:"
    if room.exits:
        for exit in room.exits:
            text += f"\n  |y@e {exit.key}|n"
            if exit.aliases.all():
                text += " (|y{aliases}|n)".format(aliases="|n, |y".join(
                    alias for alias in exit.aliases.all()
                ))
            if exit.destination:
                text += f" toward {exit.get_display_name(caller)}"
    else:
        text += "\n\n |gNo exit has yet been defined.|n"

    return text

def nomatch_exits(menu, caller, room, string):
    """
    The user typed something in the list of exits.  Maybe an exit name?
    """
    string = string[3:]
    exit = caller.search(string, candidates=room.exits)
    if exit is None:
        return

    # Open a sub-menu, using nested keys
    caller.msg(f"Editing: {exit.key}")
    menu.open_submenu("commands.building.ExitBuildingMenu", exit, parent_keys=["e"])
    return False

class ExitBuildingMenu(BuildingMenu):

    """
    Building menu to edit an exit.

    """

    def init(self, exit):
        self.add_choice("key", key="k", attr="key", glance="{obj.key}")
        self.add_choice_edit("description", "d")


class EditCmd(Command):

    """
    Editing command.

    Usage:
      @edit [object]

    Open a building menu to edit the specified object.  This menu allows to
    specific information about this object.

    Examples:
      @edit here
      @edit self
      @edit #142

    """

    key = "@edit"
    locks = "cmd:id(1) or perm(Builders)"
    help_category = "Building"

    def func(self):
        if not self.args.strip():
            self.msg("|rYou should provide an argument to this function: the object to edit.|n")
            return

        obj = self.caller.search(self.args.strip(), global_search=True)
        if not obj:
            return

        if obj.typename == "Room":
            Menu = RoomBuildingMenu
        else:
            obj_name = obj.get_display_name(self.caller)
            self.msg(f"|rThe object {obj_name} cannot be edited.|n")
            return

        menu = Menu(self.caller, obj)
        menu.open()