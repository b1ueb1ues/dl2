import __init__
from core.ctx import *
from core.characterbase import *
from mod.energy import *


class Pia(Character):
    def dconf(this):
        conf = {
            'acl.cancel': """
                `s1
                `s2, x=5
                `s3
                `fs, x=5
            """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 4
        ,'ele'     : 'wind'
        ,'wt'      : 'lance'
        ,'atk'     : 446

        ,'s1.stop'            : 1.85
        ,'s1.sp'              : 2579
        ,'s1.attr.h1.coef'    : 8.38
        ,'s1.hit'             : [(0,'h1')]

        ,'s2.stop'     : 1
        ,'s2.sp'       : 3636
        }

    def s2_end(this):
        this.Energy.team(1)


if __name__ == '__main__':
    import run
    run.this_character()
