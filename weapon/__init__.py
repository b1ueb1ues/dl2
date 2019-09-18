if __package__ is None or __package__ == '':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from weapon.weaponbase import *

#from weapon import axe
from weapon import blade
#from weapon import bow
#from weapon import dagger
#from weapon import lance
#from weapon import staff
#from weapon import sword
#from weapon import wand

type_ = {
        0:0
#    , 'axe'    : axe
    ,'blade'  : blade
#    ,'bow'    : bow
#    ,'dagger' : dagger
#    ,'lance'  : lance
#    ,'staff'  : staff
#    ,'sword'  : sword
#    ,'wand'   : wand
}
