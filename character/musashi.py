import __init__
from core.ctx import *
from core.characterbase import *

class Musashi(Character):
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
         'star'            : 4
        ,'ele'             : 'wind'
        ,'wt'              : 'blade'
        ,'atk'             : 503
        ,'a1'              : ('lo', 0.40)
        ,'a3'              : ('od', 0.08)

        ,'s1.hit'          : [(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 4.32
        ,'s1.recovery'     : 2.0
        ,'s1.sp'           : 2567

        ,'s2.sp'           : 4430
        ,'s2.buff'         : ('self', 0.30, 5)
        ,'s2.recovery'     : 1
        }




if __name__ =='__main__':
    import run
    run.this_character()
