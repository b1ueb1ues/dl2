import __init__
from core.ctx import *
from core.dc import *


class Buff(object):
    def __init__(this, Dc):
        this.Dc = Dc
        Dc.conf_src.sync_buff = this.sync

        this.buff_group = {}
        this.time_mod = None
        Event('buff')(this.l_buff)


    def __call__(this, *args, **kwargs):
        class __Buff(_Buff):
            _static = this
        return __Buff(*args, **kwargs)


    def l_buff(this, e):
        this(e.name, e.value, e.duration, e.mtype, e.morder, e.group)()


    def sync(this, c, cc):
        this.hostname = c.name


class _Buff(object):
    def __init__(this, name, value, duration=-1,
            mtype='atk', morder=None, group=None):
        if morder == None:
            if mtype in ['cc','cd']:
                morder = 'p'
            else:
                morder = 'b'
        this.name = name
        this.hostname = this._static.hostname
        this.__value = value
        this.duration = duration
        this.mod_type = mtype # atk def_ cc cd buff sp x fs s dmg
        this.mod_order = morder # p: passive, b: buff, k: killer, ex: co-ab
        if group == None:
            this.group_name = mtype
        else:
            this.group_name = group
        group_id = (this.group_name, this.mod_order)

        if group_id not in this._static.buff_group:
            this.group = []
            this._static.buff_group[group_id] = this.group
        else:
            this.group = this._static.buff_group[group_id]

        this.dc = this._static.Dc(this.name,
                this.mod_type, this.mod_order, value)

        this.t_buffend = Timer(this.__buff_end)
        this.__active = 0


    def get(this):
        if this.__active:
            return this.__value
        else:
            return 0


    def set(this, v, d=None):
        this.__value = v
        this.dc.set(v)
        if d != None:
            this.duration = d
        return this


    def get_group(this):
        value = 0
        stack = len(this.group)
        for i in this.group :
            if i.__active != 0:
                value += i.__value
        return value, stack


    def __buff_stack(this):
        v_total, stacks = this.get_group()
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s stack: %d'%(this.group_name, stacks),
                'total: %.2f'%(v_total))


    def __buff_start(this, duration):
        this.__active = 1
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
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this.get()),
                '%s buff start <%ds>'%(this.group_name, duration))
        if stacks > 1:
            this.__buff_stack()
        log('debug', '%s: dc %s'%(this.hostname, this.mod_type),
                this._static.Dc.get(this.mod_type))


    def __buff_refresh(this, duration):
        if duration > 0:
            this.t_buffend.on(duration)
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this.get()),
                '%s buff refresh <%ds>'%(this.group_name, duration))
        stacks = len(this.group)
        if stacks > 1:
            this.__buff_stack()


    def __buff_end(this, e):
        log('buff', '%s: %s'%(this.hostname, this.name),
                '%s: %.2f'%(this.mod_type, this.get()),
                'buff end <timeout>')
        this.__active = 0

        idx = len(this.group)
        stack = idx
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == this.group[idx]:
                this.group.pop(idx)
                break
        if stack > 1:
            this.__buff_stack()
        this.dc.off()
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

        idx = len(this.group)
        while 1:
            idx -= 1
            if idx < 0:
                break
            if this == this.group[idx]:
                this.group.pop(idx)
                break
        this.dc.off()
        this.__buff_stack()
        this.t_buffend.off()
        return this




#class Selfbuff(object):
#    def __init__(this, mod):
#        if mod.__class__ != Modifier:
#            print('should init buff with modifier')
#            print(mod.__class__)
#            errrrrrrrrrrrrr()
#        this.host = mod.host
#        this.buff_group = {}
#        this.time_mod = None
#        this.Mod = mod
#
#
#    def __call__(this, *args, **kwargs):
#        class __Selfbuff(_Selfbuff):
#            _static = this
#        return __Selfbuff(*args, **kwargs)
#
#
#class _Selfbuff(buffbase._Buff):
#    def __init__(this, name, value, duration=-1, 
#            mtype='atk', morder='b', group=None):
#        super(_Selfbuff, this).__init__(name, value, duration, 
#            mtype, morder, group)
#        this.duration += this.duration * this._static.Mod.get('buff')
#
#
#    def on(this, duration=None):
#        if duration == None:
#            super(this.__class__, this).on(
#                    this.duration * this._static.Mod.get('buff'))
#            #d = this.duration * this._static.Mod.get('buff')
#        else:
#            super(this.__class__, this).on(
#                    duration * this._static.Mod.get('buff'))
#            #d = duration * this._static.Mod.get('buff')
#
#        if this.__active == 0:
#            this.__buff_start(d)
#        else:
#            this.__buff_refresh(d)
#
#        return this
#
#    __call__ = on
#
#
#class Teambuff(object):
#    def __init__(this, mod):
#        if mod.__class__ != Modifier:
#            print('should init buff with modifier')
#            print(mod.__class__)
#            errrrrrrrrrrrrr()
#        this.host = mod.host
#        this.buff_group = {}
#        this.time_mod = None
#        this.Mod = mod
#
#
#    def __call__(this, *args, **kwargs):
#        class __Teambuff(_Selfbuff):
#            _static = this
#        return __Teambuff(*args, **kwargs)
#
#
#class _Teambuff():
#    pass
#


if __name__ == '__main__':
    logset(['debug','buff'])

    
    class C():
        def __init__(this):
            src = Conf()
            dst = Conf()
            src.name = '1p'
            dst.name = 'dummy'
            this.Dc = Dmg_calc(src, dst)
            this.Buff = Buff(this.Dc)
            this.Buff('buff1',0.15,10)()
            this.Buff('buff2',0.20,5)()
            this.Buff('buff3',0.20,-1,'atk','p')()

    c = C()
    e = Event('buff')
    e.name = 'buff_event'
    e.value = 0.3
    e.duration = 10
    e.mtype = 'atk'
    e.morder = 'p'
    e.group = 'atk'

    Timer.run()
    logcat()



