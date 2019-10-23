import __init__
from core.ctx import *
from core.characterbase import *
from mod.bleed import *
from mod.afflic import *
from mod.skillupgrade import *


class Celliera(Character):
    def dconf(this):
        return {
        #'slot.a' : 'RR+JotS',
        'acl.cancel' : """
            `s2
            `s1
            `fsf, x=5
        """,
        }

    def conf(this):
        return {
         'name'            : 'Celliera'
        ,'star'            : 4
        ,'ele'             : 'water'
        ,'wt'              : 'blade'
        ,'atk'             : 492
        ,'a1'              : ('atk', 0.08, 'hp70')

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1'),(1,'h1')]
        ,'s1.attr.h1.coef' : 2.42
        ,'s1.recovery'     : 2.5
        ,'s1.sp'           : 2537
        ,'s12.proc'        : [this.s12_proc]

        ,'s2.sp'           : 4877
        ,'s2.recovery'     : 1
        }

    def init(this):
        this.Afflic = Afflic(this)
        this.Bleed = Bleed(this)
        this.freeze = this.Afflic['freeze']('s1', 1.10)
        this.ss = this.Selfbuff('s2',0.25)
        this.su = Skillupgrade(this,1,this.conf['s12'], this.ss)

    def s12_proc(this):
        this.freeze()

    def s2_proc(this):
        this.su(10)


if __name__ =='__main__':
    import run
    run.this_character(mass=0)
