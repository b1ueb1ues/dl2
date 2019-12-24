import __init__
from core.ctx import *
from core.characterbase import *
from mod.bleed import *


class Victor(Character):
    def dconf(this):
        conf = {
            'acl.cancel' : """
            #bs = this.Bleed.stacks()
            `s1
            `s2, x=5
            `s3, x=5
            """
        }
        if 'bow' in this.ex:
            conf['slot.a'] = 'HoH+JotS'
        return conf

    def conf(this):
        return {
         'star'            : 5
        ,'ele'             : 'wind'
        ,'wt'              : 'blade'
        ,'atk'             : 494
        ,'a1'              : ('atk', 0.13, 'hp70')
        ,'a3'              : ('bt', 0.30)

        ,'s1.hit'          : [(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1')]
        ,'s1.attr.h1.coef' : 1.9
        ,'s1.sp'           : 2838
        ,'s1.stop'         : 2.267

        ,'s2.hit'          : [(0,'h1')]
        ,'s2.attr.h1.coef' : 9.57
        ,'s2.sp'           : 7500
        ,'s2.stop'         : 2.567
        }

    def init(this):
        this.Bleed = Bleed(this)
        this.bleed = this.Bleed('s1',0.8,1.46)

    def s1_proc(this):
        this.bleed()


if __name__ =='__main__':
    import run
    run.this_character(mass=1)
