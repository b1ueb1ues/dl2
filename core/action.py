import __init__
from core.ctx import *


class Action(object):
    def __init__(this, host):
        this.host = host
        def nospeed():
            return 1

        class Nop(object):
            name = '__idle__'
            index = 0
            status = -2
            idle = 1

        this.nop = Nop()

        this.prev = this.nop
        this.doing = this.nop
        this.spd = nospeed


    def __call__(this, *args, **kwargs):
        class __Action(_Action):
            _static = this
        return __Action(*args, **kwargs)


class Conf_Action(Config):
    def default(this, conf):
        conf.lag          = 0
        conf.startup      = 0
        conf.recovery     = 120
        conf.interrupt_by = []
        conf.cancel_by    = []
        conf.type         = this.name


    def sync(this, conf):
        this.atype        = conf.type
        this.lag          = conf.lag
        this.startup      = conf.startup
        this.recovery     = conf.recovery
        this.interrupt_by = conf.interrupt_by
        this.cancel_by    = conf.cancel_by


class _Action(object):   
    def __init__(this, name=None, conf=None, active=None):  
        ## can't change name after this
        #  conf : startup, recovery, active
        this.hostname = this._static.host.name
        this.src = this.hostname + ', '
        if name != None:
            if type(name) == tuple:
                this.name = name[0]
                this.index = name[1]
            else:
                this.name = name
                this.index = 0
        else:
            this.name = '_Action'
        if active:
            this.act = active

        this.index = 0
        this.recover_start = 0
        this.startup_start = 0
        this.status = -2 # -2nop -1startup 0doing 1recovery
        this.idle = 0

        this.t_startup = Timer(this._cb_acting)
        this.t_recovery = Timer(this._cb_act_end)
        this.e_idle = Event('idle')

        this.conf = Conf_Action(this, conf)
        this.log = Logger('act')


    def __call__(this):
        return this.start()
    

    def get_recovery(this):
        return this.recovery / this.speed()


    def get_startup(this):
        return this.startup / this.speed()


    def speed(this):
        return this._static.spd()


    def _cb_acting(this, e):
        if this._static.doing == this:
            this.status = 0
            this._act()
            this.status = 1
            this.recover_start = now() 
            this.t_recovery(this.get_recovery())


    def _cb_act_end(this, e):
        if this._static.doing == this:
            if this.log:
                this.log(this.src+'end', this.name)
            this.status = -2
            this._static.prev = this # turn this from doing to prev
            this.idle = 1
            this.e_idle()


    def _act(this):
        if this.log:
            this.log(this.src+'active',this.name)
        this.act(this)


    def act(this, action):
        Event(this.atype)()


    def start(this):
        doing = this._static.doing

        if doing.idle :
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

        #if doing.idle # idle
        #    pass
        if not doing.idle : # doing != this
            if doing.status == -1: # try to interrupt an action
                if this.atype in doing.interrupt_by : # can interrupt action
                    doing.t_startup.off()
                    if this.log:
                        this.log(this.src+'interrupt', doing.name,
                                'by '+this.name \
                                +'\tafter %.2fs'%(now()-doing.startup_start) )
                else:
                    if this.log:
                        this.log(this.src+'failed', this.name)
                    return 0
            elif doing.status == 1: # try to cancel an action
                if this.atype in doing.cancel_by : # can interrupt action
                    doing.t_recovery.off()
                    if this.log:
                        this.log(this.src+'cancel', doing.name , 'by '+this.name+'\t'+'after %.2fs'%(now()-doing.recover_start) )
                else:
                    if this.log:
                        log('act',this.src+'failed', this.name)
                    return 0
            elif doing.status == 0:
                print('err in action start()')
                errrrrrrrrrrrr()
            this._static.prev = this._static.doing # turn this from doing to prev
        this.idle = 0
        this.status = -1
        this.startup_start = now()
        this.t_startup(this.get_startup()+this.lag)
        this._static.doing = this # setdoing
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
            this.X = X(this.Action)
            this.S = S(this.Action)
            this.a = this.X('foo')
            this.b = this.S('bar')
            this.c = this.X('baz')

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

