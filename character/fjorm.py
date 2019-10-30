import __init__
from core.ctx import *
from core.characterbase import *

class Fjorm(Character):
    'no counter damage'
    def dconf(this):
        conf = {
            'acl.cancel': """
                #e = this.Energy.stacks()
                `s1, s2.sp.cur<=10000
                `s1, s=2
                `s2
                `s3
                `fs, x=5 
            """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 5
        ,'ele'     : 'water'
        ,'wt'      : 'lance'
        ,'atk'     : 508
        #,'a1'      : ('last_bravery')
        ,'a3'      : ('prep', '100%')

        ,'s1.recovery'     : 2.05
        ,'s1.sp'           : 2738
        ,'s1.hit'          : [(1,'h1'),(1,'h1')]
        ,'s1.attr.h1.coef' : 4.11

        ,'s2.recovery'     : 3.85
        ,'s2.hit'          : [(3,'h1')]
        ,'s2.attr.h1.coef' : 8.29
        ,'s2.sp'           : 4548
        }

if __name__ == '__main__':
    import run
    run.this_character()
