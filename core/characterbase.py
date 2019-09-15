import __init__
from core.ctx import *
from core.buff import *
from core.action import *
from core.skill import *
from core import floatsingle


class Conf_chara(Config):
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
        conf.s1.recovery = 1.4  # int recovery frames
        conf.s1.hit = { 
                0.4:'h1', 
                0.5:'h1', 
                0.6:'h1',
                0.8:'h2',
                }    # dict {float timing: idx hitattr}
        conf.s1.hitattr.h1.coef = 2
        conf.s1.hitattr.h1.to_od = 0.5
        conf.s1.hitattr.h1.to_bk = 2
        conf.s1.hitattr.h2.coef = 2
        conf.s1.hitattr.h2.killer = {'bk':1}


        conf.s2.sp = 4500
        conf.s2.recovery = 1
        conf.s2.buff = ('self', 0.2, 10, 'spd')

        conf.s3.hit = {
                0.15:'h1'
                }
        conf.s3.hitattr.h1.coef = 0
        conf.s3.sp = 8000
        conf.s3.debuff = ('debuff', 0.15, 10)

        conf.x1.hit = {
                0:'h1'
                }

        conf.slot.w = 'c534'
        conf.slot.d = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'FP'

        conf.ex = ['blade', 'wand']


    def sync(this, c):
        this.name = c.name
        this.base_atk = c.atk
        if c.wt in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8


    def config(this, c):
        this.config(c)



class Character(object):
    def __init__(this, conf=None):
        this.atk = 2000
        this.conf = Conf_chara(this, conf)

        this.logsp = Logger('sp')


    def config(this, conf):
        pass


    # after settle down all config
    def init(this):
        this.classinit()
        this.s1 = this.Skill('s1', this, this.conf.s1)
        this.s2 = this.Skill('s2', this, this.conf.s2)
        this.s3 = this.Skill('s3', this, this.conf.s3)
        this.s1.init()
        this.s2.init()
        this.s3.init()


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
        this.Skill = Skill(this)

    
    def speed(this):
        return this.mod('spd')


    def tar(this, target):
        this.target = target
        this.Dmg = Dmg_calc(this, target)


    def charge(this, name, sp):
        sp = int(sp) * floatsingle.tofloat(this.mod('sp'))
        sp = floatsingle.tofloat(sp)
        sp = floatsingle.ceiling(sp)
        this.s1.charge(sp)
        this.s2.charge(sp)
        this.s3.charge(sp)
        if this.logsp :
            this.logsp(name, sp,'%d/%d, %d/%d, %d/%d'%(\
                this.s1.charged, this.s1.sp,
                this.s2.charged, this.s2.sp,
                this.s3.charged, this.s3.sp) )



if __name__ == '__main__':
    from dummy import *
    import benchmark
    logset('act')
    logset('buff')
    logset('dmg')
    logset('skill')
    logset('od')
    logset('bk')
    logset('debug')
    logset('dbg')

    def foo():
        t = Dummy()
        t.conf.od = 100
        t.conf.bk = 100
        t.conf()
        t.init()
        c = Character()
        c.conf.name = 'c'
        c.conf()
        c.tar(t)
        c.init()

        c.s2.sp.cur = 5000
        c.s2()
        c.s2()
        def foo(t):
            n = now()
            if n == 1:
                c.s2()
            if n == 4:
                c.s2.sp.cur = 5000
                c.s2()
            if n == 7:
                c.s1.sp.cur = 5000
                c.s1()
            if n == 11:
                c.s3.sp.cur = 8000
                c.s3()
            if n == 14:
                c.s3.sp.cur = 8000
                c.s3()
        Timer(foo)(1)
        Timer(foo)(4)
        Timer(foo)(7)
        Timer(foo)(11)
        Timer(foo)(14)
        Timer.run()
    foo()
    #benchmark.run(foo)
    logcat()

