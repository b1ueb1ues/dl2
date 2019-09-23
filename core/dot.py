import __init__
from core.ctx import *

class Dot():
    def __init__(this, src, dst):
        this.src = src
        this.Dc = src.Dmg
        this.host = dst
        this.hostname = this.host.name
        this.stacks = 0
        this.all_stacks = []

    def __call__(this, *args, **kwargs):
        return _Dot(this, *args, **kwargs)
    

class _Dot():
    def __init__(this, static, name, coef, duration, iv):
        this._static = static
        this.host = this._static.host
        this.src = this._static.src
        this.label = '%s, %s'%(this.src.name, name)
        this.name = name
        this.duration = duration
        this.iv = iv
        this.Dmg = static.Dc
        dmgconf = {
                 'name'     : name
                ,'hostname' : this.src
                ,'hit'      : 0
                ,'to_od'    : 0
                ,'to_bk'    : 0
                ,'coef'     : coef
                ,'type'     : 's'
                }
        this.dmg = this.Dmg(dmgconf)
        this.log = Logger('dot')
        this.t_dot_end = Timer(this.dot_end_proc)

    def __call__(this):
        if this.log:
            this.log(this.label, 'apply',this.host.name)
        this.true_dmg = this.dmg.calc()
        this._static.all_stacks.append(this)
        this.t_dot_end(this.duration)
        if this._static.stacks == 0:
            this._static.e_tick = Timer(this.tick_proc)(this.iv)
        this._static.stacks += 1
        if this.log:
            if this._static.stacks > 1:
                this.log(this.name,'stack_add',
                        "dot stack <%d>"%this._static.stacks)

    def dot_end_proc(this, t):
        idx = this._static.all_stacks.index(this)
        this._static.all_stacks.pop(idx)
        this._static.stacks -= 1
        if this.log:
            this.log(this.name,'stack_end',
                    "dot stack <%d>"%this._static.stacks)
        if this._static.stacks < 0:
            print('err in dot_end_proc')
            raise
        if this._static.stacks == 0:
            this._static.e_tick.off()

    def tick_proc(this, t):
        dmg_sum = 0
        stacks = this._static.stacks
        for i in this._static.all_stacks:
            dmg_sum += i.true_dmg
        this.dmg.dmg.dmg = dmg_sum
        this.host.dt_no_od(this.dmg.dmg)
        t()

