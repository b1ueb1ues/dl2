import __init__
from core.ctx import *
from core.characterbase import *
from mod.bleed import *


class Botan(Character):
    def dconf(this):
        conf = {
            'slot.a': 'RR+JotS',
            'acl.cancel' : """
            `s1
            `s2, fs
            `s3
            `fs, x=5
            """,
        }
        return conf

    def conf(this):
        return {
         'star'            : 4
        ,'ele'             : 'shadow'
        ,'wt'              : 'lance'
        ,'atk'             : 439
        ,'a3'              : ('prep', '50%')

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 1.5
        ,'s1.sp'           : 2427
        ,'s1.recovery'     : 2.6

        ,'s2.buff'         : ('team',0.15,15)
        ,'s2.sp'           : 7634
        ,'s2.recovery'     : 1
        }

    def init(this):
        this.Bleed = Bleed(this)
        this.bleed = this.Bleed('s1',0.8,1.32)

    def s1_proc(this):
        this.bleed()


if __name__ =='__main__':
    import run
    run.this_character(mass=1)
