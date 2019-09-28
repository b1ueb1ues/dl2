from functools import partial
from itertools import combinations
import random
from mod.dot import *


class Bleed(object):
    def __init__(this, src):
        this.src = src
        this.dst = src.target
        if 'Bleed_dot' not in this.dst.mod :
            this.dst.mod['Bleed_dot'] = Bleed_dot(this.dst)

    def __call__(this, name, *args, **kwargs):
        return this.dst.mod['Bleed_dot'](this.src, name, *args, **kwargs)


class Bleed_dot(object):
    def __init__(this, host):
        this.host = host
        if 'Dot_group' not in this.host.mod:
            host.mod['Dot_group'] = Dot_group(host)

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
        if not static.dot_group[atype] :
            static.dot_group[atype] = host.Dot_group(atype,4.99)
                                        
        this.atype = atype
        this.coef = coef
        if duration:
            this.duration = duration
        else:
            this.duration = 30

        this.dot = static.dot_group[atype]
        this.log = Logger('afflic')

    def __call__(this):
        if random.random() < this.rate:
            # proc
            this.log('proc', '%.2f'%(this.rate) )
            this.dot(this.src, this.name, this.coef, this.duration)()
        else:
            # resist
            if this.log:
                this.log('normal resist')

    on = __call__

