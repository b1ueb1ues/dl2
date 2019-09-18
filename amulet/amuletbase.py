import __init__

_max = {
       'atk'           : 0.20   # attack
      , 'fs'           : 0.50   # force strike
      , 'sd'           : 0.40   # skill damage
      , 'cc'           : 0.15   # crit chance
      , 'cd'           : 0.25   # crit damage
      , 'sp'           : 0.15   # skill haste

      , 'bt'           : 0.30   # buff time

      , 'bk'           : 0.30   # break killer
      , 'od'           : 0.15   # od killer

      , 'lo'           : 0.60   # lastoffence
      , 'def_c_atk'    : 0.15   # buffchain
      , 'def_c_energy' : 0.15   # buffchain
      , 'sts'          : 0.06   # striker strength
      , 'sls'          : 0.06   # slayer stength
      , 'dc'           : 3      # dragon claw
      , 'prep'         : 1      # skill prep

      , 'k_burn'       : 0.30   # burn killer
        }

_initialize = 0
class Amulet(object):
    a = []
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

    
    def __call__(this, classname1, classname2):
        global _max
        import amulet
        this.a1 = vars(amulet)[classname1](this.host)
        this.a2 = vars(amulet)[classname2](this.host)
        this.atk = this.a1.atk + this.a2.atk
        this.tmp = this.a1.a + this.a2.a
        this.a = {}

        for i in this.tmp:
            if len(i)==2 or (len(i)==3 and i[2]==None):
                k = i[0]
                if k not in _max:
                    this.merge(this.a, i)
                elif _max[k] > 0:
                    if _max[k] > i[1]:
                        this.merge(this.a, i)
                        _max[k] -= i[1]
                    else :
                        i = (i[0],_max[k])
                        this.merge(this.a, i)
                        _max[k] = 0

        for i in this.tmp:
            if len(i)==3 and i[2]!=None:
                k = i[0]
                if k not in _max:
                    this.merge_cond(this.a, i)
                elif _max[k] > 0:
                    if _max[k] > i[1]:
                        this.merge_cond(this.a, i)
                        _max[k] -= i[1]
                    else:
                        i = (i[0],_max[k],i[2])
                        this.merge_cond(this.a, i)
                        _max[k] = 0

        tmp = []
        for k,i in this.a.items():
            tmp.append(i)
        this.a = tmp
        return this


    def init(this):
        idx = 0
        for i in this.a:
            idx += 1
            this.host.Ability('amulet_a%d'%idx, *i)()


    def merge(this, a, b):
        k = b[0]
        if k not in a:
            a[k] = b
        else:
            a[k] = (b[0],a[k][1]+b[1])

    def merge_cond(this, a, b):
        k = b[0]+b[2]
        if k not in a:
            a[k] = b
        else:
            a[k] = (b[0],a[k][1]+b[1],b[2])
