import __init__
from core.ctx import *


class Dmg(object):
    def __init__(this, Dc):
        this.name = name
        this.hostname = Dc.hostname
        this.dmg = 0
        this.to_od = 1 # rate
        this.to_bk = 1 # rate

class Dmg_calc(object):
    def __init__(this, conf):
        this.conf 

    def sync_conf(this, c, cc):
        if cc[0] == 'src':
            this.conf_src = cc[1]

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


    def base(this, conf): # calculate base damage
        dmg = Dmg()
        dmg.to_od = 1
        dmg.to_bk = 1





class Dmg_param(object):
    def __init__(this):
        this.type_mods = {}
        this.cache = {}  # type: cache_value(-1:dirty)


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
            return 1.0

        mods = this.type_mods[mtype]
        m = {}
        for i in mods:
            if i.mod_order in m:
                m[i.mod_order] += i.get()
            else:
                m[i.mod_order] = 1 + i.get()
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
        return '<%s %s %s %s>'%(
                this.mod_name, this.mod_type, this.mod_order, this.mod_value)

#} class _Dmg_calc


if __name__ == '__main__':
    dp = Dmg_param()
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


