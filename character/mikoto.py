import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *

class Mikoto(Character):
    def config(this, conf):
        conf.name    = 'Mikoto'
        conf.star    = 5
        conf.ele     = 'flame'
        conf.wt      = 'blade'
        conf.atk     = 520
        conf.a1      = ('cc', 0.10, 'hp70')
        conf.a3      = ('cc', 0.08)
        conf.slot.w  = 'c534_flame'
        #conf.slot.w  = 'v534_flame_zephyr'
        #conf.slot.d  = 'Cerb'
        #conf.slot.d  = 'Arctos'
        conf.slot.d  = 'Sakuya'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'BN'

        conf.s1.recovery = 1.4
        conf.s1.sp = 4500
        conf.s1.hit = [
                (0.4, 'h1'), 
                (0.5, 'h1'), 
                ]
        conf.s1.attr.h1.coef = 5.32
        conf.s1.attr.h2.coef = 3.54
        conf.s1.attr.h3.coef = 2.13
        conf.s1.attr.h4.coef = 4.25
        conf.s1.on_end = this.s1_end

        conf.s2.recovery = 1
        conf.s2.sp = 4500
        conf.s2.buff = ('self', 0.2, 10, 'spd')

    def init(this):
        this.stance = 0
        
    def s1_end(this):
        if this.stance == 0:
            this.conf.s1.hit = [(0.4,'h2'), (0.5,'h2'), (0.6,'h2')]
            this.conf.s1.recovery = 1.6
            this.conf.s1()

            this.stance = 1
            this.stancebuff = this.Selfbuff('s1', 0.10)(20)
            this.stancebuff.end = this.clean_stance

        elif this.stance == 1:
            this.conf.s1.hit = [(0.4,'h3'), (0.5,'h3'), (0.6,'h3'), (0.8,'h4')]
            this.conf.s1.recovery = 2
            this.conf.s1()

            this.stance = 2
            this.stancebuff.off()

            this.stancebuff = this.Selfbuff('s1', 0.15)(15)
            this.stancebuff.end = this.clean_stance

        else:
            this.conf.s1.hit = [(0.4,'h1'), (0.5,'h2')]
            this.conf.s1.recovery = 1.4
            this.conf.s1()

            this.stance = 0
            this.stancebuff.off()

    def clean_stance(this):
        this.stance = 0




if __name__ == '__main__':
    #logset(['buff', 'dmg', 'od', 'bk'])
    logset(['buff', 'dmg', 'bk', 'sp'])
    #logset('s')
    #logset(['buff','debug','dmg', 'hit'])

    tar = Dummy()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    c.init()

    Timer.run(3)
    logcat()
