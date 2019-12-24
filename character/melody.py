import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Melody(Character):
    'no s2'
    def dconf(this):
        conf = {
         'slot.a' : 'BB+HG'
        ,'acl.cancel' : """
            `s1
            `fsf, x=5
        """
        }
        return conf

    def conf(this):
        return {
         'star'            : 3
        ,'ele'             : 'wind'
        ,'wt'              : 'blade'
        ,'atk'             : 470
        ,'a1'              : ('cc', 0.08, 'hp100')

        ,'s1.buff'         : ('team', 0.15, 15)
        ,'s1.sp'           : 2987
        ,'s1.stop'         : 1

        ,'s2.hit'          : [(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s2.attr.h1.coef' : 2.64
        ,'s2.sp'           : 4784
        ,'s2.stop'         : 2.733
        }




if __name__ =='__main__':
    import run
    run.this_character(mass=0, verbose=-2)
