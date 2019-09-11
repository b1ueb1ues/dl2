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


class _Action(object):   
    def default(this, conf):
        conf.startup = 0.1
        conf.recovery = 1.9

    def __init__(this, name=None, conf=None):  ## can't change name after this
        # conf : startup, recovery, active, action
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

        this.atype = this.name

        this.index = 0
        this.recover_start = 0
        this.startup_start = 0
        this.__startup = 0
        this.__recovery = 0
        this.status = -2 # -2nop -1startup 0doing 1recovery
        this.idle = 0

        this.cancel_by = []
        this.interrupt_by = []

        this.t_startup = Timer(this._cb_acting)
        this.t_recovery = Timer(this._cb_act_end)
        this.e_idle = Event('idle')

        tmp = Conf()
        this.default(tmp)
        if conf :
            tmp(conf)
            conf(tmp)
            tmp = conf
        this.conf = tmp
        this.conf.sync_action = this.sync



    def sync(this, c, cc):
        this.__startup = c.startup
        this.__recovery = c.recovery
        #this.__active = c.active
        if 'action' in c:
            this.act = c.action

    def __call__(this):
        return this.start()
    
    def get_doing(this):
        return this._static.doing
    def set_doing(this):
        this._static.doing = this
    def get_prev(this):
        return this._static.prev
    def set_prev(this):
        this._static.prev = this._static.doing


    def get_recovery(this):
        return this.__recovery / this.speed()


    def get_startup(this):
        return this.__startup / this.speed()


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
            log('act', this.src+'end', this.name)
            this.status = -2
            this._static.prev = this # turn this from doing to prev
            this.idle = 1
            this.e_idle()


    def _act(this):
        log('act',this.src+'active',this.name)
        this.act(this)


    def act(this, action):
        Event(this.atype)()


    def start(this):
        doing = this._static.doing

        if doing.idle :
            log('act',this.src+'start',this.name, 'idle:%d'%doing.status)
        else:
            log('act',this.src+'start',this.name, 'doing '+doing.name+':%d'%doing.status)
            if doing == this : # self is doing
                log('act',this.src+'failed',this.name, 'self is doing')
                return 0

        #if doing.idle # idle
        #    pass
        if not doing.idle : # doing != this
            if doing.status == -1: # try to interrupt an action
                if this.atype in doing.interrupt_by : # can interrupt action
                    doing.t_startup.off()
                    log('act', this.src+'interrupt', doing.name , 'by '+this.name+'\t'+'after %.2fs'%(now()-doing.startup_start) )
                else:
                    log('act',this.src+'failed', this.name)
                    return 0
            elif doing.status == 1: # try to cancel an action
                if this.atype in doing.cancel_by : # can interrupt action
                    doing.t_recovery.off()
                    log('act', this.src+'cancel', doing.name , 'by '+this.name+'\t'+'after %.2fs'%(now()-doing.recover_start) )
                else:
                    log('act',this.src+'failed', this.name)
                    return 0
            elif doing.status == 0:
                print('err in action start()')
                errrrrrrrrrrrr()
            this._static.prev = this._static.doing # turn this from doing to prev
        this.idle = 0
        this.status = -1
        this.startup_start = now()
        this.t_startup(this.get_startup())
        this._static.doing = this # setdoing
        #if now() <= 3:
        #    log('debug','tap,startup', this.get_startup())
        return 1


    def __str__(this):
        return this.name


class X(Action):
    def __init__(this, name, conf, act=None):
        Action.__init__(this, name, conf, act)
        this.atype = 'x'
        this.interrupt_by = ['fs','s','dodge']
        this.cancel_by = ['fs','s','dodge']


    def realtime(this):
        this.act_event = Event('x')
        this.act_event.name = this.name
        this.rt_name = this.name
        this.tap, this.o_tap = this.rt_tap, this.tap


    def rt_tap(this):
        if this.rt_name != this.name:
            if this.atype == this.rt_name:
                this.atype = this.name
            this.rt_name = this.name
            this.act_event.name = this.name
        return this.o_tap()


class Fs(Action):
    def __init__(this, name, conf, act=None):
        Action.__init__(this, name, conf, act)
        this.atype = 'fs'
        this.interrupt_by = ['s']
        this.cancel_by = ['s','dodge']


    def realtime(this):
        this.act_event = Event('fs')
        this.act_event.name = this.name


class Fs_group(object):
    def __init__(this, name, conf, act=None):
        this.actions = {}
        this.conf = conf
        fsconf = conf.fs
        xnfsconf = [fsconf,fsconf,fsconf,fsconf,fsconf,fsconf]

        for i in range(5):
            xnfs = 'x%dfs'%(i+1)
            if xnfs in this.conf:
                xnfsconf[i] += this.conf[xnfs]

        if 'dfs' in this.conf:
            xnfsconf[5] += this.conf.dfs

        this.add('default', Fs(name, fsconf     , act))
        this.add('x1',      Fs(name, xnfsconf[0], act))
        this.add('x2',      Fs(name, xnfsconf[1], act))
        this.add('x3',      Fs(name, xnfsconf[2], act))
        this.add('x4',      Fs(name, xnfsconf[3], act))
        this.add('x5',      Fs(name, xnfsconf[4], act))
        this.add('dodge',   Fs(name, xnfsconf[5], act))


    def add(this, name, action):
        this.actions[name] = action


    def __call__(this, before):
        if before in this.actions:
            return this.actions[before]()
        else:
            return this.actions['default']()


class Dodge(Action):
    def __init__(this, name, conf, act=None):
        Action.__init__(this, name, conf, act)
        this.atype = 'dodge'
        this.cancel_by = ['fs','s']


    def realtime(this):
        this.act_event = Event('dodge')
        this.act_event.name = this.name


class S(Action):
    def __init__(this, name, conf, act=None):
        Action.__init__(this, name, conf, act)
        this.atype = 's'
        this.interrupt_by = []
        this.cancel_by = []


    def realtime(this):
        this.act_event = Event('s')
        this.act_event.name = this.name


    def _act(this, partidx):
        this.idx = partidx
        log('act',this.name)

        this.act(this)

        this.act_event.name = this.name
        this.act_event.idx = this.idx
        this.act_event()



if __name__ == '__main__' :
    logset('act')
    logset('debug')

    class C1(object):
        name = 'c1'
        def __init__(this):
            this.action = Action(this)
            this.a = this.action('foo')
            this.a.interrupt_by = ['bar']
            this.b = this.action('bar')
            this.c = this.action('baz')

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

