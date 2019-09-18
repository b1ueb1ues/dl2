import __init__
from core.ctx import *
from core.buff import *
from core.action import *
from core.skill import *
from core import floatsingle
from ability import *
from amulet import *
from weapon import *
from dragon import *


class Conf_chara(Config):
    def default(this, conf):
        conf.name = 'characterbase'
        conf.star = 5
        conf.ele = 'flame'
        conf.wt = 'blade'
        conf.atk = 500
        conf.a1 = ('hp70'   , 'cc'   , 10  )
        conf.a3 = (''       , 'cc'   , 8   )

        conf.dodge.recovery = 0.7

        conf.ex = ['blade', 'wand']
        #conf.ex = ['blade']


    def sync(this, c):
        this.name     = c.name
        this.base_atk = c.atk
        this.wt       = c.wt
        this.ele      = c.ele
        this.star     = c.star
        this.ex       = c.ex
        if c.wt in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8
        if c.wt in ['axe'] :
            this.base_crit = 0.04
        else:
            this.base_crit = 0.02


    def config(this, c):
        this.config(c)


class Character(object):
    def __init__(this, conf=None):
        this.atk = 2000
        this.conf = Conf_chara(this, conf)
        this.hitcount = 0
        this.t_hitreset = Timer(this.hitreset)
        this.e_hit = Event('hit')

        this.logsp = Logger('sp')
        this.loghit = Logger('hit')

        this.child_init = this.init
        this.init = this.character_init


    def config(this, conf):
        pass


    # after settle down all config
    def character_init(this):
        this.classinit()
        this.listeners()
        this.setup()

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

        this.a_fs = this.Fs('fs', this, wtconf.fs)
        this.fs.init()
        this.fss = {}
        for i in range(1, 6):
            fsname = 'x%dfs'%i
            if fsname in wtconf:
                tmp = Conf(wtconf.fs)
                tmp(wtconf[fsname])
                wtconf[fsname](tmp)
                this.fss[fsname] = this.Fs('fs', this, wtconf[fsname])
            else:
                this.fss[fsname] = this.Fs('fs', this, wtconf.fs)
        if dfs in wtconf:
            tmp = Conf(wtconf.fs)
            tmp(wtconf.dfs)
            wtconf.dfs(tmp)
            this.fss['dfs'] = this.Fs('fs', this, wtconf.dfs)

        for i in this.fss:
            this.fss[i].init()

        this.child_init()

        this.e_idle = Event('idle')
        this.e_idle()


    def setup(this):
        this.Passive('base_crit_chance', this.base_crit, 'cc')()
        this.Passive('base_crit_damage', 0.7, 'cd')()

        this.a1 = this.Ability('chara_a1', *this.conf.a1)()
        this.a3 = this.Ability('chara_a3', *this.conf.a3)()

        this.d = this.Dragon(this.conf.slot.d)
        this.w = this.Weapon(this.conf.wt, this.conf.slot.w)
        this.a = this.Amulet(this.conf.slot.a1, this.conf.slot.a2)

        this.d.init()
        this.w.init()
        this.a.init()

        ex = {}
        for i in this.ex:
            ex[i] = 1
        ex[this.wt] = 1

        for i in ex:
            if i == 'blade':
                this.Passive('ex_blade',  0.10, 'atk', 'ex')()
            elif i == 'wand':
                this.Passive('ex_wand',   0.15, 'sd',  'ex')()
            elif i == 'dagger':
                this.Passive('ex_dagger', 0.10, 'cc',  'p')()
            elif i == 'bow':
                this.Passive('ex_bow',    0.15, 'sp',  'p')()

        from config import forte
        this.atk = this.base_atk * forte.c(this.ele, this.wt)
        this.atk += this.d.atk * forte.d(this.ele)
        this.atk += this.w.atk + this.a.atk


    def think_cancel(this, e):
        if e.hit == e.last:
            x = e.idx
        else:
            x = e.idx*10+e.hit
        #if e.idx == 5 and e.hit==e.last:
        #    this.fs()
        if this.s1.sp.cur >= this.s1.sp.max:
            this.think_s1()
        if this.s2.sp.cur >= this.s2.sp.max:
            this.think_s2()
        if this.s3.sp.cur >= this.s3.sp.max:
            this.think_s3()

    def think_s(this):
        pass

    def think_s1(this):
        this.s1()
    def think_s2(this):
        this.s2()
    def think_s3(this):
        this.s3()

    def think_fs(this):
        pass

    def listeners(this):
        if this.conf.rotation :
            Event('idle')(this.l_rotation)
        else:
            Event('idle')(this.x)
            Event('cancel')(this.think_cancel)


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

        this.Ability = Ability(this)
        this.Dragon = Dragon(this)
        this.Weapon = Weapon(this)
        this.Amulet = Amulet(this)

    
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
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )


    def charge_p(this, name, sp):
        if type(sp) == str and sp[-1] == '%':
            charge = int(sp[:-1]) / 100
        elif type(sp) == int :
            charge = sp
        elif type(sp) == float :
            charge = sp
        else:
            charge = 0

        this.s1.charge( floatsingle.ceiling(this.conf.s1.sp * charge) )
        this.s2.charge( floatsingle.ceiling(this.conf.s2.sp * charge) )
        this.s3.charge( floatsingle.ceiling(this.conf.s3.sp * charge) )
        if this.logsp:
            this.logsp('%s, %s'%(this.name, name), '%d%%'%(charge*100),
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )
        #this.think_pin('prep')


    def x(this, e):
        doing = this.Action.doing.name
        if doing[0] == 'x':
            this.a_x[int(doing[1])]()
        else:
            this.a_x[0]()


    def hit(this, count):
        if this.loghit:
            this.loghit('add', '%d+%d'%(this.hitcount, count) )
        this.hitcount += count
        this.t_hitreset(2)
        this.e_hit.hit = this.hitcount
        this.e_hit()


    def hitreset(this, t):
        this.hitcount = 0
        if this.loghit:
            this.loghit('reset', 0)
        this.e_hit.hit = 0
        this.e_hit()



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
    #logset([])

    def foo():
        Ctx()
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
        Timer.run(180)

    foo()
    #benchmark.run(foo, 2000)

    logcat()

