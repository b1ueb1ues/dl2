import __init__
from core.ctx import *
from core.buff import *
from core.action import *


class Character(object):
    def default(this, conf):
        conf.name = 'characterbase'
        conf.star = 4
        conf.ele = 'flame'
        conf.wt = 'sword'
        conf.atk = 500
        conf.a1 = ('hp70', 'atk', 10)
        conf.a2 = ('resist', 'stun', 100)
        conf.a3 = ('hit15', 'cc', 10)
        conf.slot.w = 'c534'
        conf.slot.d = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'FP'
        conf.ex = ['blade', 'wand']

    def __init__(this, conf=None):
        tmp = Conf()             
        this.default(tmp)    # conf prior
        this.config(tmp)     # default < class < param
        if conf:
            tmp(conf)
            conf(tmp)
            tmp = conf
        this.conf = tmp
        this.conf.sync_characterbase = this.sync


    # after settle down all config
    def init(this):
        this.classinit()


    def classinit(this):
        this.Dp = Dmg_param(this.conf)

        this.Passive = Passive(this.Dp)
        this.Buff = Buff(this.Dp)

        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)

        this.Action = Action(this)


    def sync(this, c, cc):
        this.name = c.name
        this.base_atk = c.atk
        if c.wt in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8
        this.atk = 2000


    def tar(this, target):
        this.target = target
        this.Dmg = Dmg_calc(this, target)
