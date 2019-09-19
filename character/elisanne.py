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
        conf.slot.w  = 'c534_water'
        conf.slot.d  = 'DJ'
        conf.slot.a1 = 'BB'
        conf.slot.a2 = 'JotS'

        conf.s1.recovery = 1
        conf.s1.sp = 3817
        conf.s1.buff = ('s1', 0.20, 15)

        conf.s2.recovery = 1.9
        conf.s2.hit = [(0, 'h1')]
        conf.s2.attr.h1.coef = 7.54


    def s1_proc(this):
        this.target.Debuff('s1',0.1)(10)


    def init(this):
        this.stance = 0
        this.conf.s1.on_end = this.s1_end

        this.conf.s12.recovery = 1.83
        this.conf.s12.hit = [(0.23,'h2'), (0.42,'h2'), (0.65,'h2')]

        this.conf.s13.recovery = 2.8
        this.conf.s13.hit = [(0.22,'h3'), (0.42,'h3'),
                             (0.65,'h3'), (1.15,'h4')]

        this.ss = Skillshift(this, 1, this.conf.s12, this.conf.s13)
        

    def s1_end(this):
        if this.stance == 0:
            this.stancebuff = this.Selfbuff('s1', 0.10)(20)
            this.stancebuff.end = this.clean_stance
            this.stance = 1
        elif this.stance == 1:
            this.stancebuff.off()
            this.stancebuff = this.Selfbuff('s1', 0.15)(15)
            this.stancebuff.end = this.clean_stance
            this.stance = 2
        else:
            this.stance = 0
            this.stancebuff.off()


    def clean_stance(this):
        this.stance = 0
        this.ss.reset()




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

    c = Mikoto()
    c.tar(tar)
    c.init()

    Timer.run(60)
    logcat()
