"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPRoom
from evennia import AttributeProperty

from evennia.contrib.grid.xyzgrid.xyzroom import XYZRoom


class Room(ContribRPRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """

    allow_combat = AttributeProperty(False, autocreate=False)
    allow_pvp = AttributeProperty(False, autocreate=False)
    allow_death = AttributeProperty(False, autocreate=False)

    appearance_template = """
|/{header}
|510[ |224{name}{extra_name_info} |510]|n
{desc}|/
|510[ |224Exits |510]|n|/{exits}
{characters}
{things}
{footer}|/
    """


"""
Room

Rooms are simple containers that has no location of their own.

"""


CHAR_SYMBOL = "|w@|n"
CHAR_ALT_SYMBOL = "|w>|n"
ROOM_SYMBOL = "|bo|n"
LINK_COLOR = "|B"

_MAP_GRID = [
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", "@", " ", " "],
    [" ", " ", " ", " ", " "],
    [" ", " ", " ", " ", " "],
]
_EXIT_GRID_SHIFT = {
    "north": (0, 1, "||"),
    "east": (1, 0, "-"),
    "south": (0, -1, "||"),
    "west": (-1, 0, "-"),
    "northeast": (1, 1, "/"),
    "southeast": (1, -1, "\\"),
    "southwest": (-1, -1, "/"),
    "northwest": (-1, 1, "\\"),
}

""" class OverworldRoom(wilderness.WildernessRoom, Room):
    """ """""
    Special typeclass for the Overworld rooms
    Allows displaying the Overworld map
    """ """""

    VIEW_WIDTH = 13
    VIEW_HEIGHT = 9
    VIEW_HALF_WIDTH = VIEW_WIDTH // 2
    VIEW_HALF_HEIGHT = VIEW_HEIGHT // 2

    def return_appearance(self, looker, **kwargs):
        result = super().return_appearance(looker, **kwargs)
        if not result:
            return result

        map = self.get_map_display(looker)
        result += f"\n{map}\n"

        return result

    def get_map_display(self, looker):
        overworld = Overworld.get_instance()
        x, y = overworld.get_obj_coordinates(looker)
        width = self.VIEW_WIDTH
        height = self.VIEW_HEIGHT
        half_width = self.VIEW_HALF_WIDTH
        half_height = self.VIEW_HALF_HEIGHT
        top_left_x = x - half_width
        top_left_y = y - half_height

        symbols = OverworldMap.get_rect_symbols(top_left_x, top_left_y, width, height)
        symbols[half_height][half_width] = "@"
        rows = ["".join((symbol for symbol in row)) for row in symbols]

        tile_str = "\n".join(rows)

        return tile_str """


class TownRoom(Room, XYZRoom):
    """
    Combines the XYZGrid functionality with Ainneve-specific room code.
    """

    map_visual_range = 2


class PvPRoom(Room):
    """
    Room where PvP can happen, but noone gets killed.

    """

    allow_combat = AttributeProperty(True, autocreate=False)
    allow_pvp = AttributeProperty(True, autocreate=False)

    def get_display_footer(self, looker, **kwargs):
        """
        Display the room's PvP status.

        """
        return "|yNon-lethal PvP combat is allowed here!|n"
