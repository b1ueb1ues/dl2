import __init__
from core.ctx import *
from core.characterbase import *

class Jakob(Character):
    'no bog'
    def dconf(this):
        conf = {
            'slot.d':'DJ',
            'acl.cancel': """
                `s1
                `fs, x=5 
            """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 3
        ,'ele'     : 'water'
        ,'wt'      : 'lance'
        ,'atk'     : 437
        ,'a3'      : ('prep', '50%')

        ,'s1.recovery'     : 1.65
        ,'s1.sp'           : 2738
        ,'s1.hit'          : [(1,'h1'),(1,'h1')]
        ,'s1.attr.h1.coef' : 4.11

        ,'s2.recovery'     : 1
        ,'s2.buff'         : ('team', 0.15, 15, 'def')
        }


if __name__ == '__main__':
    import run
    run.this_character()
