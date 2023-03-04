from dataclasses import dataclass

@dataclass(frozen=True)
class Race:
    key: str
    name: str
    desc: str

    def __str__(self):
        return self.name
    
class Races:
    _cached_dict = None

    Human = Race(
        key="human",
        name="Human",
        desc="Your average human."
    )

    Dwarf = Race(
        key="dwarf",
        name="Dwarf",
        desc="Short and stocky"
    )




    @classmethod
    def _get_cached_dict(cls):
        if not cls._cached_dict:
            new_dict = {value.key: value for value in cls.__dict__.values() if isinstance(value, Race)}
            cls._cached_dict = new_dict
        return cls._cached_dict
    
    @classmethod
    def item(cls):
        return cls._get_cached_dict().items()
    
    @classmethod
    def values(cls):
        return cls._get_cached_dict().values()
    
    @classmethod
    def get(cls,key):
        return cls._get_cached_dict().get(key)