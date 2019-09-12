import __init__
from core.ctx import *
from core.targetbase import *
from core.dummy import *
from core.mikoto import *
import benchmark


logset(['buff','debug','dmg', 'od', 'bk', 'ks'])

tar = Dummy()
tar.init()
tar.conf.od = 1000
tar.conf.bk = 1000
tar.Passive('',0.2,'ks','burn')()

c = Mikoto()
c.atk = 2000
c.tar(tar)
c.init()
c.Passive('a1',0.2,'killer','burn')()

ha = Conf()
ha.name = 's1'
ha.type = 's'
ha.coef = 1
ha.killer = {'bk':1, 'burn':0}

#c.Passive('dragon', 0.60)()
#c.Passive('ex-wand', 0.15, 's', 'ex')()
#c.Passive('ex-blade', 0.1, 'atk', 'ex')()
#c.Passive('a1', 0.1)()
#c.Buff('buff', 0.20)(10)

dmg = c.Dmg(ha)
#print(dmg.conf)

def foo():
    for i in range(1000000):
        dmg()

#benchmark.run(foo)
#exit()

def tick(t):
    #log('debug', 'dmg', dmg.calc())
    dmg()
    
    t(1)

Timer(tick)()

Timer.run(10)
logcat()
