from ctx import *


class Modifier(object):
    def __init__(this, host):
        this.host = host
        this.type_mods = {}
        this.cache = {}  # type: cache_value(-1:dirty)


    def __call__(this, *args, **kwargs):
        class __Modifier(_Modifier):
            _static = this
        return __Modifier(*args, **kwargs)


    def mod(this, mtype):
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


class _Modifier(object):

    def __init__(this, name, mtype, morder, value):
        # mod_name = '<nop>'
        # mod_type = '_nop' or 'atk' or 'def' or 'dmg' or 'x' or 'fs' or 's' #....
        # mod_order = '_nop' or 'p' or 'ex' or 'b' # 
        this.mod_name = name
        this.mod_type = mtype
        this.mod_order = morder
        this.mod_value = value
        this.__active = 0
        if this.mod_type not in this._static.type_mods:
            this._static.type_mods[this.mod_type] = []
        this.on()


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
        return '<%s %s %s %s>'%(this.mod_name, this.mod_type, this.mod_order, this.mod_value)

#} class _Modifier


class Buff(object):
    def __init__(this, mod):
        if mod.__class__ != Modifier:
            print('should init buff with modifier')
            errrrrrrrrrrrrr()
        this.host = mod.host
        this.buff_group = {}
        this.time_mod = None
        this.Mod = mod


    def __call__(this, *args, **kwargs):
        class __Buff(_Buff):
            _static = this
        return __Buff(*args, **kwargs)


class _Buff(object):
    def __init__(this, name, value, duration=-1, mtype='atk', morder='b', group=None):
        if mtype in ['cc','cd']:
            morder = 'p'
        this.name = name   
        this.__value = value
        this.duration = duration
        this.mod_type = mtype # atk def_ cc cd buff sp x fs s dmg
        this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab
        if group==None:
            this.group_name = mtype
        else:
            this.group_name = group

        if this.group_name not in this._static.buff_group:
            this._static.buff_group[this.group_name] = []

        this.t_buffend = Timer(this.__buff_end)
        this.modifier = this._static.Mod('mod_'+this.name, this.mod_type, this.mod_order, 0)

        this.__active = 0

    
    def get(this):
        if this.__active:
            return this.__value
        else:
            return 0


    def set(this, v, d=None):
        this.__value = v
        this.modifier.set(v)
        if d != None:
            this.duration = d
        return this


    def get_group(this):
        value = 0
        stack = len(this._static.buff_group[this.group_name])
        for i in this._static.buff_group[this.group_name]:
            if i.__active != 0:
                value += i.__value
        return value, stack


    def __buff_stack(this):
        group = this._static.buff_group[this.group_name]
        v_total, stacks = this.get_group()
        log('buff', this.name, 
                '%s stack: %d'%(this.group_name, stacks), 
                'total: %.2f'%(v_total))


    def __buff_start(this, duration):
        this.__active = 1
        if duration > 0:
            this.t_buffend.on(duration)
        group = this._static.buff_group[this.group_name]
        stacks = len(group)
        if stacks >= 10:
            log('buff', '%s: %s'%(this.host, this.name), 'failed', 'stack cap')
            return 
        stacks += 1
        group.append(this)
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.get()), 
                '%s buff start <%ds>'%(this.group_name, duration))
        if stacks > 1:
            this.__buff_stack()


    def __buff_refresh(this, duration):
        if duration > 0:
            this.t_buffend.on(duration)
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.get()), 
                '%s buff refresh <%ds>'%(this.group_name, duration))
        group = this._static.buff_group[this.group_name]
        stacks = len(group)
        if stacks > 1:
            this.__buff_stack()


    def __buff_end(this, e):
        group_value, stack = this.get_group()
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.get()), 
                '%s buff end <timeout>'%this.name)
        this.__active = 0

        group = this._static.buff_group[this.group_name]

        idx = len(group)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == group[idx]:
                group.pop(idx)
                break
        this.modifier.off()
        this.__buff_stack()
        this.end()


    def end(this): 
        pass


    def on(this, duration=None):
        if duration == None:
            d = this.duration
        else:
            d = duration

        if this.__active == 0:
            this.__buff_start(d)
        else:
            this.__buff_refresh(d)

        return this

    __call__ = on


    def off(this):
        if this.__active == 0:
            return 
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.get()), 
                '%s buff end <turn off>'%(this.name))
        this.__active = 0

        group = this._static.buff_group[this.group_name]

        idx = len(group)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == group[idx]:
                group.pop(idx)
                break
        this.modifier.off()
        this.__buff_stack()
        this.t_buffend.off()
        return this



if __name__ == '__main__':
    logset(['debug','buff'])
    class A():
        name = 'a'
    a = A()
    m = Modifier(a)
    b = Buff(m)
    b1 = b('b1',0.15,-1,'atk','p')
    b1()
    b1()
    b2 = b('b2',0.25,10,'atk','p')
    b2()
    b3 = b('b3',0.20,10,'atk','p','ruin')
    def foo(e):
        b3()
    Timer(foo)(1)
    Timer.run()
    logcat()
    

