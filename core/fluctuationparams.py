import benchmark

class Param(object):
    class Handler(object):
        def __init__(this, p_data, host, t):
            this.p_data = p_data
            this.l_param = host.param[t]
            this.d_cache = host.cache
            this.cachename = t

        def set(this, v):
            this.p_data[0] = v
            this.d_cache[this.cachename] = None

        def get(this):
            return this.p_data[0]
        
        def rm(this):
            this.l_param.remove(this.p_data)
            this.d_cache[this.cachename] = None
        off = rm
        

    def __init__(this, register):
        this.param = {}
        this.cache = {}
        for i in register:
            this.param[i] = []
            this.cache[i] = None

    def __call__(this, t):
        tmp = [0]
        this.param[t].append(tmp)
        return Param.Handler(tmp, this, t)
    new = __call__
    
    def get(this, t):
        if this.cache[t] != None:
            return this.cache[t]
        tmp = 0
        for p_i in this.param[t]:
            tmp += p_i[0]
        this.cache[t] = tmp
        return tmp

    def _get(this, t):
        tmp = 0
        for p_i in this.param[t]:
            tmp += p_i[0]
        this.cache[t] = tmp
        return tmp

    def copy_this_content_to_make_a_inline_get_manualy():
        cache = param.cache
        get = param._get
        if cache[t] != None:
            cache[t]
        else:
            get(t)



def main():
    p = Param(['atk','def'])
    h1 = p.new('atk')
    h2 = p.new('atk')
    h3 = p.new('atk')
    h1.set(1)
    h2.set(2)
    h3.set(3)
    cache = p.cache
    get = p._get
    t = 'atk'
    if cache[t] != None:
        print('cache')
        r = cache[t]
    else:
        print('sum')
        r = get(t)
    print(r)

    h2.rm()

    if cache[t] != None:
        print('cache')
        r = cache[t]
    else:
        print('sum')
        r = get(t)
    print(r)

    if cache[t] != None:
        print('cache')
        r = cache[t]
    else:
        print('sum')
        r = get(t)
    print(r)
    
if __name__ == '__main__':
    #benchmark.run(main, 10000)
    main()

