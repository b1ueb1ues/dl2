
_initialize = 0
class Weapon(object):
    a = []
    s3 = None
    def __init__(this, host=None):
        global _initialize
        if not _initialize:
            if not host:
                print('Amulet need a character as host')
                errrrrrrrrrrr()
            _initialize = 1
            this.host = host
            this.subclasses = {}
            for i in this.__class__.__subclasses__():
                this.subclasses[i.__name__] = i

    
    def __call__(this, wt, name):
        global _max
        import weapon
        weapons = vars(weapon.type_[wt])
        weapons[name]._static = this
        weapons[name].host = this.host
        this.w = weapons[name]()
        return this.w


    def init(this):
        if this.host.ele in this.ele:
            this.atk *= 1.5
            if this.s3 :
                this.host.conf.s3(this.s3)
                this.host.conf.s3()

            idx = 0
            for i in this.a:
                idx += 1
                this.host.Ability('weapon_a%d'%idx, *i)()



