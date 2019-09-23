

class Conf():
    def __init__(this, template=None):
        if template:
            this.get = template
        else:
            this.get = {'__sync':{}}

    @staticmethod
    def __rsetitem(d, k, v):
        l = k.find('.')
        if l <  0 :
            d[k] = v
        elif l >= 0 :
            p = k[:l]
            c = k[l+1:]
            if p not in d:
                d[p] = {'__sync':{}}
            elif type(d[p]) != dict:
                d[p] = {'__sync':{}}
            Conf.__rsetitem(d[p], c, v)

    @staticmethod
    def __from_dict(d, dic):
        if type(dic) != dict:
            print('cannot from something not dict')
            raise
        for k,v in dic.items():
            Conf.__rsetitem(d, k, v)

    @staticmethod
    def __to_dict(d, pre, get):
        for k, v in get.items():
            if type(v) == dict:
                if '__sync' in v: # class conf
                    Conf.__to_dict(d, pre+k+'.', v)
                elif k!= '__sync':
                    d[pre+k] = v
            else:
                d[pre+k] = v

    def __str__(this):
        r = ""
        d = {}
        Conf.__to_dict(d, '', this.get)
        for k, v in d.items():
            r += "%s=%s\n"%(k, v)
        return r

    def __do_sync(this):
        sync = this.get['__sync']
        for i in sync:
            i(this.get)

    def __set_sync(this, a):
        this.get['__sync'][a] = 1
        a(this.get)

    @staticmethod
    def sync(data):
        for i in data['__sync']:
            i(data)

    def commit(this):
        for i in this.get['__sync']:
            i(this.get)

    def update(this, a):
        if type(a) == dict:
            Conf.__from_dict(this.get, a)
        elif type(a) == this.__class__ :
            d = {}
            Conf.__to_dict(d, '', a.get)
            Conf.__from_dict(this.get, d)
        else:
            print('Conf can only update from Conf/dict')
            raise

    # call a dict/conf = update
    # call a function = add a sync
    # call None = sync
    def __call__(this, a=None):
        if a == None:
            for i in this.get['__sync']:
                i(this.get)
        else:
            t = a.__class__.__name__
            if t == 'dict':
                this.update(a)
            elif t == 'Conf':
                this.update(a)
            elif t == 'instancemethod':
                this.get['__sync'][a] = 1
                a(this.get)
            elif t == 'function':
                this.get['__sync'][a] = 1
                a(this.get)
            elif t == 'method':
                this.get['__sync'][a] = 1
                a(this.get)
            else:
                print('update conf with none dict/conf')
                raise
        return this


class Config(object):
    default = {}
    sync = None
        
    def __init__(this, host, conf=None):
        this.host = host
        tmp = Conf()
        tmp.update(this.default)
        if conf:
            tmp.update(conf)
        if this.sync:
            tmp.get['__sync'][this.__sync] = 1
            this.__sync(tmp.get)
        this.conf_w = tmp

    def __call__(this):
        this.host.conf_w = this.conf_w
        this.host.conf = this.conf_w.get

    def __sync(this, conf):
        this.__class__.sync(this.host, conf)


if __name__ == '__main__':
    a = {
            't2.t3':23
            ,'t2.t4':24
            }
    b = {
            't2.t3':2233
            ,'t2.t5':2255
            }
    c = Conf()(a)
    c(b)

    r = {
            'conf1.test2':22
            ,'conf2.2':2
            }
    root = Conf()(r)

    class Conf_c(Config):
        default = {
                'test1':1
                ,'test2':2
                ,'attr.h1.coef':2
                ,'attr.h1.to_bk':1
                ,'attr.h1.killer':{}
                }
        conf = {
                'test1':11
                ,'attr.h1.coef':3
                }

    root.get = Conf_c(0, root.get['conf1'])()
    print(root)
    print(root.get)



