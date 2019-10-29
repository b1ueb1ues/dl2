import __init__
from core.ctx import *
from core import dmg


class Dot_group():
    def __init__(this, host):
        this.host = host
        if 'Dot_group' not in this.host.mod:
            this.host.mod['Dot_group'] = this

    def __call__(this, classname, iv):
        return _Dot_group(this.host, classname, iv)
    

class _Dot_group():
    def __init__(this, host, classname, iv):
        this.host = host
        this.classname = classname
        this.iv = iv

        this._dmg = dmg._Dmg()
        this._dmg.to_od = 0
        this._dmg.to_bk = 0
        this._dmg.hit = 0

        this.stacks = 0
        this.all_stacks = []

        this.log = Logger('dot')
        this.ks = host.Passive('ks_'+classname, 1, 'ks', classname)
        this.t_tick = Timer(this.tick_proc)


    def reset(this):
        this.t_tick.off()
        tmp = []
        for i in this.all_stacks:
            tmp.append(i)
        for i in tmp:
            i.dot_end_proc(0)
            i.t_dot_end.off()

    def tick_proc(this, t):
        #stacks = this._static.stacks
        for i in this.all_stacks:
            this.host.dt_no_od(i._dmg)
        t()

    def __call__(this, src, name, coef, duration=None):
        return _Dot(this, src, name, coef, duration)


class _Dot():
    def __init__(this, static, src, name, coef, duration):
        this._static = static
        this.src = src
        this.name = name
        this.coef = coef
        this.duration = duration

        this.classname = static.classname
        this.iv = static.iv

        this._dmg = dmg._Dmg()
        this._dmg.name = '%s_%s'%(name, this.classname)
        this._dmg.hostname = src.name
        this._dmg.to_bk = 0
        this._dmg.to_od = 0
        this._dmg.hit = 0
        dmgconf = {
                 'coef' : coef
                ,'type' : 's'
                }
        this.srcname = src.name
        this.dmgname = this._dmg.name
        this.Dc = this.src.Dmg(dmgconf)
        this.t_dot_end = Timer(this.dot_end_proc)
        this.log = Logger('dot')


    def dot_end_proc(this, t):
        idx = this._static.all_stacks.index(this)
        this._static.all_stacks.pop(idx)
        this._static.stacks -= 1
        if this.log:
            this.log(this._static.host.name, this.classname,
                    'stack_end', "dot stack <%d>"%this._static.stacks)
        if this._static.stacks < 0:
            print('err in dot_end_proc')
            raise
        if this._static.stacks == 0:
            this._static.t_tick.off()
            this._static.ks.off()


    def __call__(this):
        this._dmg.dmg = this.Dc.calc()

        if this.log:
            this.log(this.srcname, this.dmgname, 'apply',
                    '%s, %d'%(this._static.host.name, this._dmg.dmg))

        this._static.all_stacks.append(this)
        this.t_dot_end(this.duration)
        if this._static.stacks == 0:
            this._static.t_tick(this.iv)
            this._static.ks()
        this._static.stacks += 1
        if this.log:
            if this._static.stacks > 1:
                this.log(this._static.host.name, this.classname,
                        'stack_add', "dot stack <%d>"%this._static.stacks)
