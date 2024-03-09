"""
    Equipment Sheet EvForm template
"""

import re

FORMCHAR = "x"
TABLECHAR = "o"

FORM = """


o--------------------------------------------------------------------------o
||                             |C[ |rEquipment |C]|n                                ||
o--------------------------------------------------------------------------o
|| o-------------------------------o   o----------------------------------o ||
|| ||           Armor               ||   ||           Jewelry                || ||
|| o-------------------------------o   o----------------------------------o ||
|| || Head   | xAxxxxxxxxxxxxxxxx   ||   || Necklace  | xGxxxxxxxxxxxxxxxx   || ||
|| || ----------------------------- ||   || Trinket   | xHxxxxxxxxxxxxxxxx   || ||
|| || Chest  | xBxxxxxxxxxxxxxxxx   ||   || Earring 1 | xIxxxxxxxxxxxxxxxx   || ||
|| || ----------------------------- ||   || Earring 2 | xJxxxxxxxxxxxxxxxx   || ||
|| || Arms   | xCxxxxxxxxxxxxxxxx   ||   || Ring 1    | xKxxxxxxxxxxxxxxxx   || ||
|| || ----------------------------- ||   || Ring 2    | xLxxxxxxxxxxxxxxxx   || ||
|| || Belt   | xDxxxxxxxxxxxxxxxx   ||   +----------------------------------+ ||
|| || ----------------------------- ||
|| || Legs   | xExxxxxxxxxxxxxxxx   ||
|| || ----------------------------- ||
|| || Feet   | xFxxxxxxxxxxxxxxxx   ||
|| +-------------------------------+
||
|| o---------------------o---------------------o
|| |     Main Hand       |     Off Hand        ||
|| o---------------------o---------------------o
|| | xxxxxxxxxMxxxxxxxxx | xxxxxxxxxNxxxxxxxxx ||
|| o---------------------o---------------------o
o---------------------------------------------------------------o


"""
FORM = re.sub(r'\|$', r'', FORM, flags=re.M)
