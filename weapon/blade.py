import __init__
from weapon import *

class c534_flame(Weapon):
    ele = ['flame','wind']
    wt = 'blade'
    atk = 572
    s3 = {
         "hit"          : [(0.28,'h1'), (0.65,'h1'), (1.1,'h1')]
        ,"attr.h1.coef" : 3.54
        ,"sp"           : 8030
        ,"stop"         : 2.57
    }

c534_wind = c534_flame


class c534_water(Weapon):
    ele = ['water','light']
    wt = 'blade'
    atk = 544

c534_light = c534_water


class c534_shadow(Weapon):
    ele = ['shadow']
    atk = 590
    wt = 'blade'
    s3 = {
        "hit"           : [(0,'h1'), (0,'h1'), (0,'h1'), (0,'h1'), (0,'h1')]
        ,"attr.h1.coef" : 2.13
        ,"sp"           : 7695
        ,"stop"         : 2.65
    }

class c434_light(Weapon):
    ele = ['light', 'water']
    atk = 382
    wt = 'blade'
    s3 = {
        "hit"           : [(0,'h1')]
        ,"attr.h1.coef" : 9.66
        ,"sp"           : 8178
        ,"stop"         : 1.95
    }

c434_water = c434_light

class v534_flame_zephyr(Weapon):
    ele = ['flame']
    wt = 'blade'
    atk = 353
    a = [('k',0.2,'hms'), ('prep',0.5)]
