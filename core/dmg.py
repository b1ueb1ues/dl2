import __init__
from core.ctx import *


class Dmg(object):
    def __init__(this):
        this.name = ''
        this.dmg = 0
        this.to_od = 1 # rate
        this.to_bk = 1 # rate


class Dmg_calc(object):
    def __init__(this, src, dst): # src character , dst target
        this.dst_ele = ''
        this.src_ele = ''

        this.src = src
        this.dst = dst
        this.conf_src = src.conf
        this.conf_dst = dst.conf
        this.conf_src(this.sync_src)
        this.conf_dst(this.sync_dst)
        this.hostname = src.conf.name
        this.killer = {}


    def sync_src(this, c):
        this.src_ele = c.ele
        this.set_ele()


    def sync_dst(this, c):
        this.dst_ele = c.ele
        this.set_ele()


    def set_ele(this):
        if this.src_ele == 'flame' and this.dst_ele == 'wind':
            this.ele = 1.5
        elif this.src_ele == 'water' and this.dst_ele == 'flame':
            this.ele = 1.5
        elif this.src_ele == 'wind' and this.dst_ele == 'water':
            this.ele = 1.5
        elif this.src_ele == 'light' and this.dst_ele == 'shadow':
            this.ele = 1.5
        elif this.src_ele == 'shadow' and this.dst_ele == 'light':
            this.ele = 1.5

        elif this.src_ele == 'flame' and this.dst_ele == 'water':
            this.ele = 0.5
        elif this.src_ele == 'water' and this.dst_ele == 'wind':
            this.ele = 0.5
        elif this.src_ele == 'wind' and this.dst_ele == 'flame':
            this.ele = 0.5

        else:
            this.ele = 1

        if this.dst_ele == 'on':
            this.ele = 1.5
        elif this.dst_ele == 'off':
            this.ele = 0.5
        if this.src_ele == 'on':
            this.ele = 1.5
        elif this.src_ele == 'off':
            this.ele = 0.5

        this.base_coef = this.ele / 0.6


    def __call__(this, *args, **kwargs):
        class __Dmg_calc(_Dmg_calc):
            _static = this
        return __Dmg_calc(*args, **kwargs)


class Conf_dc(Config):
    def default(this, conf):
        conf.name = 'dmg'
        conf.to_od = 1
        conf.to_bk = 1
        conf.coef = 0
        conf.type = 's'
        conf.killer = {}
        conf.missile = None
        conf.proc = None


    def sync(this, c):
        this.dmg.name = c.name
        this.dmg.to_od = c.to_od
        this.dmg.to_bk = c.to_bk
        this.coef = c.coef
        this.type = c.type
        this.killer = c.killer
        this.missile = c.missile


class _Dmg_calc(object):
    def __init__(this, conf):  # conf hitattr
        this.src = this._static.src
        this.dst = this._static.dst
        this.src_dp = this.src.Dp.get
        this.dst_dp = this.dst.Dp.get
        this.dst_ks = this.dst.Dp.type_mods['ks']
        this.src_killer = this.src.Dp.type_mods['killer']

        this.dmg = Dmg()
        this.dmg.hostname = this._static.hostname
        
        this.conf = Conf_dc(this, conf)


    def __call__(this): 
        this.dmg.dmg = this.calc()
        if this.missile :
            for i in this.missile:
                if i == 0 :
                    this.dst.dt(this.dmg)
                    if this.proc:
                        this.proc()
                else:
                    Timer(this.cb_dmg_make)(i)
        else:
            this.dst.dt(this.dmg)
            if this.proc:
                this.proc()


    def cb_dmg_make(this, t):
        this.dmg.dmg = this.calc()
        this.dst.dt(this.dmg)
        if this.proc:
            this.proc()


    def calc(this):
        atk  = this.src.atk * this.src_dp('atk')
        def_ = this.dst.def_ * this.dst_dp('def')
        true_dmg = atk / def_ * this._static.base_coef
        true_dmg *= this.src_dp('dmg')
        true_dmg *= this.src_dp(this.type)
        
        if len(this.src_killer) > 0:
            ks = {}
            bk = 1
            k = 1
            for i in this.dst_ks:
                ks[i.mod_order] = 1
            for i in this.src_killer:
                if i.mod_order in ks:
                    if i.mod_order == 'bk':
                        bk += i.mod_value
                    else:
                        k += i.mod_value
            true_dmg = true_dmg * k * bk

        for i in this.killer:
            for j in this.dst_ks :
                if j.mod_order == i:
                    true_dmg *= (1+this.killer[i])

        true_dmg *= this.coef
        return true_dmg


class Dmg_param(object):
    def __init__(this, conf):
        this.conf = conf
        conf(this.sync)

        this.type_mods = {'ks':[], 'killer':[]}
        this.cache = {}  # type: cache_value(-1:dirty)


    def sync(this, c):
        this.hostname = c.name


    def add(this, *args, **kwargs):
        class __Dmg_param(_Dmg_param):
            _static = this
        return __Dmg_param(*args, **kwargs)

    __call__ = add


    def get(this, mtype):
        if mtype in this.cache:
            if this.cache[mtype] >= 0:
                return this.cache[mtype]

        if mtype not in this.type_mods:
            return 1

        mods = this.type_mods[mtype]
        m = {}
        for i in mods:
            if i.mod_order in m:
                m[i.mod_order] += i.get()
            else:
                m[i.mod_order] = 1.0 + i.get()
        ret = 1.0
        for i in m:
            ret *= m[i]
        this.cache[mtype] = ret
        return ret


class _Dmg_param(object):
    def __init__(this, name, mtype, morder, value):
        # mod_type = atk, def, dmg, x, fs, s, buff ...
        # mod_order = p: passive, b: buff, ex: co-ability
        this.mod_name = name
        this.mod_type = mtype
        this.mod_order = morder
        this.mod_value = value
        this.__active = 0
        static = this._static
        if this.mod_type not in this._static.type_mods:
            this.mods = []
            static.type_mods[this.mod_type] = this.mods
        else:
            this.mods = static.type_mods[this.mod_type]
        this.cache = static.cache
        #this.on()


    def get(this):
        return this.mod_value


    def set(this, value):
        this.cache[this.mod_type] = -1
        this.mod_value = value


    def on(this, value=None):
        if value!=None:
            this.set(value)
        if this.__active == 1:
            return this
        this.__active = 1
        this.mods.append(this)
        this.cache[this.mod_type] = -1
        return this

    __call__ = on


    def off(this):
        if this.__active == 0:
            return this
        this.__active = 0
        mods = this.mods
        idx = len(mods)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if mods[idx] == this:
                mods.pop(idx)
                break
        this.cache[this.mod_type] = -1
        return this


    def __repr__(this):
        return '%s:%s:<%s %s %s>'%(this._static.hostname,
                this.mod_name, this.mod_type, this.mod_order, this.mod_value)

#} class _Dmg_calc


if __name__ == '__main__':
    conf = Conf()
    conf.name = '1p'
    dp = Dmg_param(conf)
    dp1 = dp('str10', 'atk', 'p', 0.1)()
    dp2 = dp('str15', 'atk', 'b', 0.15)()
    dp3 = dp('str15', 'atk', 'b', 0.15)()
    dp4 = dp('def-10', 'def', 'b', -0.10)()
    print(dp1)
    print(dp2)
    print(dp3)
    print(dp4)
    print(dp.get('atk'))
    print(dp.get('def'))


