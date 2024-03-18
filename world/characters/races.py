from dataclasses import dataclass

"""
Races Module

This module contains data and functions relating to Races. Its
public module functions are to be used primarily during the
character creation process.

classes:

    `Race`: base class for all races
    `Dwarf`: dwarf race class
    `Elf`: elf race class
    `HalfElf`: half-elf race class
    `Human`: human race class
    `Pallum`: pallum race class
    `Renard`: renard race class

Module Functions

    - `load_race(str)`: loads an instance of the named Race class
    - `apply_race(char, race)`: have a character "become" a member of the specified race
        with the specified focus


"""


@dataclass(frozen=True)
class Race:
    key: str
    name: str
    desc: str
    strength_mod: int = 0
    dexterity_mod: int = 0
    constitution_mod: int = 0
    intelligence_mod: int = 0
    wisdom_mod: int = 0
    charisma_mod: int = 0

    base_strength: int = 0
    base_endurance: int = 0
    base_dexterity: int = 0
    base_agility: int = 0
    base_magic: int = 0
    base_luck: int = 0

    def __str__(self):
        return self.name


# TODO Write good descriptions

class RaceException(Exception):
    """Base exception class for races module."""
    def __init__(self, msg):
        self.msg = msg


ALL_RACES = ('Dwarf', 'Elf', 'Half-Elf', 'Humand', 'Pallum', 'Renard')
_SORTED_ALL_RACES = sorted(list(ALL_RACES))
KINGDOM_RACES = ('Human', 'Elf', 'Dwarf', 'Gnome', 'Centaur', 'Ogryn')
CALIPHATE_RACES = ('Human', 'Drow', 'Duergar', 'Svirfneblin', 'Wemic', 'Drakkar')
EMPIRE_RACES = ('Human', 'Ursine', 'Feline', 'Lupine', 'Vulpine', 'Naga')


def load_race(race):
    """Returns an instance of the named race class.
    Args:
        race (str): case-insensitive name of race to load
    Returns:
        (Race): instance of the appropriate subclass of `Race`
    """
    race = race.strip().capitalize()

    if race in ALL_RACES:
        return globals()[race]()
    else:
        raise RaceException("Invalid race specified.")


def apply_race(character, race):
    """Causes a Character to "become" the named race.
    Args:
        character: the character object becoming a member of race
        race (str, Race): the name of the race to apply
    """

    if isinstance(race, Race):
        race = race.name
    race = load_race(race)

    # Set race and related attributes on the character
    character.db.race = race.name
    character.db.slots = race.slots
    character.db.limbs = race.limbs
    character.db.size = race.size
    character.msg('You have become {}.' .format(race.name))


class Races2(object):
    """Base class for race attributes"""

    slots = {
        # armor slots
        'wield1': None,
        'wield2': None,
        'helm': None,
        'necklace': None,
        'cloak': None,
        'torso': None,
        'belt': None,
        'bracers': None,
        'gloves': None,
        'ring1': None,
        'ring2': None,
        'boots': None,
        # clothing slots
        'hat': None,
        'accessory': None,
        'overtop': None,
        'top': None,
        'bottom': None,
        'belt2': None,
        'accessory2': None,
        'gloves2': None,
        'accessory3': None,
        'accessory4': None,
        'shoes': None,

    }
    limbs = (
        ('r_hand', ('wield1',)),
        ('l_hand', ('wield2',)),
        ('head', ('helm', 'hat')),
        ('neck', ('necklace', 'accessory',)),
        ('back', ('cloak', 'overtop')),
        ('body', ('torso', 'top',)),
        ('waist', ('belt', 'belt2', 'bottom',)),
        ('wrists', ('bracers', 'accessory2',)),
        ('hands', ('gloves', 'gloves2',)),
        ('finger1', ('ring1', 'accessory3',)),
        ('finger2', ('ring2', 'accessory4',)),
        ('feet', ('boots', 'shoes',)),
    )

    def __init__(self):
        self.name = ""
        self.description = ""
        self.plural = ""
        self.size = ""
        self.bonuses = {}
        self.language = {}


class Dwarf(Races2):

    name = "Dwarf"
    desc = ("Dwarf\n\n"
            "Short and strong.\n"
            )
    str_base = 12
    end_base = 12
    dex_base = 8
    agi_base = 8
    mag_base = 10
    luk_base = 10
    size = "medium"

    def __init__(self):
        super(Dwarf, self).__init__()
        self.name = "Dwarf"
        self.plural = "Dwarfs"
        self.size = "medium"
        self.traits.STR.base = 12
        self.traits.END.base = 12
        self.traits.DEX.base = 8
        self.traits.AGI.base = 8
        self.traits.MAG.base = 10
        self.traits.LUK.base = 10


class Elf(Races2):

    name = "Elf"
    desc = ("Elf\n"
            "Skinny and Agile.\n"
            )

    str_base = 8
    end_base = 10
    dex_base = 8
    agi_base = 12
    mag_base = 12
    luk_base = 10
    size = "medium"

    def __init__(self):
        super(Elf, self).__init__()
        self.name = "Elf"
        self.plural = "Elves"
        self.size = "medium"
        self.traits.STR.base = 8
        self.traits.END.base = 10
        self.traits.DEX.base = 8
        self.traits.AGI.base = 12
        self.traits.MAG.base = 12
        self.traits.LUK.base = 10


class HalfElf(Races2):

    name = "Half-Elf"
    desc = "Skinny and Agile."

    def __init__(self):
        super(HalfElf, self).__init__()
        self.name = "Half-Elf"
        self.plural = "Half-elves"
        self.size = "medium"
        self.traits.STR.base = 10
        self.traits.END.base = 10
        self.traits.DEX.base = 10
        self.traits.AGI.base = 10
        self.traits.MAG.base = 10
        self.traits.LUK.base = 10


class Human(Races2):

    name = "Human"
    desc = "Skinny and Agile."

    def __init__(self):
        super(Human, self).__init__()
        self.name = "Human"
        self.plural = "Humans"
        self.size = "medium"
        self.traits.STR.base = 10
        self.traits.END.base = 10
        self.traits.DEX.base = 10
        self.traits.AGI.base = 10
        self.traits.MAG.base = 10
        self.traits.LUK.base = 10


class Pallum(Races2):

    name = "Pallum"
    desc = "Skinny and Agile."

    def __init__(self):
        super(Pallum, self).__init__()
        self.name = "Pallum"
        self.plural = "Pallums"
        self.size = "small"
        self.traits.STR.base = 8
        self.traits.END.base = 8
        self.traits.DEX.base = 12
        self.traits.AGI.base = 12
        self.traits.MAG.base = 8
        self.traits.LUK.base = 12


class Renard(Races2):

    name = "Renard"
    desc = "Skinny and Agile."

    def __init__(self):
        super(Renard, self).__init__()
        self.name = "Renard"
        self.plural = "Renards"
        self.size = "medium"
        self.traits.STR.base = 6
        self.traits.END.base = 8
        self.traits.DEX.base = 10
        self.traits.AGI.base = 8
        self.traits.MAG.base = 14
        self.traits.LUK.base = 12


class Races:

    _cached_dict = None

    Dwarf = Race(
        key="dwarf",
        name="Dwarf",
        base_strength=12,
        base_endurance=12,
        base_dexterity=8,
        base_agility=8,
        base_magic=10,
        base_luck=10,
        strength_mod=1,
        desc="Short and strong.",
    )

    Elf = Race(
        key="elf",
        name="Elf",
        base_strength=8,
        base_endurance=10,
        base_dexterity=8,
        base_agility=12,
        base_magic=12,
        base_luck=10,
        strength_mod=-1,
        wisdom_mod=1,
        desc="Regular elves",
    )

    HalfElf = Race(
        key="half_elf",
        name="Half Elf",
        base_strength=10,
        base_endurance=10,
        base_dexterity=10,
        base_agility=10,
        base_magic=10,
        base_luck=10,
        wisdom_mod=1,
        desc="Bit less average",
    )

    Human = Race(
        key="human",
        name="Human",
        base_strength=10,
        base_endurance=10,
        base_dexterity=10,
        base_agility=10,
        base_magic=10,
        base_luck=10,
        desc="Your average human.",
    )

    Pallum = Race(
        key="pallum",
        name="Pallum",
        base_strength=8,
        base_endurance=8,
        base_dexterity=12,
        base_agility=12,
        base_magic=8,
        base_luck=12,
        dexterity_mod=1,
        desc="Smaller in stature, they appear similar to humans. Often called hobbits",
    )

    Rednard = Race(
        key="renard",
        name="Renard",
        base_strength=6,
        base_endurance=8,
        base_dexterity=10,
        base_agility=8,
        base_magic=14,
        base_luck=12,
        desc="Smaller in stature, they appear similar to humans. Often called hobbits",
    )

    @classmethod
    def _get_cached_dict(cls):
        if not cls._cached_dict:
            new_dict = {value.key: value for value in cls.__dict__.values() if isinstance(value, Race)}
            cls._cached_dict = new_dict
        return cls._cached_dict

    @classmethod
    def items(cls):
        return cls._get_cached_dict().items()

    @classmethod
    def values(cls):
        return cls._get_cached_dict().values()

    @classmethod
    def get(cls, key):
        return cls._get_cached_dict().get(key)


"""     Goblin = Race(
        key="goblin",
        name="Goblin",
        cunning_mod=1,
        strength_mod=-1,
        will_mod=1,
        desc="Small and cunning"
    )

    Orc = Race(
        key="orc",
        name="Orc",
        strength_mod=2,
        will_mod=-1,
        desc="Tall and strong",
    )

    Lizardman = Race(
        key="lizardman",
        name="Lizardman",
        cunning_mod=1,
        strength_mod=1,
        will_mod=-1,
        desc="Reptilian hunters"
    )

    Ratman = Race(
        key="ratman",
        name="Ratman",
        cunning_mod=2,
        strength_mod=-1,
        desc="Shorter but cunning"
    )
"""
