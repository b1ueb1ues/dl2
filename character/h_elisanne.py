import __init__
from core.ctx import *
from core.characterbase import *
from mod.skillshift import *


class H_Elisanne(Character):
    def dconf(this):
        conf = {
            'acl.cancel': """
                `s1
                `s2, x=5
                `s3
                `fs, x=5 
            """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 5
        ,'ele'     : 'light'
        ,'wt'      : 'lance'
        ,'atk'     : 483
        ,'a1'      : ('sd', 0.30)

        ,'s1.stop'            : 2.8
        ,'s1.sp'              : 2450
        ,'s1.attr.h1.coef'    : 1.15
        ,'s1.hit'             : [ (0,'h1'),
                                  (1,'h1'),(1,'h1'),(1,'h1'),
                                  (1,'h1'),(1,'h1'),(1,'h1')]

        ,'s12.on_end':[this.s1_buff]
        ,'s13.on_end':[this.s1_buff]

        ,'s2.hit'             : [
            (0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),
            (0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1')
            ]
        ,'s2.attr.h1.coef' : 0.83
        ,'s2.stop'     : 3.55
        ,'s2.sp'       : 5252
        }

    def init(this):
        this.stance = 0
        this.ss = Skillshift(this, 1, this.conf['s12'], this.conf['s13'])

    def s1_buff(this):
        this.Teambuff('s1',0.1)(15)

    def s2_proc(this):
        this.charge('s2', 500)



if __name__ == '__main__':
    import run
    run.this_character()
