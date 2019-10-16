import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *
from amulet import *
from dragon import *
from weapon import *


class Plain_w(Weapon):
    ele = ['on']
    wt = 'blade'
    atk = 0

class Plain_d(Dragon):
    atk = 0
    ele = 'on'
    a = [('atk',0.6)]

class Plain_a1(Amulet):
    atk = 0
    a = [('sd',0.25)]

class Plain_a2(Amulet):
    atk = 0
    a = [('atk',0.13)]

class Faketeam(Character):
    def dconf(this):
        return {
         'slot.w'  : 'Plain_w'
        ,'slot.d'  : 'Plain_d'
        ,'slot.a1' : 'Plain_a1'
        ,'slot.a2' : 'Plain_a2'

        ,'acl.cancel': """
            `s1, x=5
            `s2, x=5
            `s3, x=5
            `fsf, x=5
        """
        }

    def conf(this):
        return {
         'name'    : 'Faketeam'
        ,'star'    : 5
        ,'ele'     : 'on'
        ,'wt'      : 'blade'
        ,'atk'     : 2000 * 2.25

        ,'s1.recovery'     : 1.9
        ,'s1.sp'           : 2500
        ,'s1.hit'          : [(0,'h1')]
        ,'s1.attr.h1.coef' : 10

        ,'s2.recovery'     : 1.9
        ,'s2.sp'           : 5000
        ,'s2.hit'          : [(0,'h1')]
        ,'s2.attr.h1.coef' : 10
        }
        

if __name__ == '__main__':
    #logset(['buff', 'dmg', 'od', 'bk'])
    logset(['buff', 'dmg', 'bk', 'sp'])
    #logset('x')
    logset('fs')
    #logset('act')
    logset('s')
    #logset(['buff','debug','dmg', 'hit'])

    tar = dummy()
    tar.init()

    c = Faketeam()
    c.tar(tar)
    c.init()

    d = 120
    Timer.run(d)
    logcat()
    print('dps',Skada.sum()['Faketeam']['dmg']/now())
    print(Skada._skada)
