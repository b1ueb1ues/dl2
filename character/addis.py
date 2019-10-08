import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from target.mg import *
from mod.bleed import *
from mod.afflic import *
from mod.skillupgrade import *


class Addis(Character):
    def conf(this):
        return {
         'name'            : 'Addis'
        ,'star'            : 4
        ,'ele'             : 'wind'
        ,'wt'              : 'blade'
        ,'atk'             : 509
        ,'a1'              : ('bk', 0.25)
        ,'a3'              : ('k', 0.08, 'bleed')

        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 7.54
        ,'s1.recovery'     : 2.4
        ,'s1.sp'           : 2537
        ,'s12.proc'        : [this.s12_proc]

        ,'s2.sp'           : 4877
        ,'s2.recovery'     : 1

        ,'slot.w'          : 'c534_wind'
        ,'slot.d'          : 'Vayu'
        ,'slot.a1'         : 'RR'
        ,'slot.a2'         : 'BN'
        ,'acl.cancel' : """
            #bs = this.Bleed.stacks()
            `s2, s1.sp.cur >= s1.sp.max-260 and bs != 3
            `s1, s2.sp.cur < s2.sp.max and bs != 3
            `s3, not this.ss.get() and x=5
            `fs, this.ss.get() and x=4 and s1.sp.cur>=s1.sp.max-200
            `fsf, x=5
        """
        ,'acl.other' :"""
            #bs = this.Bleed.stacks()
            `s1, e.type=='silence' and s2.sp.cur < s2.sp.max and bs != 3
        """
        }

    def init(this):
        this.Afflic = Afflic(this)
        this.Bleed = Bleed(this)
        this.poison = this.Afflic['poison']('s1', 1.00, 0.53)
        this.bleed = this.Bleed('s1',0.8,1.32)
        this.ss = this.Selfbuff('s2',0.25)
        this.su = Skillupgrade(this,1,this.conf['s12'], this.ss)

    def s1_proc(this):
        this.poison()

    def s12_proc(this):
        this.bleed()

    def s2_proc(this):
        this.su(10)


if __name__ =='__main__':
    logset(['buff','dmg','bk'])
    #logset(['buff','dmg','bk','sp'])
    #logset('afflic')
    #logset('act')
    #logset('rotation')
    #logset('x')
    #logset('fs')
    #logset('act')
    #logset('s')
    #logset(['buff','debug','dmg','hit'])
    root = {}
    #root = {'ex':['bow']}

    logset([])
    sample = 1000
    for i in range(sample):
        Ctx()
        #tar = water()
        tar = dummy()
        tar.init()

        c = Addis(root)
        c.tar(tar)
        c.init()

        d = 120
        Timer.run(d)
    logcat()
    print('dps',Skada.sum()['Addis']['dmg']/d/sample)
    print(Skada._skada)

