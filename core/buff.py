from ctx import *


class Modifier(object):
    def __init__(this, host):
        this.host = host
        this.type_mods = {}
        this.cache = {}


    def __call__(this, *args, **kwargs):
        class __Modifier(_Modifier):
            _static = this
        return __Modifier(*args, **kwargs)


    def mod(this, mtype):
        if mtype in this.cache:
            if this.cache[mtype] != -1:
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
        return this
    

    def __repr__(this):
        return '<%s %s %s %s>'%(this.mod_name, this.mod_type, this.mod_order, this.mod_value)

#} class _Modifier


class C():
    name = 'test'
c = C()
c.Modifier = Modifier(c)
c.mod1 = c.Modifier('a','atk','p',0.35)
c.mod2 = c.Modifier('a2','atk','p',0.15)
c.mod2 = c.Modifier('a2','atk','b',1.0)
c.mod3 = c.Modifier('a3','cc','p',0.15)
print(c.Modifier.mod('atk'))
c.mod2.off()
print(c.Modifier.mod('atk'))
exit()

class Buff(object):
    def __init__(this, host):
        this.host = host
        this.all_buffs = []
        this.time_mod = 0

    def __call__(this, *args, **kwargs):
        class __Buff(_Buff):
            _static = this
        return __Buff(*args, **kwargs)


class _Buff(object):

    def __init__(this, name='<buff_noname>', value=0, duration=0, mtype=None, morder=None):  
        this.name = name   
        this.__value = value
        this.duration = duration
        this.mod_type = mtype or 'atk' or 'x' or 'fs' or 's' #....
        this.bufftype = ''
        if morder ==None:
            if this.mod_type == 'crit':
                this.mod_order = 'chance'
            else:
                this.mod_order = 'buff'
        else:
            this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab

        if this.mod_order != 'buff':
            this.bufftime = this.nobufftime
        if not this._static.time_mod:
            this._static.time_mod = this.nobufftime

        this.buff_end_timer = Timer(this.buff_end_proc)
        this.modifier = Modifier('mod_'+this.name, this.mod_type, this.mod_order, 0)
        this.modifier.get = this.get
        this.dmg_test_event = Event('dmg_formula')
        this.dmg_test_event.dmg_coef = 1
        this.dmg_test_event.dname = 'test'

        this.__stored = 0
        this.__active = 0
        #this.on()

    def nobufftime(this):
        return 1
    
    def bufftime(this):
        return this._static.time_mod()


    def value(this, newvalue=None):
        if newvalue:
            return this.set(newvalue)
        else:
            return this.get()

    def get(this):
        if this.__active:
            return this.__value
        else:
            return 0

    def set(this, v, d=None):
        this.__value = v
        if d != None:
            this.duration = d
        return this

    def stack(this):
        stack = 0
        for i in this._static.all_buffs:
            if i.name == this.name:
                if i.__active != 0:
                    stack += 1
        return stack

    def valuestack(this):
        stack = 0
        value = 0
        for i in this._static.all_buffs:
            if i.name == this.name:
                if i.__active != 0:
                    stack += 1
                    value += i.__value
        return value, stack

    def buff_end_proc(this, e):
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.value()), this.name+' buff end <timeout>')
        this.__active = 0

        if this.__stored:
            idx = len(this._static.all_buffs)
            while 1:
                idx -= 1
                if idx < 0:
                    break
                if this == this._static.all_buffs[idx]:
                    this._static.all_buffs.pop(idx)
                    break
            this.__stored = 0
        value, stack = this.valuestack()
        if stack > 0:
            log('buff', this.name, '%s: %.2f'%(this.mod_type, value), this.name+' buff stack <%d>'%stack)
        this.modifier.off()


    def on(this, duration=None):
        if duration == None:
            d = this.duration * this.bufftime()
        else:
            d = duration * this.bufftime()
        if this.__active == 0:
            this.__active = 1
            if this.__stored == 0:
                this._static.all_buffs.append(this)
                this.__stored = 1
            if d >= 0:
                this.buff_end_timer.on(d)
            log('buff', this.name, '%s: %.2f'%(this.mod_type, this.value()), this.name+' buff start <%ds>'%d)
        else:
            if d >= 0:
                this.buff_end_timer.on(d)
            log('buff', this.name, '%s: %.2f'%(this.mod_type, this.value()), this.name+' buff refresh <%ds>'%d)

        value, stack = this.valuestack()
        if stack > 1:
            log('buff', this.name, '%s: %.2f'%(this.mod_type, value), this.name+' buff stack <%d>'%stack)

        this.modifier.on()
        return this


    def off(this):
        if this.__active == 0:
            return 
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.value()), this.name+' buff end <turn off>')
        this.__active = 0
        this.modifier.off()
        this.buff_end_timer.off()
        return this

if __name__ == '__main__':
    class _Buff(Buff):
        pass
    Buff = _Buff
    Buff.init()
    Buff()
    
