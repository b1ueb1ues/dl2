from functools import partial
from itertools import combinations
import random
from mod.dot import *
import mod
import core.dmg


class Bleed_group(Dot_group):
    def __init__(this, host):
        this.host = host
        if 'Bleed_group' not in this.host.mod:
            this.host.mod['Bleed_group'] = this

    def __call__(this, classname, iv):
        return _Bleed_group(this.host, classname, iv)

class _Bleed_group(mod.dot._Dot_group):
    def __init__(this, *args, **kwargs):
        super().__init__(*args, **kwargs)
        this.dmgs = []
        for i in range(3):
            dmg = core.dmg._Dmg()
            dmg.to_od = 0
            dmg.to_bk = 0
            dmg.hit = 0
            this.dmgs.append(dmg)


    def tick_proc(this, t):
        stacks = len(this.all_stacks)
        if stacks == 1:
            coef = 1
        elif stacks == 2:
            coef = 1.5
        elif stacks == 3:
            coef = 2
        else:
            print('0 < bleed stacks < 3')
            raise
        idx = 0
        for i in this.all_stacks:
            dmg = this.dmgs[idx]
            idx += 1
            dmg.hostname = i._dmg.hostname
            dmg.name = i._dmg.name
            dmg.dmg = i._dmg.dmg * coef
            this.host.dt_no_od(dmg)
        t()


class Bleed(object):
    def __init__(this, src):
        this.src = src
        this.dst = src.target
        if 'Bleed_dot' not in this.dst.mod :
            this.dst.mod['Bleed_dot'] = Bleed_dot(this.dst)

    def stacks(this):
        return this.dst.mod['Bleed_dot'].bleed_group.stacks

    def __call__(this, name, *args, **kwargs):
        return this.dst.mod['Bleed_dot'](this.src, name, *args, **kwargs)


class Bleed_dot(object):
    def __init__(this, host):
        this.host = host
        if 'Bleed_group' not in this.host.mod:
            host.mod['Bleed_group'] = Bleed_group(host)
        this.bleed_group = None

    def __call__(this, *args, **kwargs): # src, name, coef, duration):
        return _Bleed_dot(this, *args, **kwargs)


class _Bleed_dot(object):
    def __init__(this, static, src, name, rate, coef, duration=None):
        this._static = static
        this.rate = rate
        this.src = src
        this.name =name
        this.coef = coef
        host = static.host
        atype = 'bleed'
        if not static.bleed_group :
            static.bleed_group = host.mod['Bleed_group'](atype,4.99)
                                        
        this.atype = atype
        this.coef = coef
        if duration:
            this.duration = duration
        else:
            this.duration = 30

        this.dot = static.bleed_group
        this.log = Logger('bleed')
        this.loghost = src.name

    def __call__(this):
        if random.random() < this.rate:
            # proc
            stacks = this._static.bleed_group.stacks
            if this.log:
                this.log(this.loghost, 'proc', '%.2f'%(this.rate) )
            if stacks >= 3:
                if this.log:
                    this.log(this.loghost, 'bleed hit cap')
                return -1
            this.dot(this.src, this.name, this.coef, this.duration)()
            return stacks+1
        else:
            # resist
            if this.log:
                this.log(this.loghost, 'normal miss')
            return 0

    on = __call__

