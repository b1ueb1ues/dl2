from core.ctx import *
from target.dummy import *
from target.hms import *
from character.mikoto import *
from character.elisanne import *
from core import benchmark

logset('all')

logset('dmg')
logset('buff')
logset('bk')
#logset('dot')
#logset('afflic')
logset('s')
logset('sp')
#logset('act')
#logset('x')

import core.acl

def foo():
    global c
    global acl
    Ctx()
    tar = hms()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    #c.conf['slot']['w'] = 'v534_flame_zephyr'
    c.init()

    c2 = Elisanne()
    c2.tar(tar)
    c2.init()

    d = 120
    Timer.run(d)
    logcat()
    skada = Skada.sum()
    print('dps',skada['Mikoto']['dmg']/d)
    print('dps',skada['Elisanne']['dmg']/d)
    print(Skada._skada)
    Timer.run()

foo()

