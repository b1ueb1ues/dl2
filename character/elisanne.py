import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Elisanne(Character):
    def dconf(this):
        conf = {
         'slot.w'  : 'c534_water'
        ,'slot.d'  : 'DJ'
        ,'slot.a1' : 'BB'
        ,'slot.a2' : 'JotS'
        ,'acl.cancel' : """
            `s1
            `s2, fs=1
            `fs, x=5
        """
        }
        if 'bow' in this.ex:
            conf['acl.cancel'] = """
                `s1
                `s2
            """
        return conf

    def conf(this):
        return {
         'name'            : 'Elisanne'
        ,'star'            : 4
        ,'ele'             : 'water'
        ,'wt'              : 'lance'
        ,'atk'             : 460
        ,'a1'              : ('bt', 0.25)

        ,'s1.recovery'     : 1
        ,'s1.sp'           : 3817
        ,'s1.buff'         : ('team', 0.20, 15)

        ,'s2.sp'           : 5158
        ,'s2.recovery'     : 1.9
        ,'s2.hit'          : [(0,'h1')]
        ,'s2.attr.h1.coef' : 7.54
        }




if __name__ =='__main__':
    import run
    run.this_character()
