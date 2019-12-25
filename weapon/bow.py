import __init__
from weapon import *

class c534_flame(Weapon):
    ele = ['flame','water','wind']
    wt = 'bow'
    atk = 518
    s3 = {
        "buff"  : ('self',0.25, 10, 'cc'),
        "sp"    : 7316  ,
        "stop"  : 1
        }
c534_water = c534_flame
c534_wind = c534_flame

class c534_light(Weapon):
    ele = ['light']
    wt = 'bow'
    atk = 534
    s3 = {
        "dmg"      : 9.49     ,
        "sp"       : 8075     ,
        "startup"  : 0.1      ,
        "recovery" : 2.25     ,
        }


class c534_shadow(Weapon):
    ele = ['shadow']
    atk = 534
    wt = 'bow'
    s3 = {
        "dmg"      : 3*3.16   ,
        "sp"       : 7501     ,
        "startup"  : 0.1      ,
        "recovery" : 2.75     ,
        }
