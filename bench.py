from core.ctx import *
from target.hms import *
from character.mikoto import *
from character.elisanne import *
from core import benchmark


def foo():
    Ctx()
    tar = Hms()
    tar.init()

    c = Mikoto()
    c.tar(tar)
    c.init()

    c2 = Elisanne()
    c2.tar(tar)
    c2.init()

    Timer.run()

logset([])
benchmark.run(foo, 200)

logcat()
