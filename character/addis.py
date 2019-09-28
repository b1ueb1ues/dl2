import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from mod.bleed import *
from mod.afflic import *


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
        ,'s1.recovery'     : 1
        ,'s1.sp'           : 3817
        ,'s1.proc' : this.s1_proc

        ,'s2.sp'           : 5158
        ,'s2.recovery'     : 1
        ,'s2.buff'         : ('self', 0.25, 10)

        ,'slot.w'          : 'c534_wind'
        ,'slot.d'          : 'Vayu'
        ,'slot.a1'         : 'RR'
        ,'slot.a2'         : 'BN'
        ,'acl.cancel' : """
            `s1
            `s2
            `s3, x=5
            `fsf, x=5
        """
        }

    def init(this):
        this.Afflic = Afflic(this)
        this.Bleed = Bleed(this)
        this.poison = this.Afflic['poison']('s1', 1.00, 0.53)

    def s1_proc(this):
        this.poison()



if __name__ =='__main__':
    #logset(['buff','dmg','od','bk'])
    logset(['buff','dmg','bk','sp'])
    #logset('x')
    #logset('fs')
    #logset('act')
    #logset('s')
    #logset(['buff','debug','dmg','hit'])
    root = {}
    #root = {'ex':['bow']}

    tar = Dummy()
    tar.init()

    c = Addis(root)
    c.tar(tar)
    c.init()

    Timer.run(60)
    logcat()
