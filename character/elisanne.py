import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Elisanne(Character):
    def config(this, conf):
        conf.name    = 'Elisanne'
        conf.star    = 4
        conf.ele     = 'water'
        conf.wt      = 'lance'
        conf.atk     = 460
        conf.a1      = ('bt', 0.25)

        conf.s1.recovery = 1
        conf.s1.sp = 3817
        conf.s1.buff = ('s1', 0.20, 15)

        conf.s2.sp = 5158
        conf.s2.recovery = 1.9
        conf.s2.hit = [(0, 'h1')]
        conf.s2.attr.h1.coef = 7.54

        conf.slot.w  = 'c534_water'
        conf.slot.d  = 'DJ'
        conf.slot.a1 = 'BB'
        conf.slot.a2 = 'JotS'



if __name__ == '__main__':
    #logset(['buff', 'dmg', 'od', 'bk'])
    logset(['buff', 'dmg', 'bk', 'sp'])
    #logset('x')
    logset('fs')
    #logset('act')
    logset('s')
    #logset(['buff','debug','dmg', 'hit'])

    tar = Dummy()
    tar.init()

    c = Elisanne()
    c.tar(tar)
    c.init()

    Timer.run(60)
    logcat()
