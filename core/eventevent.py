
class Event(object):
    @classmethod
    def init(cls):
        cls._event_listeners = {}

    def __init__(this, name):
        if name :
            this.name = name
            this.__name = name
            this._trigger = this.get_event_trigger(name)
        else:
            this._trigger = []

    def __call__(this):
        for i in this._trigger:
            i(this)

    on = __call__

    def __str__(this):
        return this.__name

    def get_event_trigger(this, eventname, trigger = []): 
        if eventname in this._event_listeners:
            return this._event_listeners[eventname]
        else:
            this._event_listeners[eventname] = []
            return this._event_listeners[eventname]
#} class Event


class Listener(object):
    @classmethod
    def init(cls, event):
        cls._event_listeners = event._event_listeners

    def __init__(this, eventname):
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

    def get_event_trigger(this, eventname, trigger = []): 
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

    Event.init()
    Listener.init(Event)
    Listener('e1')(lis)
    Event('e1')()

    class E(Event):
        pass
    class L(Listener):
        pass
    E.init()
    L.init(E)
    L('e1')(lis2)
    E('e1')()
    print('-')
    Listener('e1')(lis3)
    Event('e1')()

