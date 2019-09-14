

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



class X(object):
    def __init__(this, Actionbase):
        this.Actionbase = Actionbase


    def __call__(this, *args, **kwargs):
        a = this.Actionbase(*args, **kwargs)
        a.conf.type = 'x'
        a.conf.interrupt_by = ['fs','s','dodge']
        a.conf.cancel_by = ['fs','s','dodge']
        return a


class FS(object):
    def __init__(this, Actionbase):
        this.Actionbase = Actionbase


    def __call__(this, *args, **kwargs):
        a = this.Actionbase(*args, **kwargs)
        a.conf.type = 'fs'
        a.conf.interrupt_by = ['s']
        a.conf.cancel_by = ['s','dodge']
        return a


class S(object):
    def __init__(this, Actionbase):
        this.Actionbase = Actionbase


    def __call__(this, *args, **kwargs):
        a = this.Actionbase(*args, **kwargs)
        a.conf.type = 's'
        return a


class Dodge(object):
    def __init__(this, Actionbase):
        this.Actionbase = Actionbase


    def __call__(this, *args, **kwargs):
        a = this.Actionbase(*args, **kwargs)
        a.conf.type = 'dodge'
        a.conf.cancel_by = ['fs','s']
        return a


