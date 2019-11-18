import __init__
from core.ctx import *
from core.characterbase import *

class Ryozen(Character):
    def dconf(this):
        conf = {
            'acl.cancel': """
                `s2
                `s3
                `fs, x=5 
            """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 4
        ,'ele'     : 'light'
        ,'wt'      : 'lance'
        ,'atk'     : 444
        ,'a3'      : ('od',0.08)

        ,'s1.recovery'     : 1
        ,'s1.buff'         : ('team', 0.15, 15, 'def')
        ,'s1.sp' : 4367

        ,'s2.recovery'     : 2.6
        ,'s2.sp'           : 4855
        ,'s2.hit'          : [(0,'h1')]*5
        ,'s2.attr.h1.coef' : 1.51

        }


if __name__ == '__main__':
    import run
    run.this_character()
