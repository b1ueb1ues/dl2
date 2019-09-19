
class Dragon(object):
    a = []
    s3 = None
    def __init__(this, host=None):
        if not host:
            print('dragon need a character as host')
            errrrrrrrrrrr()
        this.host = host

    
    def get_sub(this):
        this.subclasses = {}
        for i in this.__class__.__subclasses__():
            this.subclasses[i.__name__] = i
        return this.subclasses


    def __call__(this, name):
        import dragon
        dragons = vars(dragon)
        dragons[name]._static = this
        this.d = dragons[name](this.host)

        return this.d


    def init(this):
        if this.host.ele in this.ele:
            this.atk *= 1.5

            idx = 0
            for i in this.a:
                idx += 1
                this.host.Ability('dragon_a%d'%idx, *i)()



