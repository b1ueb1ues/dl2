import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Alain(Character):
    def dconf(this):
        conf = {
        'acl.cancel' : """
            `s1
            `s2
            `s3
            `fs, x=5
        """,
        }
        return conf

    def conf(this):
        return {
         'star'            : 3
        ,'ele'             : 'flame'
        ,'wt'              : 'lance'
        ,'atk'             : 438

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 2.54
        ,'s1.stop'         : 1.9
        ,'s1.sp'           : 2581

        ,'s2.hit'          : [(0,'h1'),(0,'h1')]
        ,'s2.attr.h1.coef' : 3.43
        ,'s2.sp'           : 5112
        ,'s2.stop'         : 1.4
        }




if __name__ =='__main__':
    import run
    run.this_character()
