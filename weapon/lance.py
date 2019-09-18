import __init__
from weapon import *

class c534_flame(Weapon):
    ele = ['flame','light','shadow']
    wt = 'lance'
    atk = 567
    s3 = {
        "hit"           : [(0,'h1'), (0,'h1')]
        ,"attr.h1.coef" : 4.61
        ,"sp"           : 8111
        ,"recovery"     : 1.9
    }

c534_light = c534_flame
c534_shadow = c534_flame

class c534_water(Weapon):
    ele = ['water','wind']
    wt = 'lance'
    att = 523

c534_wind = c534_water

