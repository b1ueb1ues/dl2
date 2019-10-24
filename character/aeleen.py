import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Aeleen(Character):
    def dconf(this):
        conf = {
        'acl.cancel' : """
            `s1
            `fs, x=5
        """,
        }
        return conf

    def conf(this):
        return {
         'star'            : 4
        ,'ele'             : 'wind'
        ,'wt'              : 'lance'
        ,'atk'             : 470
        ,'a1'              : ('bt', 0.25)

        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 8.38
        ,'s1.recovery'     : 1.8
        ,'s1.sp'           : 2579

        ,'s2.sp'           : 8534
        ,'s2.buff'         : ('team', 0.15, 15, 'def')
        ,'s2.recovery'     : 1
        }




if __name__ =='__main__':
    import run
    run.this_character()
