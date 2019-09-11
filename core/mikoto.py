import __init__
from core.ctx import *
from core.characterbase import *
from core.dummy import *

class Mikoto(Character):
    def config(this, conf):
        conf.name    = 'Mikoto'
        conf.star    = 5
        conf.ele     = 'flame'
        conf.wt      = 'blade'
        conf.atk     = 520
        conf.a1      = ('hp70', 'cc', 10)
        conf.a1      = ('resist', 'stun', 100)
        conf.a3      = ('', 'cc', 0)
        conf.slot.w  = 'c534'
        conf.slot.d  = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'CE'

        conf.s1.recovery = 1.4

    def test(this):
        this.a1 = this.Action('a1', this.conf.s1)
        this.a1()
        this.conf.s1.startup = 10
        def foo(t):
            this.conf.s1.recovery = 0.5
            this.a1()
        Timer(foo)(5)



if __name__ == '__main__':
    logset(['act','buff','debug','dmg', 'od', 'bk'])

    tar = Dummy()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    c.init()

    c.Passive('dragon', 0.60)()
    c.Passive('ex-wand', 0.15, 's', 'ex')()
    c.Passive('ex-blade', 0.1, 'atk', 'ex')()
    c.Passive('a1', 0.1)()
    c.Buff('buff', 0.20)(10)

    
    c.test()

    Timer.run()
    logcat()
