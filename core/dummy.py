import __init__
from core.ctx import *
from core.targetbase import *

class Dummy(Target):
    def config(this, conf):
        conf.name = 'dummy'
        conf.ele = 'light'
        conf.hp = 1000000
        conf.od = 10000
        conf.bk = 10000
        #conf.ks = ['hms']


if __name__ == '__main__':


    print('!')
    #logset(['od','bk','debug'])
    logset(['debug'])
    tar = Dummy()
    tar.init()

    dmg = lobject()
    dmg.dmg = 100
    dmg.to_bk = 1
    dmg.to_od = 1
    dmg.name = 'fs'
    dmg.src = '1p'

    def foo(t):
        tar.dt(dmg)
        log('debug', '%d, %d, %d'%(tar.hp, tar.od, tar.bk))
        t(1)
    Timer(foo)(1)

    Timer.run(30)

    logcat()


