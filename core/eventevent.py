

class Event(object):
    def __init__(this, host):
        this.host = host
        this._event_listeners = {}
    def __call__(this, name):
        return _Event(this._event_listeners, name)

class _Event(object):
    def __init__(this, el, name):
        this._event_listeners = el
        this.__name = name
        this._trigger = this.get_event_trigger(name)

    def __call__(this):
        for i in this._trigger:
            i(this)

    on = __call__

    def __str__(this):
        return this.__name

    def get_event_trigger(this, eventname): 
        if eventname in this._event_listeners:
            return this._event_listeners[eventname]
        else:
            this._event_listeners[eventname] = []
            return this._event_listeners[eventname]
#} class Event

class Listener(object):
    def __init__(this, event):
        this._event_listeners = event._event_listeners
    def __call__(this, name):
        return _Listener(this._event_listeners, name)


class _Listener(object):
    def __init__(this, el, eventname):
        this._event_listeners = el
        this.__eventname = eventname
        this.__online = 0

    def __call__(this, cb):
        this.__cb = cb
        this.on()
        return this

    def on(this, cb=None):
        if this.__online :
            return 
        if cb :
            this.__cb = cb
        if type(this.__eventname) == list or type(this.__eventname) == tuple:
            for i in this.__eventname:
                this.add_event_listener(i, this.__cb)
        else:
            this.add_event_listener(this.__eventname, this.__cb)
        this.__online = 1

    def pop(this):
        this.off()
        return this.__cb

    def off(this):
        if not this.__online:
            return 
        if type(this.__eventname) == list or type(this.__eventname) == tuple:
            for i in this.__eventname:
                els = this.get_event_trigger(i)
                idx = els.index(this.__cb)
                els.pop(idx)
        else:
            els = this.get_event_trigger(this.__eventname)
            idx = els.index(this.__cb)
            els.pop(idx)
        this.__online = 0
        return this

    #listener should be a function
    def add_event_listener(this, eventname, listener): 
        if eventname in this._event_listeners:
            this._event_listeners[eventname].append(listener)
        else:
            this._event_listeners[eventname] = [listener]

    def get_event_trigger(this, eventname): 
        if eventname in this._event_listeners:
            return this._event_listeners[eventname]
        else:
            this._event_listeners[eventname] = []
            return this._event_listeners[eventname]
#} class Listener



if __name__ == '__main__' :
    def lis(e):
        print('listener1')
    def lis2(e):
        print('listener2')
    def lis3(e):
        print('listener3')

    class A():
        pass
    this = A()
    this.Event = Event()
    this.Listener = Listener(this.Event)
    this.Listener('e1')(lis)
    this.Event('e1')()
    this.E2 = Event()
    this.L2 = Listener(this.E2)
    this.L2('e1')(lis2)
    this.E2('e1')()
    this.Event('e1')()

