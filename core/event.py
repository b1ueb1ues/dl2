

_g_event_listeners = {}


def add_event_listener(eventname, listener): #listener should be a function
    global _g_event_listeners

    if eventname in _g_event_listeners:
        _g_event_listeners[eventname].append(listener)
    else:
        _g_event_listeners[eventname] = [listener]


def get_event_trigger(eventname, trigger = []): 
    global _g_event_listeners
    if eventname in _g_event_listeners:
        return _g_event_listeners[eventname]
    else:
        _g_event_listeners[eventname] = []
        return _g_event_listeners[eventname]


class Listener(object):
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
                add_event_listener(i, this.__cb)
        else:
            add_event_listener(this.__eventname, this.__cb)
        this.__online = 1

    def pop(this):
        this.off()
        return this.__cb

    def off(this):
        if not this.__online:
            return 
        if type(this.__eventname) == list or type(this.__eventname) == tuple:
            for i in this.__eventname:
                els = get_event_trigger(i)
                idx = els.index(this.__cb)
                els.pop(idx)
        else:
            els = get_event_trigger(this.__eventname)
            idx = els.index(this.__cb)
            els.pop(idx)
        this.__online = 0
        return this

#} class Listener


class Event(object):

    @classmethod
    def init(cls, el=None):
        global _g_event_listeners
        if not el:
            el = {}
            el['event_listeners'] = {}
        _g_event_listeners = el['event_listeners']
        return el


    def __init__(this, name=None):
        if name :
            this.name = name
            this.__name = name
            this._trigger = get_event_trigger(name)
        else:
            this._trigger = []

    def __call__(this):
        for i in this._trigger:
            i(this)

    on = __call__

    def __str__(this):
        return this.__name

#} class Event


if __name__ == '__main__' :

    def foo():
        def lis(e):
            print('listener1')
        Listener('e1')(lis)
        Event('e1')()

    import dis
    dis.dis(foo)


