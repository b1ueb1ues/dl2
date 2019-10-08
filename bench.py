from core.ctx import *
from target.hms import *
from character.mikoto import *
from character.natalie import *
from character.elisanne import *
from core import benchmark
from core.skada import *


def foo():
    Ctx()
    tar = hms()
    tar.init()

    c = Natalie()
    c.tar(tar)
    c.init()

    c2 = Elisanne()
    c2.tar(tar)
    c2.init()

    Timer.run(120)

logset([])
benchmark.run(foo, 200)

#logcat()
Skada.sum()
