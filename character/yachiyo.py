import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from target.mg import *
from mod.afflic import *
from mod.fs_alt import *


class Yachiyo(Character):
    def dconf(this):
        return {
         'slot.w'          : 'c534_light'
        ,'slot.d'          : 'Cupid'
        ,'slot.a1'         : 'RR'
        ,'slot.a2'         : 'SS'
        ,'acl.cancel' : '''
            `s1
            `s2, x=5
            `s3, fsc
            `fs, x=5
        '''
        }

    def conf(this):
        return {
         'name'            : 'Yachiyo'
        ,'star'            : 4
        ,'ele'             : 'light'
        ,'wt'              : 'blade'
        ,'atk'             : 501
#        ,'a1'              : ('skill_link', 0.15, 'def')
        ,'a3'              : ('k', 0.20, 'paralysis')

        ,'s1.hit'          : [(0,'h1'),(1,'h1')]
        ,'s1.attr.h1.coef' : 4.32
        ,'s1.recovery'     : 2.4
        ,'s1.sp'           : 2567

        ,'s2.sp'           : 4139
        ,'s2.recovery'     : 1
        }

    def init(this):
        this.Afflic = Afflic(this)
        this.para = this.Afflic['paralysis']('s1', 1.00, 0.66)
        this.ss = this.Selfbuff('s2',0,'')
        fsaconf = Conf()
        fsaconf({
              'fs.hit'          : [(0.15, 'h1')]
            , 'fs.attr.h1.coef' : 7.82
            , 'fs.attr.h1.to_bk': 1.5
            , 'fs.sp'           : 200
            , 'fs.startup'      : 0.37
            , 'fs.recovery'     : 0.85
            , 'fs.proc'  : [this.fsa_proc]

            , 'x1fs.startup'    : 0.68
            })
        this.fsa = Fs_alt(this, fsaconf.get, this.ss)

    def fsa_proc(this):
        this.fsa.off()

    def s1_proc(this):
        this.para()

    def s2_proc(this):
        this.fsa(-1)


if __name__ =='__main__':
    logset(['buff','dmg','bk','sp'])
    logset('all')
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

    #logset([])
    Ctx()
    #tar = water()
    tar = dummy()
    tar.init()

    c = Yachiyo(root)
    c.tar(tar)
    c.init()

    d = 120
    Timer.run(d)
    logcat()
    d = Skada.sum()
    print(' dps',d['Yachiyo']['dmg']/now())
    print('odps',d['Yachiyo']['odmg']/tar.od_count)
    print(Skada._skada)

