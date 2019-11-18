import __init__
from core.ctx import *
from core.characterbase import *

class Malka(Character):
    def dconf(this):
        conf = {
            'acl.cancel': """
                `s1
                `s2
                `s3
                `fs, x=5 
            """,
        }
        if 'bow' in this.ex:
            conf['slot.a'] = 'RR+JotS'
        return conf

    def conf(this):
        return {
         'star'    : 3
        ,'ele'     : 'light'
        ,'wt'      : 'lance'
        ,'atk'     : 459
        ,'a3'      : ('prep', '50%')

        ,'s1.recovery'     : 1.4
        ,'s1.sp'           : 2556
        ,'s1.hit'          : [(0,'h1')] * 2
        ,'s1.attr.h1.coef' : 3.81

        ,'s2.recovery'     : 1
        ,'s2.sp'           : 6610
        ,'s2.buff'         : ('team', 0.10, 15, 'atk')
        }


if __name__ == '__main__':
    import run
    run.this_character()
