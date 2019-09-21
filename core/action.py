import __init__
from core.ctx import *


class Action(object):
    def __init__(this, host):
        this.host = host

        class Nop(object):
            conf = Conf()
            name = '__idle__'
            status = -1

        this.nop = Nop()

        this.prev = this.nop
        this.doing = this.nop

        this.speed = this.host.speed


    def __call__(this, *args, **kwargs):
        return _Action(this, *args, **kwargs)


class Conf_Action(Config):
    default = {
            'type'      : this.name
            ,'startup'   : 0
            ,'recovery'  : 2
            ,'cancel_by' : []
            ,'on_cancel' : None
            ,'on_end'    : None
            }

    def sync(this, conf):
        pass
        this.atype     = conf['type']
        this.startup   = conf['startup']
        this.recovery  = conf['recovery']
        this.cancel_by = conf['cancel_by']
        this.on_cancel = conf['on_cancel']
        this.on_end    = conf['on_end']


class _Action(object):   
    def __init__(this, static, name, conf=None):  
        ## can't change name after this
        this._static = static
        this.name = name
        this.conf = Conf_Action(this, conf)

        this.hostname = this._static.host.name
        this.src = this.hostname + ', '

        this.speed = this._static.speed

        this.action_start = 0
        this.status = 0 # -1: idle/end 0:wait 1:doing 2cancel

        this.t_recovery = Timer(this._cb_act_end)
        this.e_idle = Event('idle')
        this.e_idle.host = this._static.host

        this.log = Logger('act')


    def __call__(this):
        return this.start()
    

    def get_recovery(this):
        return this.conf.get['recovery'] / this.speed()


    def _cb_act_end(this, e):
        if this._static.doing != this:
            return 

        if this.log:
            this.log(this.src+'end', this.name)
        this.status = -1
        this._static.prev = this # turn this from doing to prev

        if this.on_end:
            this.on_end()
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
                if this.conf.get['type'] in doing.cancel_by : # can cancel action
                    doing.t_recovery.off()
                    if doing.on_cancel:
                        doing.on_cancel()
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
        this.t_recovery(this.conf.get['startup'] + this.get_recovery())
        return 1


    def __str__(this):
        return this.name



if __name__ == '__main__' :
    logset('act')
    logset('debug')

    class C1(object):
        name = 'c1'
        def __init__(this):
            this.Action = Action(this)
            this.a = this.Action('foo')
            this.a.conf.cancel_by=['s']
            this.a.conf()
            this.b = this.Action('bar', Conf({'type':'x'}) )
            this.c = this.Action('baz')
            this.c.conf.type = 's'
            this.c.conf()

    class C2(object):
        name = 'c2'
        def __init__(this):
            this.action = Action(this)
            this.a = this.action('test')


    c = C1()
    c2 = C2()
    c.a()
    c.b()
    c.c()
    c2.a()
    print(repr(c.a))
    Timer.run()
    logcat()

