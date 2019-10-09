from core.ctx import *
from target.dummy import *
from target.hms import *
from character.mikoto import *
from character.elisanne import *
from character.faketeam import *
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
    tar = dummy()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    #c.conf['slot']['w'] = 'v534_flame_zephyr'
    c.init()

    c2 = Elisanne()
    c2.tar(tar)
    c2.init()

    c3 = Faketeam()
    c3.tar(tar)
    c3.init()

    d = 120
    r = Timer.run(d)
    logcat()
    skada = Skada.sum()
    print('dps',skada['Mikoto']['dmg']/now())
    print('dps',skada['Elisanne']['dmg']/now())
    print('dps',skada['Faketeam']['dmg']/now())
    for i in Skada._skada:
        print(i, Skada._skada[i])

foo()

