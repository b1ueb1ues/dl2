from slot import *

class Zephyr(DragonBase):
    ele = 'wind'
    atk = 127
    a = [('atk',0.60)]


class Longlong(DragonBase):
    ele = 'wind'
    atk = 127
    a = [('atk', 0.45),
        ('cd', 0.55)]


class Pazuzu(DragonBase):
    ele = 'wind'
    atk = 126
    a = [('atk',0.5),
        ('k',0.2,'poison')]


class Vayu(DragonBase):
    ele = 'wind'
    atk = 126
    aura = [('atk', 0.20),
            ('sd', 0.90)]


class Freyja(DragonBase):
    ele = 'wind'
    atk = 120
    a = [('sp', 0.35)]


