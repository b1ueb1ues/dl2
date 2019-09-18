
_initialize = 0
class Dragon(object):
    a = []
    s3 = None
    def __init__(this, host=None):
        global _initialize
        if not _initialize:
            if not host:
                print('dragon need a character as host')
                errrrrrrrrrrr()
            _initialize = 1
            this.host = host
            this.subclasses = {}
            for i in this.__class__.__subclasses__():
                this.subclasses[i.__name__] = i

    
    def __call__(this, name):
        global _max
        import dragon
        dragons = vars(dragon)
        dragons[name]._static = this
        dragons[name].host = this.host
        this.d = dragons[name]()

        return this.d


    def init(this):
        if this.host.ele in this.ele:
            this.atk *= 1.5

            idx = 0
            for i in this.a:
                idx += 1
                this.host.Ability('dragon_a%d'%idx, *i)()



