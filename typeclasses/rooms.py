"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia.objects.objects import DefaultRoom
from evennia.contrib.rpg.rpsystem.rpsystem import ContribRPRoom
import textwrap

from .objects import ObjectParent


class Room(ContribRPRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """


    appearance_template = (
        '{header}'
        f"{'==='}{' |502{name}|n ' :=<50}\n"
        '{desc}\n'
        f"{' |502Characters|n ':=^56}"
        '{characters}\n'
        f"{' |502Exits|n ':=^56}\n"
        '{exits}\n'
        '{footer}'
    )

    # appearance_template = """
    # {header}
    # |502{name}|n
    # {desc}
    # {exits}{characters}{things}
    # {footer}
    # """

    pass
