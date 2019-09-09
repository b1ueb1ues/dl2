from ctx import *


class Dmg_calc(object):
    def __init__(this, src, dst):
        this.c_src = src
        this.c_dst = dst
        src.dc = this
        src.sync_dc = this.sync_src
        dst.sync_dc = this.sync_dst
        this.type_mods = {}
        this.cache = {}  # type: cache_value(-1:dirty)


    def sync_src(this, c, cc):
        return 


    def sync_dst(this, c, cc):
        return 


    def add(this, *args, **kwargs):
        class __Dmg_calc(_Dmg_calc):
            _static = this
        return __Dmg_calc(*args, **kwargs)

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


class _Dmg_calc(object):
    def __init__(this, name, mtype, morder, value):
        # mod_type = atk, def, dmg, x, fs, s, buff ...
        # mod_order = p: passive, b: buff, ex: co-ability
        this.mod_name = name
        this.mod_type = mtype
        this.mod_order = morder
        this.mod_value = value
        this.__active = 0
        if this.mod_type not in this._static.type_mods:
            this._static.type_mods[this.mod_type] = []
        #this.on()


    def get(this):
        return this.mod_value


    def set(this, value):
        this._static.cache[this.mod_type] = -1
        this.mod_value = value


    def on(this, value=None):
        if value!=None:
            this.set(value)
        if this.__active == 1:
            return this
        this.__active = 1
        this._static.type_mods[this.mod_type].append(this)
        this._static.cache[this.mod_type] = -1
        return this

    __call__ = on


    def off(this):
        if this.__active == 0:
            return this
        this.__active = 0
        mods = this._static.type_mods[this.mod_type]
        idx = len(mods)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if mods[idx] == this:
                mods.pop(idx)
                break
        this._static.cache[this.mod_type] = -1
        return this


    def __repr__(this):
        return '<%s %s %s %s>'%(this.mod_name, this.mod_type,
                this.mod_order, this.mod_value)

#} class _Dmg_calc


if __name__ == '__main__':
    src = Conf()
    dst = Conf()
    dc = Dmg_calc(src, dst)
    dc1 = dc('str10', 'atk', 'p', 0.1)()
    dc2 = dc('str15', 'atk', 'b', 0.15)()
    print(dc1)
    print(dc2)
    print(dc.get('atk'))


