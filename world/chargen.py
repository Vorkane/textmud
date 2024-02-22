from django.conf import settings

from evennia import create_object
from evennia.contrib.grid.xyzgrid.xyzgrid import get_xyzgrid
from evennia.objects.models import ObjectDB
from evennia.utils.evmenu import EvMenu
from evennia.utils import dedent

from typeclasses.characters import Character
# from world.characters.races import Races

from .rules import dice

from world.characters.races import _SORTED_ALL_RACES
# from typeclasses.characters import Character

import world.characters.races


_ABILITIES = {
    "STR": "strength",
    "END": "endurance",
    "DEX": "dexterity",
    "AGI": "agility",
    "MAG": "magic",
    "LUK": "luck"
}

_TEMP_SHEET = """
|wName:|n {name}
|wRace:|n {race}

|wHP:|n {hp} / {hp_max}

|w=========Attributes=========|n

|wStrength:|n        {strength}
|wEndurnace:|n       {endurance}
|wDexterity:|n       {dexterity}
|wAgility:|n         {agility}
|wMagic:|n           {magic}
|wLuck:|n            {luck}

|w============================|n

"""


class TemporaryCharacterSheet:
    """
    This collects all the rules for generating a new character. An instance of this class is used
    to pass around the current character state during character generation and also applied to
    the character at the end. This class instance can also be saved on the menu to make sure a user
    is not losing their half-created character.

    Note:
        In standard Knave, the character's attribute bonus is rolled randomly and will give a
        value 1-6; and there is no guarantee for 'equal' starting characters.

        Knave uses a d8 roll to get the initial hit points. We will follow the recommendation
        from the rule that we will use a minimum of 5 HP.

        We *will* roll random start equipment though. Contrary to standard Knave, we'll also
        randomly assign the starting weapon among a small selection of equal-dmg weapons (since
        there is no GM to adjudicate a different choice).

    """

    def __init__(self):

        self.name = ""
        self.race = "None"
        self.cl_race = ""

        self.strength = 5
        self.endurance = 5
        self.dexterity = 5
        self.agility = 5
        self.magic = 5
        self.luck = 5

        self.hp_max = max(18, dice.roll("1d30"))
        self.hp = self.hp_max

    def _swap_race(self, new_race):

        _race = new_race

        # get_race_class = getattr(world.characters.races, _race)

        self.race_type = _race
        self.cl_race = _race
        self.race = self.race_type.name
        self.strength = self.race_type.str_base
        self.endurance = self.race_type.end_base
        self.dexterity = self.race_type.dex_base
        self.agility = self.race_type.agi_base
        self.magic = self.race_type.mag_base
        self.luck = self.race_type.luk_base

    def show_sheet(self):
        """
        Show a temp character sheet, a compressed version of the real thing.

        """

        return _TEMP_SHEET.format(
            name=self.name,
            race=self.race,
            strength=self.strength,
            endurance=self.endurance,
            dexterity=self.dexterity,
            agility=self.agility,
            magic=self.magic,
            luck=self.luck,
            hp=self.hp,
            hp_max=self.hp_max,
        )

    def apply(self, account):
        """
        Once the chargen is complete, call this create and set up the character.

        """
        grid = get_xyzgrid()
        start_location = grid.get_room(('12', '7', 'orario'))
        # start_location = "#39"
        if start_location:
            start_location = start_location[0]  # The room we got above is a queryset so we get it by index
        else:
            start_location = ObjectDB.objects.get_id(settings.START_LOCATION)

        default_home = ObjectDB.objects.get_id(settings.DEFAULT_HOME)
        permissions = settings.PERMISSION_ACCOUNT_DEFAULT

        # creating character with given abilities
        new_character = create_object(
            Character,
            key=self.name,
            location=start_location,
            home=default_home,
            permissions=permissions,
        )

        new_character.db.race = self.cl_race.name
        new_character.db.slots = self.cl_race.slots
        new_character.db.limbs = self.cl_race.limbs
        new_character.db.size = self.cl_race.size

        new_character.stats.STR.base = int(self.strength)
        new_character.stats.END.base = int(self.endurance)
        new_character.stats.DEX.base = int(self.dexterity)
        new_character.stats.AGI.base = int(self.agility)
        new_character.stats.MAG.base = int(self.magic)
        new_character.stats.LUK.base = int(self.luck)

        new_character.stats.HP.max = int(10 + new_character.stats.END.base * 1.5)
        new_character.stats.HP.current = int(new_character.stats.HP.max)

        new_character.stats.MP.max = int(10 + new_character.stats.MAG.base * 0.5)
        new_character.stats.MP.current = int(new_character.stats.MP.max)

        new_character.stats.ST.max = int(10 + new_character.stats.END.base * 0.5)
        new_character.stats.ST.current = int(new_character.stats.ST.max)

        new_character.locks.add(
            "puppet:id(%i) or pid(%i) or perm(Developer) or pperm(Developer);delete:id(%i) or"
            " perm(Admin)" % (new_character.id, account.id, account.id)
        )
        # spawn equipment
        # TODO: add item prototypes
        # none of the equipment from the random tables have prototypes, so there is no starting gear
        """ if self.weapon:
            try:
                weapon = spawn(self.weapon)
                new_character.equipment.move(weapon[0])
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Weapon: Prototype not found for '{self.weapon}'.")

        if self.armor:
            try:
                armor = spawn(self.armor)
                new_character.equipment.move(armor[0])
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Armor: Prototype not found for '{self.armor}'.")

        if self.shield:
            try:
                shield = spawn(self.shield)
                new_character.equipment.move(shield[0])
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Shield: Prototype not found for '{self.shield}'.")

        if self.helmet:
            try:
                helmet = spawn(self.helmet)
                new_character.equipment.move(helmet[0])
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Helmet: Prototype not found for '{self.helmet}'.")

        for item in self.backpack:
            try:
                item = spawn(item)
                new_character.equipment.move(item[0])
            except KeyError:
                logger.log_err(f"[Chargen] Could not spawn Item: Prototype not found for '{item}'.")
 """
        return new_character


##########################################################
#
# chargen menu section
#
##########################################################

##########################################################
#               Start Character Generation
##########################################################

def start_chargen(caller, session=None):
    # node_initial_name()

    menutree = {
        "menunode_welcome": menunode_welcome,
        "menunode_rules": menunode_rules,
        "menunode_name": menunode_name,
        "menunode_base": menunode_base,
        "menunode_show_race": menunode_show_race,
        "menunode_select_race": menunode_select_race,
        "menunode_apply_race": menunode_apply_race,
        "menunode_apply": menunode_apply
    }

    tmp_character = TemporaryCharacterSheet()

    EvMenu(caller, menutree, session=session, startnode="menunode_welcome", startnode_input=("sgsg", {"tmp_character": tmp_character}))

##########################################################
#               Welcome page
##########################################################


def menunode_welcome(caller, **kwargs):

    caller.msg("\n" * settings.CLIENT_DEFAULT_HEIGHT)

    # tmp_character = kwargs["tmp_character"]

    """ Starting Page. """
    text = dedent(
        """\
        |wWelcome to Character Creation!|n

        This is the starting node for all brand new characters. It's a good place to
        remind players that they can exit the character creator and resume later,
        especially if you're going to have a really long chargen process.
    """
    )

    help = "You can explain the commands for exiting and resuming more specifically here."
    options = {"desc": "Let's begin!", "goto": ("menunode_rules", kwargs)}

    return (text, help), options


##########################################################
#               Rules
##########################################################

def menunode_rules(caller, **kwargs):

    caller.msg("\n" * settings.CLIENT_DEFAULT_HEIGHT)

    # tmp_character = kwargs["tmp_character"]

    text = dedent(
        """\
           Have you read the rules and agree to abide by them?
    """
    )
    options = [
        {"desc": "I agree to the rules", "goto": ("menunode_name", kwargs)},
        {"desc": "I do not agree to the rules", "goto": "node_change_name"},
    ]

    return text, options

##########################################################
#               Change your Name
##########################################################


def menunode_name(caller, raw_string, **kwargs):

    caller.msg("\n" * settings.CLIENT_DEFAULT_HEIGHT)

    tmp_character = kwargs["tmp_character"]

    if tmp_character.name:
        text = (
            f"You are already name |g{tmp_character.name}|n.\n"
            "What would you like your new name to be named?\n"
            "Enter name or leave empty to abort."
        )
    else:
        text = (
            "What would you like to be named?\n"
            "Enter name or leave empty to abort."
        )

    options = {
        "key": "_default",
        "goto": (_update_name, kwargs)
    }
    return text, options


def _update_name(caller, raw_string, **kwargs):

    key = raw_string.strip()

    from evennia.objects.models import ObjectDB
    typeclass = settings.BASE_CHARACTER_TYPECLASS

    if ObjectDB.objects.filter(db_typeclass_path=typeclass, db_key__iexact=key):
        # check if this Character already exists. Note that we are only
        # searching the base character typeclass here, not any child
        # classes.
        caller.msg("|rA character named '|w%s|r' already exists.|n" % key)
        return
    else:
        tmp_character = kwargs["tmp_character"]
        tmp_character.name = key.lower().capitalize()

    # options = [
    #     {"key": ("Yes", "y"), "desc": f"Confirm you want to be name |w{tmp_character.name}|n", "goto": ("menunode_base", kwargs)},
    #     {"key": ("No", "n"), "desc": f"Change my name.", "goto": "menunode_name"},
    # ]
    return "menunode_base", kwargs


def menunode_base(caller, raw_string, **kwargs):

    tmp_character = kwargs["tmp_character"]

    text = tmp_character.show_sheet()

    options = [
        {"desc": "Change your name.", "goto": ("menunode_name", kwargs)},
        {"desc": "Change your race.", "goto": ("menunode_show_race", kwargs)},
        {"desc": "Accept and create the character.", "goto": ("menunode_apply", kwargs)}
    ]

    return text, options


def menunode_show_race(caller, raw_string, **kwargs):

    text = """\
        Select a |cRace|n.

        Select one by number below to view its details, or |whelp|n
        at any time for info.
    """

    options = []

    for race in _SORTED_ALL_RACES:
        options.append({
            "desc": "|c{}|n".format(race),
            "goto": ("menunode_select_race", {"race": race, **kwargs}),

        })
    return (text, "Select a race to show it's details"), options


def menunode_select_race(caller, raw_string, **kwargs):
    try:
        choice = int(raw_string.strip())
        _race = _SORTED_ALL_RACES[choice - 1]
    except (ValueError, KeyError, IndexError):
        caller.msg("|rInvalid choice. Try again.")
        return None

    get_race_class = getattr(world.characters.races, _race)

    text = get_race_class.desc + "\nWould you like to become this race?"
    options = (
        {"key": ("Yes", "y"), "desc": f"Become {get_race_class.name}", "goto": ("menunode_apply_race", {'race': get_race_class, **kwargs}), },
        {"key": ("No", "n", "_default"), "desc": "Return to main menu", "goto": "menunode_show_race"}
    )

    return text, options


def menunode_apply_race(caller, raw_string, **kwargs):
    race = kwargs.get('race')
    get_race_class = getattr(world.characters.races, race)
    tmp_character = kwargs["tmp_character"]
    tmp_character._swap_race(get_race_class)
    caller.msg('Swapper race!')

    return menunode_base(caller, '', tmp_character=tmp_character)


def menunode_apply(caller, raw_string, **kwargs):
    """
    End chargen and create the character. We will also puppet it.

    """
    tmp_character = kwargs["tmp_character"]

    new_character = tmp_character.apply(caller)
    caller.db._playable_characters.append(new_character)
    session = caller.ndb._evmenu._session
    caller.puppet_object(session=session, obj=new_character)

    text = "Character created!"

    return text, None

# def node_chargen(caller, raw_string, **kwargs):

#     tmp_character = kwargs["tmp_character"]

#     text = tmp_character.show_sheet()

#     options = [
#         {
#             "desc": "Change your name",
#             "goto": ("node_change_name", kwargs)
#         }
#     ]
#     options.append(
#         {
#             "desc": "Accept and create character",
#             "goto": ("node_apply_character", kwargs)
#         },
#     )

#     return text, options

# def menunode_welcome(caller):
#     """Starting page."""
#     # make sure it's a player not a generic character
#     if not caller.new_char.is_typeclass("typeclasses.characters.Character"):
#         # it's not - swap it
#         caller.new_char.swap_typeclass("typeclasses.characters.Character")

#     text = dedent(
#         """\
#         |wWelcome to the game!|n

#         During the character creation process, you can go forwards and back between steps,
#         as well as quit and resume later. Feel free to take your time!
#     """
#     )
#     options = {"desc": "Let's begin!", "goto": "menunode_points_base"}
#     return text, options
