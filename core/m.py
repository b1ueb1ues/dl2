import __init__
from core.ctx import *
from core.target import *


c = Conf()
c.target.name = 'dummy'
c.target.ele = 'light'
c.target.hp = 100000
c.target.od = 200
c.target.bk = 300
c.target.def_ = 10
c.target.od_def = 1
c.target.bk_def = 0.6
c.target.bk_time = 5

c._1p.name = '1p'
c._1p.ele = 'shadow'
c._1p.atk = 3000
c._1p.target = c.target

tar = Target(c.target)
tar.init()

class C():
    def __init__(this, conf, target):
        this.conf = conf
        this.Dp = Dmg_param(conf)
        this.Dc = Dmg_calc(this, target)
        hitattr = Conf()
        hitattr.name = 's1'
        hitattr.type = 's'
        hitattr.coef = 1.0
        hitattr.to_od = 1
        hitattr.to_bk = 1
        hitattr.killer = {}
        this.dmg = this.Dc(hitattr)
        print(this.dmg.calc())
        this.dmg()

c = C(c._1p, tar)

