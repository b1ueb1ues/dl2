import __init__

class Ability(object):
    def __init__(this, host):
        if not host:
            print('ability need a character as host')
            errrrrrrrrrrr()
        this.host = host

    
    def __call__(this, name, classname, *args, **kwargs):
        import ability
        abilities = vars(ability)
        abilities[classname]._static = this
        abilities[classname].host = this.host
        this.a = abilities[classname](name, *args, **kwargs)
        this.a.host = this.host
        return this.a
    

    def get_sub(this):
        this.subclasses = {}
        for i in this.__class__.__subclasses__():
            this.subclasses[i.__name__] = i
        return this.subclasses


    def init(this):
        pass
