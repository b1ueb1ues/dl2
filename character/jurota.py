import __init__
from core.ctx import *
from core.characterbase import *

class Jurota(Character):
    def dconf(this):
        conf = {
        'acl.cancel' : """
            `s1
            `s2, x=5
            `s3
            `fsf, x=5
        """,
        }
        return conf

    def conf(this):
        return {
         'star'            : 3
        ,'ele'             : 'water'
        ,'wt'              : 'blade'
        ,'atk'             : 492
        ,'a1'              : ('bk', 0.20)

        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 8.78
        ,'s1.sp'           : 2640
        ,'s1.stop'         : 1.733

        ,'s2.buff'         : ('self', 0.25, 5)
        ,'s2.sp'           : 4101
        ,'s2.stop'         : 1
        }




if __name__ =='__main__':
    import run
    run.this_character()
