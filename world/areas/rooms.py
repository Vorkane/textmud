from evennia import AttributeProperty, DefaultRoom

class EvAdventureRoom(DefaultRoom):

    """ Simple room supporting some EvAdventure-specifics"""

    allow_combat = AttributeProperty(False, autocreate=False)
    allow_pvp = AttributeProperty(False, autocreate=False)
    allow_death = AttributeProperty(False, autocreate=False)