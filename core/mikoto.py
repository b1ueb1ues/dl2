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
        conf.a1      = ('cc', 0.10, 'hp70')
        conf.a3      = ('cc', 0.08)
        #conf.slot.w  = 'c534_flame'
        conf.slot.w  = 'v534_zephyr'
        conf.slot.d  = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'CE'

        conf.s1.recovery = 1.6
        conf.s1.sp = 4500
        conf.s1.hit = [
                (0.4, 'h1'), 
                (0.5, 'h1'), 
                ]
        conf.s1.attr.h1.coef = 5.32
        conf.s1.on_end = this.s1buff

        conf.s2.recovery = 1
        conf.s2.sp = 4500
        conf.s2.buff = ('self', 0.2, 10, 'spd')

        
    def s1buff(this):
        this.Selfbuff('s1', 0.1)(10)


    def test(this):
        this.a1 = this.Ability('c1', *this.conf.a1)
        this.a3 = this.Ability('c3', *this.conf.a3)

        this.a = this.Amulet(this.conf.slot.a1, this.conf.slot.a2)
        this.a.init()

        this.w = this.Weapon(this.conf.wt, this.conf.slot.w)
        this.w.init()
        print(this.w.atk)
        print(this.w.a)

        this.d1 = this.Ability('d', 'atk', 0.60)()



if __name__ == '__main__':
    logset(['buff', 'dmg', 'od', 'bk'])
    logset('sp')
    #logset(['buff','debug','dmg', 'hit'])

    tar = Dummy()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    c.init()
    c.test()

    Timer.run(5)
    logcat()
