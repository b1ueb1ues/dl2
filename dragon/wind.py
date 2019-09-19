import __init__
from dragon.dragonbase import *

class Zephyr(Dragon):
    ele = 'wind'
    atk = 127
    a = [('atk',0.60)]


class Longlong(Dragon):
    ele = 'wind'
    atk = 127
    a = [('atk', 0.45),
        ('cd', 0.55)]


class Pazuzu(Dragon):
    ele = 'wind'
    atk = 126
    a = [('atk',0.5),
        ('k',0.2,'poison')]


class Vayu(Dragon):
    ele = 'wind'
    atk = 126
    aura = [('atk', 0.20),
            ('sd', 0.90)]


class Freyja(Dragon):
    ele = 'wind'
    atk = 120
    a = [('sp', 0.35)]


