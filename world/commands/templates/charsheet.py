"""
    Character Sheet EvForm template
"""

import re

FORMCHAR = "x"
TABLECHAR = "o"

FORM = """


o-=-=-=-=-=-=-=-=-=-=-=-|C[ |rCharacter Sheet |C]|n-=-=-=-=-=-=-=-=-=-=-=-=-o
||                                                                   ||
|| Name : xAxxxxxxxx                                                 ||
|| Title: xBxxxxxxxx                                                 ||         
|| Race : xCxxxxxxxx                                                 ||
||                                                                   || 
 >-----------------------------------------------------------------< 
||                                                                   ||
||   |CStrength|n    : xLx                |CAgility    : xOx               || 
||   |CEndurnace|n   : xMx                |CMagic      : xPx               ||
||   |CDexterity|n   : xNx                |CLuck       : xQx               ||
||                                                                   ||
 >-----------------------------------------------------------------<
||                                                                   ||
||                                                                   ||
||                                                                   ||
||                                                                   ||
||                                                                   ||
o-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-o


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