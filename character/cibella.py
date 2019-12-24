import __init__
from core.ctx import *
from core.characterbase import *


class Cibella(Character):
    def dconf(this):
        conf = {
        'slot.d' : 'DJ',
        'acl.cancel' : """
            `s2
            `s3
            `fs, x=5
        """,
        }
        return conf

    def conf(this):
        return {
         'star'            : 3
        ,'ele'             : 'water'
        ,'wt'              : 'lance'
        ,'atk'             : 437
        ,'a1'              : ('bt', 0.25)

        ,'s1.stop'         : 1
        ,'s1.sp'           : 2920

        ,'s2.hit'          : [(0,'h1'),(0,'h1')]
        ,'s2.attr.h1.coef' : 3.43
        ,'s2.sp'           : 5000
        ,'s2.stop'         : 1.45
        }



if __name__ =='__main__':
    import run
    run.this_character()
