import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from mod.energy import *
import copy
import random


class Natalie(Character):
    def dconf(this):
        conf = {
        'acl.cancel': """
            `s2, x=5
            `s1
            `s3, fs
            `s3, x=5 and s1.sp.cur < s1.sp.max-200
            `fs, x=5 and s1.sp.cur+212>=s1.sp.max and s1.sp.cur<=s1.sp.max
            `fs, x=5 and s1.sp.cur > 3000 and s3.sp.cur>=s3.sp.max
            `fsf, x=5
        """,
        'acl.other':"""
            `s1
        """,
        }
        return conf

    def conf(this):
        return {
         'star'    : 5
        ,'ele'     : 'shadow'
        ,'wt'      : 'blade'
        ,'atk'     : 521
        ,'a1'      : ('extra_energy', 0.80)
        #,'a3'      : this.a3

        ,'s1.hit'             : [(0,'h1'),(1,'h1'),(1.2,'h1')]
        ,'s1.attr.h1.coef'    : 3.54
        ,'s1.attr.h1.missile' : [0]
        ,'s1.on_hit'          : this.s1_hit
        ,'s1.sp'              : 3247
        ,'s1.stop'            : 1.778

        ,'s2.stop'     : 1
        ,'s2.sp'       : 6000
        }

    def init(this):
        this.hp = 100

        
    def s1_end(this):
        this.Energy.self(1)


    def s1_hit(this, dmg):
        crisis = (100.0-this.hp)/100.0
        crisis = crisis * crisis * 1
        tmp = dmg.copy()
        tmp.dmg = int(dmg.dmg * crisis)
        tmp.name = 's1_crisis'
        this.target.dt(tmp)


    def s2_proc(this):
        if this.hp == 100:
            this.hp = 20
            this.Passive('a3',0.2)()
            this.Passive('a3',0.1,'spd')()
        elif this.hp == 20:
            this.Selfbuff('s2',0.15)(10)



if __name__ == '__main__':
    import run 
    run.this_character(mass=1)
