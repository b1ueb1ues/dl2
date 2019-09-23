import __init__
from core.ctx import *
from core.characterbase import *
from target.dummy import *


class Elisanne(Character):
    conf = {
         'name'            : 'Elisanne'
        ,'star'            : 4
        ,'ele'             : 'water'
        ,'wt'              : 'lance'
        ,'atk'             : 460
        ,'a1'              : ('bt', 0.25)

        ,'s1.recovery'     : 1
        ,'s1.sp'           : 3817
        ,'s1.buff'         : ('s1', 0.20, 15)

   #     ,'s2.sp'           : 5158
   #     ,'s2.recovery'     : 1.9
   #     ,'s2.hit'          : [(0,'h1')]
   #     ,'s2.attr.h1.coef' : 7.54

        ,'slot.w'          : 'c534_water'
        ,'slot.d'          : 'DJ'
        ,'slot.a1'         : 'BB'
        ,'slot.a2'         : 'JotS'
        }


if __name__ =='__main__':
    #logset(['buff','dmg','od','bk'])
    logset(['buff','dmg','bk','sp'])
    #logset('x')
    logset('fs')
    #logset('act')
    logset('s')
    #logset(['buff','debug','dmg','hit'])

    tar = Dummy()
    tar.init()

    c = Elisanne()
    c.tar(tar)
    c.init()

    Timer.run(60)
    logcat()
