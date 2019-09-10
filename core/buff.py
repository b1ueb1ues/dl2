import __init__
from core.ctx import *


class Buff(object):
    def __init__(this, Dc):
        this.Dc = Dc
        Dc.conf.src.sync_buff = this.sync

        this.buff_group = {}

        Event('buff')(this.l_buff)


    def __call__(this, *args, **kwargs):
        class __Buff(_Buff):
            _static = this
        return __Buff(*args, **kwargs)


    def l_buff(this, e):
        this(e.name, e.value, e.mtype, e.morder, e.group)(e.duration)


    def sync(this, c, cc):
        this.hostname = c.name


class _Buff(object):
    def __init__(this, name, value,
            mtype='atk', morder=None, group=None):
        if morder == None:
            if mtype in ['atk','s','hp']:
                morder = 'b'
            else:
                morder = 'p'
        this.name = name
        this._value = value
        this.mod_type = mtype # atk def_ cc cd buff sp x fs s dmg
        this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab
        if group == None:
            this.group_name = mtype
        else:
            this.group_name = group
        group_id = (this.group_name, this.mod_order)

        this.hostname = this._static.hostname
        this._active = 0
        this.t_buffend = Timer(this.__buff_end)
        this.Dc = this._static.Dc
        this.dc = this._static.Dc(this.name,
                this.mod_type, this.mod_order, value)
        if group_id not in this._static.buff_group:
            this.group = []
            this._static.buff_group[group_id] = this.group
        else:
            this.group = this._static.buff_group[group_id]


    def get(this):
        if this._active:
            return this._value
        else:
            return 0


    def set(this, v):
        if this._active:
            print('can not set buff when active')
            errrrrrrrrrrrrr()
        this._value = v
        this.dc.set(v)
        return this


    def get_group(this):
        value = 0
        stack = len(this.group)
        for i in this.group :
            if i._active != 0:
                value += i._value
        return value, stack


    def __buff_stack(this):
        v_total, stacks = this.get_group()
        log_('buff', '%s: %s'%(this.hostname, this.name),
                '%s stack: %d'%(this.group_name, stacks),
                'total: %.2f'%(v_total))


    def __buff_start(this, duration):
        this._active = 1
        this.dc.on()
        if duration > 0:
            this.t_buffend.on(duration)
        stacks = len(this.group)
        if stacks >= 10:
            log('buff', '%s: %s'%(this.hostname, this.name),
                    'failed', 'stack cap')
            return
        stacks += 1
        this.group.append(this)
        if verbose('buff'):
            log('buff', '%s: %s'%(this.hostname, this.name),
                    '%s: %.2f'%(this.mod_type, this.get()),
                    '%s buff start <%ds>'%(this.group_name, duration))
            if stacks > 1:
                this.__buff_stack()
        log('dc', '%s: %s'%(this.hostname, this.mod_type),
                this._static.Dc.get(this.mod_type))


    def __buff_refresh(this, duration):
        if duration > 0:
            this.t_buffend.on(duration)
        if verbose('buff'):
            log('buff', '%s: %s'%(this.hostname, this.name),
                    '%s: %.2f'%(this.mod_type, this.get()),
                    '%s buff refresh <%ds>'%(this.group_name, duration))
            stacks = len(this.group)
            if stacks > 1:
                this.__buff_stack()


    def __buff_end(this, e):
        this._active = 0

        idx = len(this.group)
        stack = idx
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == this.group[idx]:
                this.group.pop(idx)
                break
        if verbose('buff'):
            log_('buff', '%s: %s'%(this.hostname, this.name),
                    '%s: %.2f'%(this.mod_type, this._value),
                    'buff end <timeout>')
            if stack > 1:
                this.__buff_stack()
        this.dc.off()
        this.end()
        log('dc', '%s: %s'%(this.hostname, this.mod_type),
                this._static.Dc.get(this.mod_type))


    def end(this):
        pass


    def on(this, duration):
        if this._active == 0:
            this.__buff_start(duration)
        else:
            this.__buff_refresh(duration)

        return this

    __call__ = on


    def off(this):
        if this._active == 0:
            return
        log('buff', this.name, '%s: %.2f'%(this.mod_type, this.get()),
                '%s buff end <turn off>'%(this.name))
        this._active = 0

        idx = len(this.group)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == this.group[idx]:
                this.group.pop(idx)
                break
        this.dc.off()
        if verbose('buff'):
            this.__buff_stack()
        this.t_buffend.off()
        return this


class Selfbuff(object):
    def __init__(this, Buff):
        this.Buff = Buff


    def __call__(this, *args, **kwargs):
        class __Selfbuff(_Selfbuff):
            _static = this.Buff
        return __Selfbuff(*args, **kwargs)


class _Selfbuff(_Buff):
    #def __init__(this, *args, **kwargs):
    #    super().__init__(*args, **kwargs)


    def on(this, duration):
        duration *= this.Dc.get('buff')
        super().on(duration)
        return this

    __call__ = on


class Debuff(object):
    def __init__(this, Buff):
        this.Buff = Buff


    def __call__(this, *args, **kwargs):
        class __Debuff(_Debuff):
            _static = this.Buff
        return __Debuff(*args, **kwargs)


class _Debuff(_Buff):
    def __init__(this, name, value,
            mtype='def', morder=None, group=None):
        super().__init__(name, value, mtype, morder, group)
        this.dc.set(0.0-value)
        

    def set(this, v):
        if this._active:
            print('can not set buff when active')
            errrrrrrrrrrrrr()
        this._value = v
        this.dc.set(0.0-v)
        return this


class Teambuff(object):
    def __init__(this, Buff):
        this.Dc = Buff.Dc
        this.e = Event('buff')


    def __call__(this, *args, **kwargs):
        class __Teambuff(_Teambuff):
            _static = this
        return __Teambuff(*args, **kwargs)


class _Teambuff():
    def __init__(this, name, value,
            mtype='atk', morder=None, group=None):
        e = this._static.e
        e.name = name
        e.value = value
        e.mtype = mtype
        e.morder = morder
        e.group = group

        this.e = e
        this.Dc = this._static.Dc


    def on(this, duration):
        this.e.duration = duration * this.Dc.get('buff')
        this.e()
        return this

    __call__ = on


    def set(this, v):
        this.e.value = v
        return this


class Zonebuff(object):
    def __init__(this, Buff):
        this.Dc = Buff.Dc
        this.e = Event('buff')


    def __call__(this, *args, **kwargs):
        class __Zonebuff(_Zonebuff):
            _static = this
        return __Zonebuff(*args, **kwargs)


class _Zonebuff():
    def __init__(this, name, value,
            mtype='atk', morder=None, group=None):
        e = this._static.e
        e.name = name
        e.value = value
        e.mtype = mtype
        e.morder = morder
        e.group = group

        this.e = e
        this.Dc = this._static.Dc


    def on(this, duration):
        this.e.duration = duration
        this.e()
        return this

    __call__ = on


    def set(this, v):
        this.e.value = v
        return this


class Passive(object):
    def __init__(this, Dc):
        this.Dc = Dc
        Dc.conf.src.sync_passive = this.sync


    def __call__(this, *args, **kwargs):
        class __Passive(_Passive):
            _static = this
        return __Passive(*args, **kwargs)


    def sync(this, c, cc):
        this.hostname = c.name


class _Passive():
    def __init__(this, name, value, mtype='atk', morder=None):
        this.name = name
        this._value = value
        this.mod_type = mtype # atk def_ cc cd buff sp x fs s dmg
        if morder == None:
            this.mod_order = 'p'
        else:
            this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab

        this.hostname = this._static.hostname
        this._active = 0
        this.Dc = this._static.Dc
        this.dc = this._static.Dc(this.name,
                this.mod_type, this.mod_order, value)


    def on(this):
        if this._active :
            this.dc()
            log('buff', '%s: %s'%(this.hostname, this.name),
                    '%s: %.2f'%(this.mod_type, this._value),'refresh')
            return this
        this.dc()
        this._active = 1
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this._value),'on')
        return this

    __call__ = on


    def off(this):
        if not this._active :
            return
        this.dc.off()
        this._active = 0
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this._value),'off')


    def get(this):
        if this._active:
            return this._value
        else:
            return 0


    def set(this, v):
        this._value = v
        this.dc.set(v)
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this._value),'set')
        return this


if __name__ == '__main__':
    def test():
        class C():
            def __init__(this):
                conf = Conf()
                conf.src.name = '1p'
                conf.dst.name = 'dummy'
                this.Dc = Dmg_calc(conf)
                this.Buff = Buff(this.Dc)
                this.Passive = Passive(this.Dc)
                this.Selfbuff = Selfbuff(this.Buff)
                this.Teambuff = Teambuff(this.Buff)

        class C2():
            def __init__(this):
                conf = Conf()
                conf.src.name = '2p'
                conf.dst.name = 'dummy'
                this.Dc = Dmg_calc(conf)
                this.Buff = Buff(this.Dc)
                this.Passive = Passive(this.Dc)
                this.Selfbuff = Selfbuff(this.Buff)
                this.Teambuff = Teambuff(this.Buff)
                this.Zonebuff = Zonebuff(this.Buff)
                this.Debuff = Debuff(this.Buff)


            def __call__(this):
                p = this.Passive('bt',0.2,'buff')()
                p.off()
                p()
                this.Teambuff('spd',0.2,'spd')(10)
                b = this.Teambuff('buff1',0.15)(10)
                b.set(0.2)
                b(10)
                this.Selfbuff('buff2',0.20)(5)
                this.Selfbuff('buff3',0.20,'atk','p')(-1)
                this.Zonebuff('zone', 0.1, 'atk')(10)
                d = this.Debuff('debuff',0.1,'def')
                d.set(0.15)
                d(10)
                print(d.get())


        c = C()
        c2 = C2()
        c2()

    #logset(['buff','dc'])
    logset(['buff'])
    test()
    Timer.run()
    logcat()





