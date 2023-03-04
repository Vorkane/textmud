

from evennia import EvMenu
from .chargen import TemporaryCharacterSheet

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
        tmp_character.name = raw_string.lower().capatilize()
    return "node_chargen", kwargs

def node_change_name(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]

    text = (
        f"Your current name is |w{tmp_character.name}|n. "
        "Enter a new name or leave empty to abort."
    )

    options = {
            "key": "_default",
            "goto": (_update_name, kwargs)

    }
    return text, options   

def node_apply_character(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]
    new_character = tmp_character.apply(caller)

    caller.account.db._playable_characters = [new_character]

    text = "Character created!"

    return text, None


def start_chargen(caller, session=None):

    menutree = {
        "node_chargen": node_chargen,
        "node_change_name": node_change_name,
        "node_apply_character": node_apply_character
    }

    tmp_character = TemporaryCharacterSheet() 

    EvMenu(caller, menutree, session=session, tmp_character=tmp_character)