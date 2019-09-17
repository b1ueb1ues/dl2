if __package__ is None or __package__ == '':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.weapon import axe
from config.weapon import blade
from config.weapon import bow
from config.weapon import dagger
from config.weapon import lance
from config.weapon import staff
from config.weapon import sword
from config.weapon import wand

wtconf = {
    'axe'    : axe.conf
  , 'blade'  : blade.conf
  , 'bow'    : bow.conf
  , 'dagger' : dagger.conf
  , 'lance'  : lance.conf
  , 'staff'  : staff.conf
  , 'sword'  : sword.conf
  , 'wand'   : wand.conf
}

