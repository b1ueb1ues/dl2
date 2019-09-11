import __init__
from core.ctx import *
from core.targetbase import *
from core.dummy import *
from core.mikoto import *
import benchmark


logset(['buff','debug','dmg', 'od', 'bk'])

tar = Dummy()
tar.init()

c = Mikoto()
c.tar(tar)
c.init()

ha = Conf()
ha.name = 's1'
ha.type = 's'
ha.coef = 10

c.Passive('dragon', 0.60)()
c.Passive('ex-wand', 0.15, 's', 'ex')()
c.Passive('ex-blade', 0.1, 'atk', 'ex')()
c.Passive('a1', 0.1)()
c.Buff('buff', 0.20)(10)

dmg = c.Dmg(ha)
print(dmg.conf)


def tick(t):
    log('debug', dmg.calc())
    dmg()
    
    t(1)

Timer(tick)()

Timer.run(15)
logcat()
