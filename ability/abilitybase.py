
_initialize = 0
class Ability(object):
    def __init__(this, host):
        global _initialize
        if not _initialize:
            _initialize = 1
            this.host = host
            this.subclasses = {}
            for i in this.__class__.__subclasses__():
                this.subclasses[i.__name__] = i

    
    def __call__(this, name, classname, *args, **kwargs):
        ability = this.subclasses[classname]
        ability._static = this
        ability.host = this.host
        return ability(name, *args, **kwargs)


    def init(this):
        pass
