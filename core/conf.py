

class lobject(object):
    def __init__(this, conf={}):
        for i in conf:
            this[i] = conf[i]

    def __getitem__(this, i):
        l = i.find('.')
        if l >= 1:
            p = i[:l]
            c = i[l+1:]
            return this.__getattribute__(p)[c]
        elif l < 0 and i != '':
            return this.__getattribute__(i)

    def __next__(this):
        return this.__dict__.__next__()

    def __iter__(this):
        return this.__dict__.__iter__()
    

    def __getattr__(this, k):
        if k[:2] != '__':
            i = this.__new__(this.__class__)
            object.__setattr__(this, k, i)
            return i
        else:
            return object.__getattr__(this,k)

    def __setitem__(this, i, v):
        l = i.find('.')
        if l >= 1:
            p = i[:l]
            c = i[l+1:]

            tmp = this.__new__(this.__class__)
            tmp.__setitem__(c,v)
            if p in this:
                if type(this[p]) == this.__class__:
                    this[p](tmp)
                else:
                    object.__setattr__(this, p, tmp)
            else:
                object.__setattr__(this, p, tmp)
            return 
        elif l < 0 and i != '':
            object.__setattr__(this, i, v)
            return
        print('can\' set item')
        errrrrrrrrrrr()
        return

    def __delitem__(this, i):
        v = this.__getattribute__(i)
        del(v)

#} //class lobject


class Conf(lobject):
    __parentname = None
    __name = None
    __idx = 0

    def __init__(this, template={}):
        this.__sync = {}
        if type(template) == dict:
            this.__fromdict(template)
        if type(template) == this.__class__:
            this.__fromdict(template.__todict())


    def __todict(this):
        ret = {}
        for k,v in this.__dict__.items():
            if k[:7] == '_Conf__':
                continue
            if type(v) == this.__class__:
                ret[k] = v.__todict()
            elif type(v) == dict:
                ret[k] = ('___realdict',v)
            else:
                ret[k] = v
        return ret


    def __todict_withname(this):
        ret = {}
        for k,v in this.__dict__.items():
            if type(v) == this.__class__:
                ret[k] = v.__todict_withname()
            elif type(v) == dict:
                ret[k] = ('___realdict',v)
            else:
                ret[k] = v
        return ret


    def __todict_all(this):
        ret = {}
        for k,v in vars(this).items():
            if type(v) == this.__class__:
                ret[k] = v.__todict_all()
            elif type(v) == dict:
                ret[k] = ('___realdict',v)
            else:
                ret[k] = v
        return ret


    def __fromdict(this,dic):
        if type(dic) != dict:
            print('err fromdict')
            errrrrrrrrr()
        for k,v in dic.items():
            if type(v) == tuple and v[0] == '___realdict':
                this[k] = v[1]
            elif type(v) == dict:
                tmp = this.__new__(this.__class__)
                tmp.__fromdict(v)
                this[k] = tmp
            else:
                this[k] = v


    def __str__(this):
        return this.__tostr()


    def __tostr(this):
        ret = ''
        ret2 = ''
        tmp = this.__new__(this.__class__)
        tmp.__init__(this.__todict_withname())
        this = tmp
        if not this.__parentname and not this.__name:
            for k,i in this.__dict__.items():
                if type(i) == Conf:
                    i.__name = k
                    tmp = i.__tostr()
                    ret2 += tmp
                    if tmp == '':
                        ret2+= k+'=Conf()\n'
                elif k[:7]!='_Conf__' :
                #elif k!='_Conf__name' and k!='_Conf__parentname':
                    ret += '%s=%s\n'%(str(k),repr(i))
        elif not this.__parentname and this.__name:
            for k,i in this.__dict__.items():
                if type(i) == Conf:
                    i.__name = k
                    i.__parentname = '%s'%(this.__name)
                    tmp = i.__tostr()
                    ret2 += tmp
                    if tmp == '':
                        ret2+= this.__name+'.'+k+'=Conf()\n'
                elif k[:7]!='_Conf__' :
                #elif k!='_Conf__name' and k!='_Conf__parentname':
                    ret += '%s.%s=%s\n'%(this.__name, k, repr(i))
        else :
            for k,i in this.__dict__.items():
                if type(i) == Conf:
                    i.__name = k
                    i.__parentname = '%s.%s'%(this.__parentname, this.__name)
                    tmp = i.__tostr()
                    ret2 += tmp
                    if tmp == '':
                        ret2+= this.__parentname+'.'+this.__name \
                                +'.'+k+'=Conf()\n'
                elif k[:7]!='_Conf__' :
                #elif k!='_Conf__name' and k!='_Conf__parentname':
                    ret += '%s.%s.%s=%s\n'%(this.__parentname, this.__name,
                            k, repr(i))
        return ret+ret2


    @staticmethod
    def showsync(this):
        for i in this.__sync:
            print(this.__sync[i])


    @staticmethod
    def show(this, name):
        this.__name = name
        print(this)


    @staticmethod
    def update(this, a):
        if type(a) == dict:
            tmp = this.__new__(this.__class__)
            tmp.__fromdict(a)
            a = tmp
        if type(a) == Conf:
            for k,i in a.__dict__.items():
                if type(i) == Conf:
                    if k in this :
                        if type(this[k]) == Conf:
                            Conf.update(this[k], i)
                            continue
                this[k] = i
        else:
            print('Conf can only update from Conf/dict')
            errrrrrrrrrrrrrrrrrrrr()


    def __add__(this, a):
        if type(a) != Conf:
            print('Conf can only add Conf')
            errrrrrrrrrrrrrrrrrrrr()
            return
        merge = this.__new__(this.__class__)
        merge.__init__(this)
        for k,i in a.__dict__.items():
            if k not in merge:
                merge[k] = i
            elif type(i) == Conf and type(merge[k]) == Conf:
                merge[k] = merge[k] + i
            else:
                merge[k] = i
        return merge


    # call a dict/conf = update
    # call a function = add a sync
    # call None = sync
    def __call__(this, a=None):
        if type(a) == this.__class__:
            Conf.update(this, a)
        elif type(a) == dict:
            Conf.update(this, a)
        elif type(a).__name__ == 'instancemethod':
            this.__sync[this.__idx] = a
            this.__idx += 1
            return this.__idx-1
        elif type(a).__name__ == 'function':
            this.__sync[this.__idx] = a
            this.__idx += 1
            return this.__idx-1
        elif type(a).__name__ == 'method':
            this.__sync[this.__idx] = a
            this.__idx += 1
            return this.__idx-1
        elif a==None:
            this.__dosync()
        else:
            print('update conf with none dict/conf')
            errrrrrrrrrrrrrrrrrrr()



    def __dosync(this):
        for i in this.__sync :
            this.__sync[i](this)


class Config(Conf):
    def default(this, conf):
        pass
    def config(this, conf):
        pass
    def sync(this, conf):
        print('config sync')
        pass

    def __new__(cls, host, conf=None):
        tmp = Conf()
        cls.default(host, conf)
        cls.config(host, conf)
        def sync(conf):
            cls.sync(host, conf)
        if conf:
            tmp(conf)
            conf(tmp)
            conf(sync)
            return conf
        else:
            tmp(sync)
            return tmp







if __name__ == '__main__':
    def foo(e):
        print('foo')
        print(e)
        pass
    a = Conf()
    for i in a:
        print(i, a[i])
    exit()
    print(a)
    exit()
    a.b = 'b'
    a.c.d = 'c.d'
    a(foo)
    if 'd' in a :
        print('if')
    else:
        print('else')

    if 'b' in a :
        print('if')
    else:
        print('else')

    a = Conf()
    a.b = 'b'
    a.c = 'c'

    class C(Config):
        def sync(this, conf):
            this.sync = conf.default

        def default(this, conf):
            conf.default = this.d

    class A():
        def __init__(this, conf):
            this.d = 'default'
            this.conf = C(this, conf)

    c = Conf()
    c.a = 'a'
    a = A(c)
    c.b = 'b'
    c()
    print(c)
    print(a.sync)
