import __init__
from core.ctx import *
from core.characterbase import *
from mod.bleed import *
from mod.afflic import *
from mod.skillupgrade import *


class Ieyasu(Character):
    def dconf(this):
        return {
        'slot.a': 'RR+JotS',
        'acl.cancel' : """
            #bs = this.Bleed.stacks()
            `s1
            `s2, x=5 and bs > 0
            `s3
            `fsf, x=5
        """,
        }

    def conf(this):
        return {
         'star'            : 5
        ,'ele'             : 'shadow'
        ,'wt'              : 'blade'
        ,'atk'             : 521
        ,'a1'              : ('cc', 0.10, 'hp70')
        ,'a3'              : ('cd', 0.20)

        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 9.52
        ,'s1.recovery'     : 4.1
        ,'s1.sp'           : 2467

        ,'s2.sp'           : 7913
        ,'s2.recovery'     : 1
        }

    def init(this):
        this.Bleed = Bleed(this)
        this.bleed = this.Bleed('s1',0.8,1.44)
        this.bleed.dot.ks.on_end.append(this.bleed_end)
        this.s2_buff = this.Selfbuff('s2', 0, 'cc')

    def s1_proc(this):
        if this.bleed() > 0:
            this.s2_buff.set(0.15)

    def bleed_end(this):
        this.s2_buff.set(0)


    def s2_proc(this):
        this.s2_buff(15)


if __name__ =='__main__':
    import run
    run.this_character(mass=1)
