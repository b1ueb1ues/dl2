import __init__
from core.ctx import *
from core.targetbase import *

class Hms(Target):
    def config(this, conf):
        conf.name = 'hms'
        conf.ele = 'wind'
        conf.hp = 863164
        conf.od = 258949
        conf.bk = 172632
        conf.ks = ['hms']
