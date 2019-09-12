import __init__
from core.ctx import *
from core.buff import *
from core.action import *
from core.skill import *


class Character(object):
    def default(this, conf):
        conf.name = 'characterbase'
        conf.star = 5
        conf.ele = 'flame'
        conf.wt = 'blade'
        conf.atk = 500
        conf.a = []
        conf.a1 = ('hp70'   , 'cc'   , 10  )
        conf.a2 = ('resist' , 'stun' , 100 )
        conf.a3 = (''       , 'cc'   , 8   )

        conf.s1.sp = 4500       # int sp_max
        conf.s1.recovery = 84  # int recovery frames
        conf.s1.hit = { 
                0.4:'h1', 
                0.5:'h1', 
                0.6:'h1',
                0.8:'h2',
                }    # dict {float timing: idx hitattr}
        conf.s1.hitattr.h1.coef = 2
        conf.s1.hitattr.h2.coef = 3
        conf.s1.hitattr.h2.to_od = 2
        conf.s1.hitattr.h2.to_bk = 2

        conf.s2.sp = 4500
        conf.s2.recovery = 60
        conf.s2.buff = ('self', 0.2, 10, 'spd')

        conf.s3

        conf.slot.w = 'c534'
        conf.slot.d = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'FP'

        conf.ex = ['blade', 'wand']


    def __init__(this, conf=None):
        this.atk = 2000
        this.killer = {}

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
        this.s1 = this.Skill('s1', this, this.conf.s1)
        this.s2 = this.Skill('s2', this, this.conf.s2)
        this.s1.init()
        this.s2.init()


    def classinit(this):
        this.Dp = Dmg_param(this.conf)
        this.mod = this.Dp.get

        this.Passive = Passive(this.Dp)
        this.Buff = Buff(this.Dp)

        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)

        this.Action = Action(this)
        this.Action.spd = this.speed
        this.Skill = Skill(this)

    
    def speed(this):
        return this.mod('spd')


    def config(this, conf):
        pass


    def sync(this, c, cc):
        this.name = c.name
        this.base_atk = c.atk
        if c.wt in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8


    def tar(this, target):
        this.target = target
        this.Dmg = Dmg_calc(this, target)


if __name__ == '__main__':
    from dummy import *
    import benchmark
    logset('act')
    logset('buff')
    logset('dmg')
    logset('skill')
    logset('od')
    logset('bk')

    def foo():
        for i in range(1000):
            t = Dummy()
            t.init()
            c = Character()
            c.conf.name = 'c'
            c.tar(t)
            c.init()

            c.s2.sp.cur = 5000
            c.s2()
            c.s2()
            def foo(t):
                n = now()
                if n == 180:
                    c.s2()
                if n == 240:
                    c.s2.sp.cur = 5000
                    c.s2()
                if n == 420:
                    c.s1.sp.cur = 5000
                    c.s1()
            Timer(foo)(180)
            Timer(foo)(240)
            Timer(foo)(420)
            Timer.run()
    benchmark.run(foo)
    #logcat()

