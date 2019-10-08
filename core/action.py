import __init__
from core.ctx import *


class Action(object):
    def __init__(this, host, Dp=None):
        this.host = host

        class Nop(object):
            conf = {'type':''}
            name = '__idle__'
            status = -1

        this.nop = Nop()

        this.prev = this.nop
        this.doing = this.nop

        if Dp:
            this.speed_cache = Dp.cache
            this.speed_get = Dp.get_
        else:
            this.speed_cache = {'spd':1}
            this.speed_get = 1


    def __call__(this, *args, **kwargs):
        return _Action(this, *args, **kwargs)


class Conf_Action(Config):
    def default(this):
        return {
             'type'      : ''
            ,'startup'   : 0
            ,'recovery'  : 2
            ,'cancel_by' : []
            ,'on_cancel' : []
            ,'on_end'    : []
            }


class _Action(object):   
    def __init__(this, static, name, conf=None):  
        ## can't change name after this
        this._static = static
        this.name = name
        this.src = this._static.host.name + ', '
        Conf_Action(this, conf)()

        this.speed_cache = static.speed_cache
        this.speed_get = static.speed_get

        this.action_start = 0
        this.status = 0 # -1: idle/end 0:wait 1:doing 2cancel

        this.t_recovery = Timer(this._cb_act_end)
        this.e_idle = static.host.Event('idle')
        this.log = Logger('act')
        this.log_r = Logger('rotation')


    def _cb_act_end(this, e):
        if this._static.doing != this:
            return 

        if this.log:
            this.log(this.src+'end', this.name)
        this.status = -1
        this._static.prev = this # turn this from doing to prev

        for i in this.conf['on_end']:
            i()
        #this._static.host.x(0)
        this.e_idle()


    def start(this):
        doing = this._static.doing

        if doing.status == -1 :
            if this.log:
                this.log(this.src+'start',this.name, 'idle:%d'%doing.status)
        else:
            if this.log:
                this.log(this.src+'start',this.name,
                        'doing '+doing.name+':%d'%doing.status)
            if doing == this : # self is doing
                if this.log:
                    this.log(this.src+'failed',this.name, 'self is doing')
                return 0

            # doing != this
            if doing.status == 1: # try to cancel an action
                dconf = doing.conf
                if this.conf['type'] in dconf['cancel_by'] : # can cancel action
                    doing.t_recovery.off()
                    for i in dconf['on_cancel']:
                        i()
                    if this.log:
                        this.log(this.src+'cancel', doing.name,
                                'by '+this.name \
                                +' after %.2fs'%(now()-doing.action_start))
                else:
                    if this.log:
                        this.log(this.src+'failed', this.name, 'cannot cancel')
                    return 0
            doing.status = 2
            this._static.prev = doing # turn this from doing to prev
        this.status = 1
        this.action_start = now()
        this._static.doing = this # setdoing
        if this.log_r:
            if this.name[0] == 'x':
                this.log_r(this.src+this.name)
            else:
                #this.log_r(this.src+'---------', this.name)
                this.log_r(this.src+this._static.prev.name+' -----', this.name)

        if this.speed_cache['spd']>=0 :
            recovery = this.conf['recovery'] / this.speed_cache['spd']
        else:
            recovery = this.conf['recovery'] / this.speed_get('spd')
        this.t_recovery(this.conf['startup'] + recovery)
        return 1

    __call__ = start

    def __str__(this):
        return this.name



if __name__ == '__main__' :
    logset('act')
    logset('debug')

    class C1(object):
        name = 'c1'
        def speed(this):
            return 1
        def __init__(this):
            this.Action = Action(this)
            this.a = this.Action('foo')
            this.a.conf['cancel_by']=['s']
            this.b = this.Action('bar', Conf({'type':'x'}) )
            this.c = this.Action('baz')
            this.c.conf['type'] = 's'

    class C2(object):
        name = 'c2'
        def __init__(this):
            this.action = Action(this)
            this.a = this.action('test')
            this.a.conf['recovery'] = 1


    c = C1()
    c2 = C2()
    c.a()
    c.b()
    c.c()
    c2.a()
    print(repr(c.a))
    Timer.run()
    logcat()

