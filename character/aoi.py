import __init__
from core.ctx import *
from core.characterbase import *


class Aoi(Character):
    def dconf(this):
        return {
        'acl.cancel': """
            `s1, x=5
            `s2, x=5
            `s3, x=5
            `fsf, x=5
        """,
        }


    def conf(this):
        return {
         'star'    : 3
        ,'ele'     : 'flame'
        ,'wt'      : 'blade'
        ,'atk'     : 494
        ,'a1'      : ('od', 0.08)

        ,'s1.recovery'     : 1.85
        ,'s1.sp'           : 2630
        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 8.78

        ,'s2.recovery'     : 1.85
        ,'s2.sp'           : 5280
        ,'s2.hit'          : [(0,'h1')]
        ,'s2.attr.h1.coef' : 7.9
        }


if __name__ == '__main__':
    import run
    run.this_character()
