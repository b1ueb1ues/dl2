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
        conf.s1.hit = [
                (0.4, 'h1'), 
                (0.5, 'h1'), 
                (0.6, 'h1'),
                (0.8, '_h2'),
                ]    # dict {float timing: idx attr}
        conf.s1.attr.h1.coef = 2
        conf.s1.attr.h1.to_od = 0.5
        conf.s1.attr.h1.to_bk = 2
        conf.s1.attr._h2.coef = 2
        conf.s1.attr._h2.killer = {'bk':1}

        conf.s2.sp = 4500
        conf.s2.recovery = 2.5
        conf.s2.buff = ('self', 0.2, 10, 'spd')

        conf.s3.hit = [
                (0.15, 'h1')
                ]
        conf.s3.attr.h1.coef = 0
        conf.s3.sp = 8000
        conf.s3.debuff = ('debuff', 0.15, 10)

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

        import config.weapon
        wtconf = Conf( config.weapon.wtconf[this.conf.wt] )
        this.x1 = this.Combo('x1', this, wtconf.x1)
        this.x2 = this.Combo('x2', this, wtconf.x2)
        this.x3 = this.Combo('x3', this, wtconf.x3)
        this.x4 = this.Combo('x4', this, wtconf.x4)
        this.x5 = this.Combo('x5', this, wtconf.x5)
        this.x1.init()
        this.x2.init()
        this.x3.init()
        this.x4.init()
        this.x5.init()
        this.a_x = [this.x1, this.x2, this.x3, this.x4, this.x5, this.x1]

        #this.fs = this.Fs('fs', this, this.conf.fs)
        #this.fs.init()
        Event('idle')(this.x)


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
        this.Combo = Combo(this)
        this.Fs = Fs(this)

    
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
            this.logsp('%s, %s'%(this.name, name), sp,
                    '%d/%d, %d/%d, %d/%d'%(\
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max) 
                    )


    def x(this, e):
        doing = this.Action.doing.name
        if doing[0] == 'x':
            this.a_x[int(doing[1])]()
        else:
            this.a_x[0]()


if __name__ == '__main__':
    from dummy import *
    import benchmark
    logset('act')
    logset('buff')
    logset('dmg')
    logset('sp')
    logset('s')
    logset('x')
    logset('fs')
    #logset('od')
    #logset('bk')
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

        def foo(t):
            n = now()
            if n == 1:
                c.x1()
            elif n == 4:
                c.s2.sp.cur = 5000
                c.s2()
            elif n == 6.2:
                c.s2.sp.cur = 5000
                c.s2()
            elif n == 7:
                c.s1.sp.cur = 5000
                c.s1()
            elif n == 11:
                c.s3.sp.cur = 8000
                c.s3()
            elif n == 14:
                c.s3.sp.cur = 8000
                c.s3()
            #elif n == 20:
            #    c.fs()

        Timer(foo)(1)
        Timer(foo)(4)
        Timer(foo)(6.2)
        Timer(foo)(7)
        Timer(foo)(11)
        Timer(foo)(14)
        Timer(foo)(20)
        Timer.run()
    foo()
    #benchmark.run(foo)
    logcat()

