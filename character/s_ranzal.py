import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from target.mg import *
from mod.afflic import *


class S_Ranzal(Character):
    def dconf(this):
        return {
        'slot.a':'RR+FRH',
        'acl.cancel' : '''
            `s1
            `s2, s='s1'
            `s3, fsc
            `fs, x=5
        ''',
        }

    def conf(this):
        return {
         'star'            : 4
        ,'ele'             : 'water'
        ,'wt'              : 'blade'
        ,'atk'             : 454
        ,'a1'              : ('lo', 0.40)
        ,'a3'              : ('skill_link', 0.08, 'def')

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 2.16
        ,'s1.stop'         : 3.100
        ,'s1.sp'           : 2489

        ,'s2.sp'           : 7383
        ,'s2.stop'         : 2.400

        }

    def init(this):
        this.Afflic = Afflic(this)
        this.bog = this.Afflic['bog']('s1', 1.20, 0.97)

    def s1_proc(this):
        this.bog()

    def s2_proc(this):
        this.Selfbuff('s2',0.5,'cd')(20)
        this.s1.full()


if __name__ =='__main__':
    import run
    run.this_character(mass=1)
