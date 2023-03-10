import time
from random import random

from evennia import Command
from evennia.server import signals
from evennia.typeclasses.attributes import AttributeProperty
from evennia.utils import search, utils

class BaseSkill:
    key ="template"
    name = "Template"
    flavor = "Template"
    visible = True
    
    triggers = []

    handler = None
    start = 0

    duration = -1
    playtime = False
    cooldown = 0

    refresh = True
    unique =  True
    maxstacks = 1
    stacks = 1
    tickrate = 0

    mods = []
    cache  = {}