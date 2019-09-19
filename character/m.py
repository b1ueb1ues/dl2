import __init__
from core.ctx import *
from target.dummy import *
from character.mikoto import *
from character.elisanne import *

tar = Dummy()
tar.init()

c = Mikoto()
c.tar(tar)
c.init()

c2 = Elisanne()
c2.tar(tar)
c2.init()

