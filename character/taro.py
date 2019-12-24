import __init__
from core.ctx import *
from core.characterbase import *


class Jurota(Character):
    def dconf(this):
        return {
        'acl.cancel': """
            `s1
            `s2
            `s3
            `fsf, x=5
        """,
        }


    def conf(this):
        return {
         'star'    : 3
        ,'ele'     : 'shadow'
        ,'wt'      : 'blade'
        ,'atk'     : 495

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 2.93
        ,'s1.sp'           : 2392
        ,'s1.stop'         : 2.733

        ,'s2.hit'          : [(0,'h1')]
        ,'s2.attr.h1.coef' : 7.9
        ,'s2.sp'           : 5259
        ,'s2.stop'         : 1.833
        }


if __name__ == '__main__':
    import run
    run.this_character()
