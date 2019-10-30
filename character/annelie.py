import __init__
from core.ctx import *
from core.characterbase import *
from mod.energy import *
from mod.skillshift import *
from mod.afflic import *


class Annelie(Character):
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
        ,'ele'     : 'light'
        ,'wt'      : 'lance'
        ,'atk'     : 483
        ,'a1'      : ('sd', 0.35, 'hp70')

        ,'s1.recovery'        : 2.1
        ,'s1.sp'              : 3051
        ,'s1.attr.h1.coef'    : 0.1
        ,'s1.attr.h2.coef'    : 8.14
        ,'s1.hit'             : [
            (1,'h1'),(1,'h2')]

        ,'s12.recovery'        : 2.1
        ,'s12.attr.h1.coef'    : 0.1
        ,'s12.attr.h2.coef'   : 4.07
        ,'s12.hit'            : [
            (1,'h1'),(1,'h2'),
            (1,'h1'),(1,'h2')]

        ,'s13.recovery'        : 2.1
        ,'s13.attr.h1.coef'    : 0.1
        ,'s13.attr.h2.coef'   : 3.54
        ,'s13.hit'            : [
            (1,'h1'),(1,'h2'),
            (1,'h1'),(1,'h2'),
            (1,'h1'),(1,'h2') ]

        ,'s2.hit'             : [
            (0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),
            (0,'h1'),(0,'h1'),(0,'h1'),(0,'h1'),(0,'h1')
            ]
        ,'s2.attr.h1.coef'    : 0.82962
        ,'s2.recovery' : 3.6
        ,'s2.sp'       : 10206
        }

    def init(this):
        this.stance = 0
        this.ss = Skillshift(this, 1, this.conf['s12'], this.conf['s13'])

    def s1_end(this):
        if this.stance == 0:
            this.Energy.self(1)
            this.stance = 1
        elif this.stance == 1:
            this.Energy.self(2)
            this.stance = 2
        elif this.stance == 2:
            this.stance = 0

    def s2_end(this):
        this.Energy.team(2)


if __name__ == '__main__':
    import run
    run.this_character()
