"""
    Inventory Sheet EvForm template
"""

import re

FORMCHAR = "x"
TABLECHAR = "o"

FORM = """


o-=-=-=-=-=-=-=-=-=-|C[ |rInventory |C]|n-=-=-=-=-=-=-=-=-=-=-o
||                                                     ||
|| Weight : xAx/ xBx                                   ||
||                                                     ||
 >----------------------------------------------------<
||                                                     ||
||   |CWielding|n  : xCxxxxxxxxxxxxxxxxxxxx                ||
||   |CArmors|n    : xDxxxxxxxxxxxxxxxxxxxx                ||
||   |CClothing|n  : xExxxxxxxxxxxxxxxxxxxx                ||
||                                                     ||
o-=-=-=-=-=-=-=-=-=-|C[ |rCarrying |C]|n-=-=-=-=-=-=-=-=-=-=-o
||                                                     ||
||    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                             ||
||    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx                                                 ||
||    xxxxxxxxxxxxxxxxxxxxFxxxxxxxxxxxxxxxxxxxxxx                                                ||
||                                                     ||
o-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-o


"""
FORM = re.sub(r'\|$', r'', FORM, flags=re.M)

# FORM = """
# o-=-=-=-=-=-=-=-=-=-=-=-|C[ |rCharacter Sheet |C]|n-=-=-=-=-=-=-=-=-=-=-=-=-o
# ||                                                                   ||
# || Name : xAxxxxxxxx                      |CStrength|n     : xLx         ||
# || Title: xBxxxxxxxx                      |CEndurance|n    : xMx         ||
# || Race : xCxxxxxxxx                      |CDextrity|n     : xNx         ||
# ||                                        |CAgility|n      : xOx         ||
# ||                                        |CMagic|n        : xPx         ||
# ||                                        |CLuck|n         : xQx         ||
# ||                                                                   ||
# ||                                                                   ||
# ||                                                                   ||
# ||                                                                   ||
# ||                                                                   ||
# ||                                                                   ||
# ||                                                                   ||
# o-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-o
# """
