import __init__
from core.ctx import *


class Passive(object):
    def __init__(this, Dp):
        this.Dp = Dp
        Dp.conf(this.sync)


    def __call__(this, *args, **kwargs):
        return _Passive(this, *args, **kwargs)


    def sync(this, c):
        this.hostname = c.name


class _Passive():
    def __init__(this, static, name, value, mtype='atk', morder=None):
        this._static = static
        this.name = name
        this._value = value
        this.mod_type = mtype # atk def_ cc cd buff sp x fs s dmg killer ks
        if morder == None:
            this.mod_order = 'p'
        else:
            this.mod_order = morder # p: passive, b: buff, ex: co-ab, 
            # od, bk, burn, poison...  (mtype = killer/ks)

        this._active = 0
        this.Dp = this._static.Dp
        this.dp = this._static.Dp(this.name,
                this.mod_type, this.mod_order, value)

        this.log = Logger('buff')

    def hostname(this):
        return this._static.hostname


    def on(this):
        if this._active :
            this.dp()
            if this.log:
                this.log('%s, %s'%(this.hostname(), this.name),
                    '%s: %.2f'%(this.mod_type, this._value),'refresh')
            return this
        this.dp()
        this._active = 1
        if this.log:
            this.log('%s, %s'%(this.hostname(), this.name),
                '%s: %.2f'%(this.mod_type, this._value),'on <passive>')
        return this

    __call__ = on


    def off(this):
        if not this._active :
            return
        this.dp.off()
        this._active = 0
        if this.log:
            this.log('%s, %s'%(this.hostname(), this.name),
                '%s: %.2f'%(this.mod_type, this._value),'off <passive>')


    def get(this):
        if this._active:
            return this._value
        else:
            return 0


    def set(this, v):
        this._value = v
        this.dp.set(v)
        if this.log:
            this.log('%s, %s'%(this.hostname(), this.name),
                '%s: %.2f'%(this.mod_type, this._value),'set')
        return this


class Buff(object):
    def __init__(this, Dp):
        this.Dp = Dp
        Dp.conf(this.sync)

        this.buff_group = {}

        Event('buff')(this.l_buff)
        this.log = Logger('buff')


    def __call__(this, *args, **kwargs):
        return _Buff(this, *args, **kwargs)


    def l_buff(this, e):
        this(e.name, e.value, e.mtype, e.morder, e.group)(e.duration)


    def sync(this, c):
        this.hostname = c.name


class _Buff(object):
    bufftype = 'buff'
    def __init__(this, static, name, value, mtype='atk', morder=None, group=None):
        this._static = static
        if morder == None:
            if mtype in ['atk','s','hp']:
                morder = 'b'
            else:
                morder = 'p'
        this.name = name
        this._value = value
        this.mod_type = mtype   # atk def_ cc cd buff sp x fs s dmg
        this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab
        if group == None:
            this.group_name = mtype
        else:
            this.group_name = group
        group_id = (this.group_name, this.mod_order)

        this._active = 0
        this.t_buffend = Timer(this.__buff_end)
        this.Dp = this._static.Dp
        this.dp = this.Dp(this.name, this.mod_type, this.mod_order, value)
        if group_id not in this._static.buff_group:
            this.group = []
            this._static.buff_group[group_id] = this.group
        else:
            this.group = this._static.buff_group[group_id]

        this.log = Logger('buff')
        this.log_dp = Logger('dp')

    def hostname(this):
        return this._static.hostname


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
        this.dp.set(this._value)
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
        this.log('%s, %s'%(this.hostname(), this.name),
            '%s stack: %d'%(this.group_name, stacks),
            'total: %.2f'%(v_total))


    def __buff_start(this, duration):
        this._active = 1
        this.dp.on()
        if duration > 0:
            this.t_buffend(duration)
        stacks = len(this.group)
        if stacks >= 10:
            if this.log:
                this.log('%s, %s'%(this.hostname(), this.name),
                    'failed', 'stack cap')
            return
        stacks += 1
        this.group.append(this)
        if this.log:
            this.log('%s, %s'%(this.hostname(), this.name),
                    '%s: %.2f'%(this.mod_type, this.get()),
                    '%s %s start <%ds>'%(this.group_name,
                        this.bufftype, duration))
            if stacks > 1:
                this.__buff_stack()
        if this.log_dp:
            this.log_dp('%s, %s'%(this.hostname(), this.mod_type),
                    this._static.Dp.get(this.mod_type))


    def __buff_refresh(this, duration):
        if duration > 0:
            this.t_buffend.on(duration)
        if this.log :
            this.log('%s, %s'%(this.hostname(), this.name),
                    '%s: %.2f'%(this.mod_type, this.get()),
                    '%s %s refresh <%ds>'%(this.group_name,
                        this.bufftype, duration))
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
        if this.log:
            this.log('%s, %s'%(this.hostname(), this.name),
                    '%s: %.2f'%(this.mod_type, this._value),
                    '%s end <timeout>'%this.bufftype)
            if stack > 1:
                this.__buff_stack()
        this.dp.off()
        this.end()
        if this.log_dp:
            this.log_dp('%s, %s'%(this.hostname(), this.mod_type),
                this._static.Dp.get(this.mod_type))


    def end(this):
        pass


    def on(this, duration):
        this.duration = duration
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
                '%s %s end <turn off>'%(this.name, this.duration))
        this._active = 0

        idx = len(this.group)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == this.group[idx]:
                this.group.pop(idx)
                break
        this.dp.off()
        if this.log:
            this.__buff_stack()
        this.t_buffend.off()
        return this


class Selfbuff(object):
    def __init__(this, Buff):
        this.Buff = Buff


    def __call__(this, *args, **kwargs):
        return _Selfbuff(this.Buff, *args, **kwargs)



class _Selfbuff(_Buff):
    bufftype = 'selfbuff'
    def on(this, duration):
        duration *= this.Dp.get('buff')
        super().on(duration)
        return this

    __call__ = on


class Debuff(object):
    def __init__(this, Buff):
        this.Buff = Buff


    def __call__(this, *args, **kwargs):
        return _Debuff(this.Buff, *args, **kwargs)


class _Debuff(_Buff):
    bufftype = 'debuff'
    def __init__(this, static, name, value, mtype='def', morder=None, group=None):
        super().__init__(static, name, 0-value, mtype, morder, group)
        #this.dp.set(0.0-value)
        

    def set(this, v):
        if this._active:
            print('can not set buff when active')
            errrrrrrrrrrrrr()
        this._value = 0.0-v
        this.dp.set(this._value)
        return this


class Teambuff(object):
    def __init__(this, Buff):
        this.Dp = Buff.Dp
        this.e = Event('buff')


    def __call__(this, *args, **kwargs):
        return _Teambuff(this, *args, **kwargs)


class _Teambuff():
    bufftype = 'teambuff'
    def __init__(this, static, name, value,
            mtype='atk', morder=None, group=None):
        this._static = static
        e = this._static.e
        e.name = name
        e.value = value
        e.mtype = mtype
        e.morder = morder
        e.group = group

        this.e = e
        this.Dp = this._static.Dp
        this.log = Logger('buff')


    def on(this, duration):
        this.e.duration = duration * this.Dp.get('buff')
        this.e()
        return this

    __call__ = on


    def set(this, v):
        this.e.value = v
        return this


class Zonebuff(object):
    def __init__(this, Buff):
        this.Dp = Buff.Dp
        this.e = Event('buff')


    def __call__(this, *args, **kwargs):
        return _Zonebuff(this, *args, **kwargs)


class _Zonebuff():
    bufftype = 'buffzone'
    def __init__(this, static, name, value,
            mtype='atk', morder=None, group=None):
        this._static = static
        e = this._static.e
        e.name = name
        e.value = value
        e.mtype = mtype
        e.morder = morder
        e.group = group

        this.e = e
        this.Dp = this._static.Dp
        this.log = Logger('buff')


    def on(this, duration):
        this.e.duration = duration
        this.e()
        return this

    __call__ = on


    def set(this, v):
        this.e.value = v
        return this




if __name__ == '__main__':
    def test():
        class C():
            def __init__(this):
                conf = Conf()
                conf.name = '1p'
                this.Dp = Dmg_param(conf)
                this.Buff = Buff(this.Dp)
                this.Passive = Passive(this.Dp)
                this.Selfbuff = Selfbuff(this.Buff)
                this.Teambuff = Teambuff(this.Buff)

        class C2():
            def __init__(this):
                conf = Conf()
                conf.name = '2p'
                this.Dp = Dmg_param(conf)
                this.Buff = Buff(this.Dp)
                this.Passive = Passive(this.Dp)
                this.Selfbuff = Selfbuff(this.Buff)
                this.Teambuff = Teambuff(this.Buff)
                this.Zonebuff = Zonebuff(this.Buff)
                this.Debuff = Debuff(this.Buff)


            def __call__(this):
                log('cast', 'passivebt')
                p = this.Passive('bt', 0.20,'buff')()
                log('cast', 'passivebt')
                p.off()
                log('cast', 'passivebt')
                p()
                log('cast', 'teamspd')
                this.Teambuff('spd', 0.20,'spd')(10)
                log('cast', 'team1', 0.15)
                b = this.Teambuff('team1', 0.15)(10)
                log('cast', 'team1', 0.20)
                b.set(0.20)
                b(10)
                log('cast', 'self2')
                this.Selfbuff('self2', 0.20)(5)
                log('cast', 'selfp')
                this.Selfbuff('selfp', 0.20,'atk','p')(-1)
                log('cast', 'zone')
                this.Zonebuff('zone', 0.10, 'atk')(10)
                log('cast', 'debuff')
                d = this.Debuff('debuff', 0.10,'def')
                d.set(0.15)
                d(10)
                print(d.get())


        c = C()
        c2 = C2()
        c2()

    logset(['buff','dp'])
    #logset(['buff','cast'])
    test()
    Timer.run()
    logcat()





