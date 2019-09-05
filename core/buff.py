from ctx import *


class Modifier(object):
    _static = {}
    mod_name = '<nop>'
    mod_type = '_nop' or 'atk' or 'def' or 'dmg' or 'x' or 'fs' or 's' #....
    mod_order = '_nop' or 'p' or 'ex' or 'b' # chance dmg for crit 
    mod_value = 0

    @classmethod
    def init(cls):
        cls._static = {}
        cls._static['all_modifiers'] = []


    def __init__(this, name, mtype, morder, value, condition=None):
        this.mod_name = name
        this.mod_type = mtype
        this.mod_order = morder
        this.mod_value = value
        this.mod_condition = condition
        this.__active = 0
        this.on()


    @classmethod
    def mod(cls, mtype, all_modifiers=None):
        if not all_modifiers:
            all_modifiers = cls._static['all_modifiers']
        m = {}
        for i in all_modifiers:
            if mtype == i.mod_type:
                if i.mod_order in m:
                    m[i.mod_order] += i.get()
                else:
                    m[i.mod_order] = 1 + i.get()
        ret = 1.0
        for i in m:
            ret *= m[i]
        return ret


    def get(this):
        return this.mod_value


    def on(this, modifier=None):
        if this.__active == 1:
            return this
        if modifier == None:
            modifier = this
        if modifier.mod_condition :
            if not m_condition.on(modifier.mod_condition):
                return this

        this._static['all_modifiers'].append(modifier)
        this.__active = 1
        return this


    def off(this, modifier=None):
        if this.__active == 0:
            return this
        this.__active = 0
        if modifier==None:
            modifier = this
        idx = len(this._static['all_modifiers'])
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this._static['all_modifiers'][idx] == modifier:
                this._static['all_modifiers'].pop(idx)
                break
        return this


    def __repr__(this):
        return '<%s %s %s %s>'%(this.mod_name, this.mod_type, this.mod_order, this.mod_value)


class Buff(object):
    @classmethod
    def init(cls):
        cls._static = {}
        cls._static['all_buffs'] = []
        cls._static['time_func'] = 0


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
        if not this._static.time_func:
            this._static.time_func = this.nobufftime

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
        return this._static.time_func()


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
    Buff.init()
