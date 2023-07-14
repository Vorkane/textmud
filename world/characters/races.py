from dataclasses import dataclass


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

    strength: int = 0
    endurance: int = 0
    dexterity: int = 0
    agility: int = 0
    magic: int = 0
    luck: int = 0


    def __str__(self):
        return self.name


# TODO Write good descriptions


class Races:
    _cached_dict = None

    Dwarf = Race(
        key="dwarf",
        name="Dwarf",
        strength=12,
        endurance=12,
        dexterity=8,
        agility=8,
        magic=10,
        luck=10,
        strength_mod=1,
        desc="Short and strong.",
    )

    Elf = Race(
        key="elf",
        name="Elf",
        strength=8,
        endurance=10,
        dexterity=8,
        agility=12,
        magic=12,
        luck=10,
        strength_mod=-1,
        wisdom_mod=1,
        desc="Regular elves",
    )

    HalfElf = Race(
        key="half_elf",
        name="Half Elf",
        strength=10,
        endurance=10,
        dexterity=10,
        agility=10,
        magic=10,
        luck=10,
        wisdom_mod=1,
        desc="Bit less average",
    )

    Human = Race(
        key="human",
        name="Human",
        strength=10,
        endurance=10,
        dexterity=10,
        agility=10,
        magic=10,
        luck=10,
        desc="Your average human.",
    )

    Pallum = Race(
        key="pallum",
        name="Pallum",
        strength=8,
        endurance=8,
        dexterity=12,
        agility=12,
        magic=8,
        luck=12,
        dexterity_mod=1,
        desc="Smaller in stature, they appear similar to humans. Often called hobbits",
    )

    Rednard = Race(
        key="renard",
        name="Renard",
        strength=6,
        endurance=8,
        dexterity=10,
        agility=8,
        magic=14,
        luck=12,
        dexterity_mod=1,
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