import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from mod.skillshift import *
from mod.afflic import *


class Mikoto(Character):
    def conf(this):
        return {
         'name'    : 'Mikoto'
        ,'star'    : 5
        ,'ele'     : 'flame'
        ,'wt'      : 'blade'
        ,'atk'     : 520
        ,'a1'      : ('cc', 0.10,'hp70')
        ,'a3'      : ('cc', 0.08)

        ,'s1.on_end'       : this.s1_end
        ,'s1.recovery'     : 1.62  # 1.83 2.8
        ,'s1.sp'           : 4500
        ,'s1.hit'          : [(0.18,'h1'),
                              (0.43,'h1')]
        ,'s1.attr.h1.coef' : 5.32
        ,'s1.attr.h2.coef' : 3.54
        ,'s1.attr.h3.coef' : 2.13
        ,'s1.attr.h4.coef' : 4.25

        ,'s2.recovery'     : 1
        ,'s2.sp'           : 4500
        ,'s2.buff'         : ('self', 0.2, 10,'spd')

        ,'slot.w'  : 'c534_flame'
       #,'slot.w'  : 'v534_flame_zephyr'
       #,'slot.d'  : 'Cerb'
       #,'slot.d'  : 'Arctos'
        ,'slot.d'  : 'Sakuya'
        ,'slot.a1' : 'RR'
        ,'slot.a2' : 'BN'

        ,'acl.cancel': """
            `s1, x=5
            `s2, x=5
            `s3, x=5
            `fsf, x=5
        """

        }

    def init(this):

        this.stance = 0
        conf = {
                 's12.recovery' : 1.83
                ,'s12.hit'      : [(0.23,'h2'), (0.42,'h2'), (0.65,'h2')]
                ,'s13.recovery' : 2.8
                ,'s13.hit'      : [(0.22,'h3'), (0.42,'h3'),
                                     (0.65,'h3'), (1.15,'h4')]
                }
        this.conf_w.update(conf)

        this.ss = Skillshift(this, 1, this.conf['s12'], this.conf['s13'])
        

    def s1_end(this):
        if this.stance == 0:
            this.stancebuff = this.Selfbuff('s1', 0.10)(20)
            this.stancebuff.on_end = this.clean_stance
            this.stance = 1
        elif this.stance == 1:
            this.stancebuff.off()
            this.stancebuff = this.Selfbuff('s1', 0.15)(15)
            this.stancebuff.on_end = this.clean_stance
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

    Timer.run(180)
    logcat()
