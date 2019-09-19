if __package__ is None or __package__ == '':
    import os
    os.sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dragon.dragonbase import *

from dragon.flame import *
from dragon.water import *
from dragon.wind import *
from dragon.light import *
from dragon.shadow import *
