import __init__
from weapon import *

class c534_flame(Weapon):
    ele = ['flame']
    wt = 'blade'
    atk = 572
    s3 = {
        "hit"           : [(0,'h1'), (0,'h1'), (0,'h1')]
        ,"attr.h1.coef" : 3.54
        ,"sp"           : 8030
        ,"recovery"     : 2.65
    }

class c534_wind(Weapon):
    ele = ['wind']
    wt = 'blade'
    atk = 572
    s3 = {
        "hit"           : [(0,'h1'), (0,'h1'), (0,'h1')]
        ,"attr.h1.coef" : 3.54
        ,"sp"           : 8030
        ,"recovery"     : 2.65
    }


class c534_water(Weapon):
    ele = ['light']
    wt = 'blade'
    atk = 544


class c534_light(Weapon):
    ele = ['light']
    wt = 'blade'
    atk = 544


class c534_shadow(Weapon):
    ele = ['shadow']
    atk = 590
    wt = 'blade'
    s3 = {
        "hit"           : [(0,'h1'), (0,'h1'), (0,'h1'), (0,'h1'), (0,'h1')]
        ,"attr.h1.coef" : 2.13
        ,"sp"           : 7695
        ,"recovery"     : 2.65
    }

class c434_light(Weapon):
    ele = ['light', 'water']
    atk = 382
    wt = 'blade'
    s3 = {
        "hit"           : [(0,'h1')]
        ,"attr.h1.coef" : 9.66
        ,"sp"           : 8178
        ,"recovery"     : 1.95
    }

class v534_zephyr(Weapon):
    ele = ['flame']
    wt = 'blade'
    atk = 353
    a = [('k',0.2,'hms'), ('prep',0.5)]
