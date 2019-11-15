if __package__ is None or __package__ == '':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from basecombo import axe
from basecombo import blade
from basecombo import bow
from basecombo import dagger
from basecombo import lance
from basecombo import staff
from basecombo import sword
from basecombo import wand

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

