from evennia.utils import EvMenu
from .chargen import TemporaryCharacterSheet


import inflect
from random import choice
from typeclasses.characters import Character

from evennia.prototypes.spawner import spawn
from evennia.utils import dedent
from evennia.utils.evtable import EvTable

_INFLECT = inflect.engine()

#########################################################
#                   Welcome Page
#
# https://github.com/InspectorCaracal/evennia-minimud/blob/main/world/chargen_menu.py
#
#########################################################

def start_chargen(caller, session=None):
    node_change_name()

    # menutree = {
    #     "node_chargen": node_chargen
    # }

    # tmp_character = TemporaryCharacterSheet()

    # EvMenu(caller, menutree, session=session, tmp_character=tmp_character)

def node_chargen(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]

    text = tmp_character.show_sheet()

    options = [
        {
            "desc": "Change your name",
            "goto": ("node_change_name", kwargs)
        }
    ]
    options.append(
        {
            "desc": "Accept and create character",
            "goto": ("node_apply_character", kwargs)
        },
    )

    return text, options


def _update_name(caller, raw_string, **kwargs):
    if raw_string:
        tmp_character = kwargs["tmp_character"]
        tmp_character.name = raw_string.lower().capitalize()
    return "node_chargen", kwargs

def node_change_name(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]

    if tmp_character.name == "":
        text = (
            f"What would you like to be named? "
            "Enter name or leave empty to abort."
        )
    elif tmp_character.name != "":
        text = (
            f"Your current name is |w{tmp_character.name}|n. "
            "Enter a new name or leave empty to abort."
        )

    options = {
        "key": "_default",
        "goto": (_update_name, kwargs)
    }
    return text, options

def menunode_welcome(caller):
    """Starting page."""
    # make sure it's a player not a generic character
    if not caller.new_char.is_typeclass("typeclasses.characters.Character"):
        # it's not - swap it
        caller.new_char.swap_typeclass("typeclasses.characters.Character")

    text = dedent(
        """\
        |wWelcome to the game!|n

        During the character creation process, you can go forwards and back between steps,
        as well as quit and resume later. Feel free to take your time!
    """
    )
    options = {"desc": "Let's begin!", "goto": "menunode_points_base"}
    return text, options
