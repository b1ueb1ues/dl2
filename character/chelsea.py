import __init__
from core.ctx import *
from core.characterbase import *
from mod.skillshift import *

class Chelsea(Character):
    def dconf(this):
        conf = {
            'acl.cancel': """
                `s1
                `s2
                `s3
                `fs, x=4 
            """,
            'slot.a' : 'HoH+FoG',
        }
        return conf

    def conf(this):
        return {
         'star'    : 5
        ,'ele'     : 'flame'
        ,'wt'      : 'bow'
        ,'atk'     : 496
        ,'a1'      : ('atkspd', (0.20, 0.10), 'hp30')

        ,'s1.hit' : [(0.400,'h1'),
                     (0.933,'h2'),
                     (1.033,'h2'),
                     (1.133,'h2'),
                     (1.233,'h2'),
                     (1.333,'h2'),
                     (1.433,'h2')]
        ,'s1.attr.h1.coef'    : 1.36
        ,'s1.attr.h2.coef'    : 1.36
        ,'s1.attr.h2.missile' : [0.133]
        ,'s1.sp'              : 2960
        ,'s1.stop'            : 1.633

        ,'s2.buff'     : ('self', 0.3, 60)
        ,'s2.sp'       : 7000
        ,'s2.stop'     : 1
        }

    def init(this):
        this.stance = 0
        this.a3 = this.Selfbuff('a3', 0, 'atk')
        this.a3(-1)

    def s2_proc(this):
        this.a3.set(0.3)
        this.s2_buff = this.Selfbuff('s2', 0.3)(60)
        this.s2_buff.on_end.append(this.a3_stop)

    def a3_stop(this):
        this.a3.set(0)




if __name__ == '__main__':
    import run
    run.this_character()
