
class Slot(object):
    atk = 0
    ele = 'none'
    wt = 'none'
    stype = 'slot'
    onele = 0
    onwt = 0

    a = None
    conf = None

    def __init__(this):
        if not this.mod:
            this.mod = []
        if not this.conf:
            this.conf = Conf()
        if not this.a:
            this.a = []

    def setup(this, c):
        if c.ele == this.ele :
            this.onele = 1
        if c.wt == this.wt :
            this.onwt = 1


    def oninit(this, adv):
        adv.conf(this.conf)

        i = this.stype
        j = this.mod
        if type(j) == tuple:
            adv.Modifier(i,*j)
        elif type(j) == list:
            idx = 0
            for k in j:
                adv.Modifier(i+'_%d'%idx,*k)
                idx += 1
        elif type(j) == dict:
            idx = 0
            for k in j:
                adv.Modifier(i+k+'_%d'%idx,*j[k])
                idx += 1



