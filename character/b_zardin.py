import __init__
from core.ctx import *
from core.characterbase import *
from mod.energy import *


class B_Zardin(Character):
    def dconf(this):
        if 0:
            conf = {
            'slot.a' : 'RR+JotS',
            'acl.cancel' : """
                `s1
                `fsf, x=5
            """,
            }
        else:
            conf = {
            'slot.a' : 'RR+JotS',
            'acl.cancel' : """
                `s3, this.Energy() = 5
                `s1
                `s2, x=5 and this.Energy() < 4
                `fsf, x=5
            """,
            }
            #conf['slot.w'] = 'c434_light'
        return conf

    def conf(this):
        return {
         'star'            : 5
        ,'ele'             : 'light'
        ,'wt'              : 'blade'
        ,'atk'             : 517
        ,'a3'              : ('sd', 0.35, 'hp70')

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 3.16
        ,'s1.sp'           : 3080
        ,'s1.recovery'     : 2.178

        ,'s2.sp'           : 5000
        ,'s2.recovery'     : 1.633
        }

    def s1_end(this):
        this.Energy.self(1)

    def s2_end(this):
        this.Energy.self(2)



if __name__ =='__main__':
    import run
    run.this_character()
