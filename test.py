import _collections_abc


class Mydict(_collections_abc.MutableMapping):

    # Start by filling-out the abstract methods
    def __init__(*args, **kwargs):
        if not args:
            raise TypeError("descriptor '__init__' of 'UserDict' object "
                            "needs an argument")
        self, *args = args
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        if args:
            dict = args[0]
        elif 'dict' in kwargs:
            dict = kwargs.pop('dict')
            import warnings
            warnings.warn("Passing 'dict' as keyword argument is deprecated",
                          DeprecationWarning, stacklevel=2)
        else:
            dict = None
        self.__data = {}
        if dict is not None:
            self.update(dict)
        if len(kwargs):
            self.update(kwargs)
    def __len__(self): return len(self.__data)
    def __getitem__(self, key):
        if key in self.__data:
            return self.__data[key]
        if hasattr(self.__class__, "__missing__"):
            return self.__class__.__missing__(self, key)
        raise KeyError(key)
    def __setitem__(self, key, item): self.__data[key] = item
    def __delitem__(self, key): del self.__data[key]
    def __iter__(self):
        return iter(self.__data)

    # Modify __contains__ to work correctly when __missing__ is present
    def __contains__(self, key):
        return key in self.__data

    # Now, add the methods in dicts but not in MutableMapping
    def __repr__(self): return repr(self.__data)
    def __copy__(self):
        inst = self.__class__.__new__(self.__class__)
        inst.__dict__.update(self.__dict__)
        # Create a copy and avoid triggering descriptors
        inst.__dict__["__data"] = self.__dict__["__data"].copy()
        return inst

    def copy(self):
        if self.__class__ is UserDict:
            return UserDict(self.__data.copy())
        import copy
        __data = self.__data
        try:
            self.__data = {}
            c = copy.copy(self)
        finally:
            self.__data = __data
        c.update(self)
        return c

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __getattr__(this, k):
        return this.__data[k]


    def __setattr__(this, k, v):
        super().__setattr__(k, v)
        if k != '_Mydict__data':
            this.__data[k]=v

    @classmethod
    def data(cls, this):
        return this.__data


class Conf(Mydict):
    def __init__(this, template=None):
        super().__init__()
        if not template :
            return 
        this.__from_shallow_dict(template)
        object.__setattr__(this, '_Conf__sync', {})
        object.__setattr__(this, '_Conf__idx', 0)


    def __from_shallow_dict(this, dic):
        if type(dic) != dict:
            print('cannot from something not dict')
            raise
        for k,v in dic.items():
            this.__rsetitem(k, v)


    def __to_dict(this, r, pre, data):
        for i in data:
            if type(data[i]) == this.__class__:
                this.__to_dict(r, pre+i+'.', data[i])
            else:
                r[pre+i] = data[i]


    def __str__(this):
        r = ""
        d = {}
        this.__to_dict(d, '', this)
        for k, v in d.items():
            r += "%s=%s\n"%(k, v)
        return r


    def __do_sync(this):
        for i in this.__sync:
            this.__sync[i](this)


    def __call__(this, p=None):
        if not p :
            this.__do_sync()
        elif type(p).__name__ == 'instancemethod':
            this.__sync[this.__idx] = p
            this.__idx += 1
            p(this)
            return this.__idx-1
        elif type(p).__name__ == 'function':
            this.__sync[this.__idx] = p
            this.__idx += 1
            p(this)
            return this.__idx-1
        elif type(p).__name__ == 'method':
            this.__sync[this.__idx] = p
            this.__idx += 1
            p(this)
            return this.__idx-1




    def __rsetitem(this, k, v):
        l = k.find('.')
        if l >= 1:
            p = k[:l]
            c = k[l+1:]
            if p not in this:
                this[p] = Conf()
            this[p].__rsetitem(c, v)
        elif l < 0 and k != '':
            this[k] = v
        else:
            print('can\' set item')
            raise


class Config():
    def default(this, conf):
        conf.a1 = 1
        conf.a2 = 2


    def __init__(this, conf):
        pass

if __name__ == '__main__':
    d = {
            'test':1
            ,'test2.test3':3
            }
    a = Conf(d)

    def foo(c):
        print('<foo>')
        print(c)
        print('</foo>')

    a(foo)
    a()
    print(a)
    

