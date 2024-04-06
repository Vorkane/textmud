from dataclasses import dataclass


@dataclass(frozen=True)
class CharacterClass:
    key: str
    name: str
    desc: str

    def __str__(self):
        return self.name


class CharacterClasses:
    _cached_dict = None

    Default = CharacterClass(
        key="none",
        name="None",
        desc="Default Class."
    )
    Warrior = CharacterClass(
        key="warrior",
        name="Warrior",
        desc="Very strong in melee combat."
    )

    Rogue = CharacterClass(
        key="rogue",
        name="Rogue",
        desc="Adept fighter relying on stealthy tactics and evasion."
    )

    @classmethod
    def _get_cached_dict(cls):
        if not cls._cached_dict:
            new_dict = {value.key: value for value in cls.__dict__.values() if isinstance(value, CharacterClass)}
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
