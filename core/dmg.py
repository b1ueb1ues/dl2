import __init__
from core.ctx import *


class _Dmg(object):
    def __init__(this):
        this.name = ''
        this.hostname = ''
        this.dmg = 0
        this.hit = 1
        this.to_od = 1 # rate
        this.to_bk = 1 # rate


class Dmg_calc(object):
    def __init__(this, src, dst): # src character , dst target
        this.dst_ele = dst.conf['ele']
        this.src_ele = src.conf['ele']
        this.set_ele()

        this.src = src
        this.dst = dst

        src.conf['__sync'][this.sync_src] = 1
        dst.conf['__sync'][this.sync_dst] = 1

        this.hostname = src.name
        this.killer = {}


    def sync_src(this, c):
        this.src_ele = c['ele']
        this.set_ele()


    def sync_dst(this, c):
        this.dst_ele = c['ele']
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
        return _Dmg_calc(this, *args, **kwargs)


class Conf_dc(Config):
    default = {
         'name'    : 'dmg'
        ,'hit'     : 1
        ,'to_od'   : 1
        ,'to_bk'   : 1
        ,'coef'    : 0
        ,'type'    : ''
        ,'killer'  : {}
        ,'missile' : None
        ,'proc'    : None
        }

    def sync(this, c):
        this.dmg.name  = c['name']
        this.dmg.to_od = c['to_od']
        this.dmg.to_bk = c['to_bk']
        this.dmg.hit   = c['hit']
        this.coef      = c['coef']
        this.type      = c['type']
        this.killer    = c['killer']
        this.missile   = c['missile']
        this.proc      = c['proc']

class _Dmg_calc(object):
    def __init__(this, static, conf):  # conf hitattr
        this._static = static
        this.src = this._static.src
        this.dst = this._static.dst

        this.src_get = this.src.Dp.get
        this.src_get_ = this.src.Dp.get_
        this.src_cache = this.src.Dp.cache

        this.dst_get = this.dst.Dp.get
        this.dst_get_ = this.dst.Dp.get_
        this.dst_cache = this.dst.Dp.cache

        this.dst_ks = this.dst.Dp.type_mods['ks']
        this.src_killer = this.src.Dp.type_mods['killer']

        this.dmg = _Dmg()
        this.dmg.hostname = this._static.hostname
        
        Conf_dc(this, conf)()


    def __call__(this): 
        this.dmg.dmg = this.calc()
        if this.missile :
            for i in this.missile:
                if i == 0 :
                    this.src.hit(this.dmg.hit)
                    this.dst.dt(this.dmg)
                    if this.proc:
                        this.proc()
                else:
                    Timer(this.cb_dmg_make)(i)
        else:
            this.src.hit(this.dmg.hit)
            this.dst.dt(this.dmg)
            if this.proc:
                this.proc()


    def cb_dmg_make(this, t):
        this.dmg.dmg = this.calc()
        this.src.hit(this.dmg.hit)
        this.dst.dt(this.dmg)
        if this.proc:
            this.proc()


    def calc(this):
        if this.src_cache['atk'] >= 0:
            atk  = this.src.atk * this.src_cache['atk']
        else:
            atk  = this.src.atk * this.src_get_('atk')

        if this.dst_cache['def'] >= 0:
            def_ = this.dst.def_ * this.dst_cache['def']
        else:
            def_ = this.dst.def_ * this.dst_get_('def')

        true_dmg = atk / def_ * this._static.base_coef

        if this.src_cache['dmg'] >= 0:
            true_dmg *= this.src_cache['dmg']
        else:
            true_dmg *= this.src_get_('dmg')

        if this.dst_cache['dt'] >= 0:
            true_dmg *= this.dst_cache['dt']
        else:
            true_dmg *= this.dst_get_('dt')

        if this.src_cache[this.type] >= 0:
            true_dmg *= this.src_cache[this.type]
        else:
            true_dmg *= this.src_get_(this.type)

        if this.src_cache['cc'] >= 0:
            cc  = this.src_cache['cc']
        else:
            cc  = this.src_get_('cc')

        if this.src_cache['cd'] >= 0:
            cd  = this.src_cache['cd']
        else:
            cd  = this.src_get_('cd')

        crit_ave = (cd-1) * (cc-1) + 1
        true_dmg *= crit_ave
        
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

        return int(true_dmg * this.coef)


class Dmg_param(object):
    def __init__(this, host):
        this.host = host
        this.type_mods = {}
        this.cache = {'':1}  # type: cache_value(-1:dirty)
        for i in host.conf['param_type']:
            this.type_mods[i] = []
            this.cache[i] = -1


    def add(this, *args, **kwargs):
        return _Dmg_param(this, *args, **kwargs)

    __call__ = add

    
    def copy_this_content_to_make_a_inline_get_manualy():
        if cache[mtype] >= 0:
            return cache[mtype]
        else:
            Dp.get_(mtype)

    def get_(this, mtype):
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

    def get(this, mtype):
        if this.cache[mtype] >= 0:
            return this.cache[mtype]

        mods = this.type_mods[mtype]
        m = {}
        for i in mods:
            if i.mod_order in m:
                m[i.mod_order] += i.mod_value
            else:
                m[i.mod_order] = 1.0 + i.mod_value
        ret = 1.0
        for i in m:
            ret *= m[i]
        this.cache[mtype] = ret
        return ret


class _Dmg_param(object):
    def __init__(this, static, name, mtype, morder, value):
        # mod_type = atk, def, dmg, x, fs, s, buff ...
        # mod_order = p: passive, b: buff, ex: co-ability
        this._static = static
        this.mod_name = name
        this.mod_type = mtype
        this.mod_order = morder
        this.mod_value = value
        this.__active = 0
        this.mods = static.type_mods[this.mod_type]
        this.cache = static.cache

    def get(this):
        return this.mod_value

    def set(this, value):
        this.cache[this.mod_type] = -1
        this.mod_value = value

    def on(this, value=None):
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
        return '%s:%s:<%s %s %s>'%(this._static.host.name,
                this.mod_name, this.mod_type, this.mod_order, this.mod_value)

#} class _Dmg_calc


if __name__ == '__main__':
    conf = Conf()
    conf.get['param_type'] = ['atk','def']
    host = Conf()
    host.name = 'host'
    host.conf = conf.get
    dp = Dmg_param(host)
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


