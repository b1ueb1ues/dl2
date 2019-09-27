import __init__
from ability.abilitybase import *
from core.ctx import *

class atk(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            this.condi = 'hp>70%'
            this.passive = this.host.Passive('%s_atk'%name, v, 'atk')
        elif c == 'hp100':
            this.condi = 'hp=100%'
            this.passive = this.host.Passive('%s_atk'%name, v, 'atk')
        elif c == 'hit15':
            this.condi = 'hit>=15'
            this.on = 0
            this.passive = this.host.Passive('%s_atk'%name, 0, 'atk')
            Event('hit')(this.l_hit)
        else:
            this.passive = this.host.Passive('%s_atk'%name, v, 'atk')


    def l_hit(this, e):
        if this.on :
            if e.hit < 15 :
                this.on = 0
                this.passive.set(0)
        else:
            if e.hit >= 15 :
                this.on = 1
                this.passive.set(this.v)


    def __call__(this):
        this.passive()


class fs(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_fs'%name, v, 'fs')


    def __call__(this):
        this.passive()


class sd(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            condi = 'hp>70%'
        elif c == 'hp100':
            condi = 'hp=100%'
        this.passive = this.host.Passive('%s_s'%name, v, 's')


    def __call__(this):
        this.passive()


class cc(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            this.condi = 'hp>70%'
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')
        elif c == 'hp100':
            this.condi = 'hp=100%'
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')
        elif c == 'hit15':
            this.condi = 'hit>=15'
            this.on = 0
            this.passive = this.host.Passive('%s_cc'%name, 0, 'cc')
            Event('hit')(this.l_hit)
        else:
            this.passive = this.host.Passive('%s_cc'%name, v, 'cc')


    def l_hit(this, e):
        if this.on :
            if e.hit < 15 :
                this.on = 0
                this.passive.set(0)
        else:
            if e.hit >= 15 :
                this.on = 1
                this.passive.set(this.v)


    def __call__(this):
        this.passive()


class cd(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'hp70':
            condi = 'hp>70%'
        elif c == 'hp100':
            condi = 'hp=100%'
        this.passive = this.host.Passive('%s_cd'%name, v, 'cd')


    def __call__(this):
        this.passive()


class sp(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        if c == 'fs':
            this.passive = this.host.Passive('%s_fsp'%name, v, 'fsp')
        elif c == None:
            this.passive = this.host.Passive('%s_sp'%name, v, 'sp')


    def __call__(this):
        this.passive()


class bt(Ability):
    def __init__(this, name, v):
        this.v = v
        this.passive = this.host.Passive('%s_bt'%name, v, 'buff')


    def __call__(this):
        this.passive()


class bk(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_bk'%name, v, 'killer', 'bk')


    def __call__(this):
        this.passive()


class od(Ability):
    def __init__(this, name, v, c=None):
        this.v = v
        this.passive = this.host.Passive('%s_od'%name, v, 'killer', 'od')


    def __call__(this):
        this.passive()


class prep(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v


    def __call__(this):
        Timer(this.charge)(0)


    def charge(this, t):
        this.host.charge_p('%s prep'%(this.name), this.v)


class k(Ability):
    def __init__(this, name, v, c):
        this.v = v
        this.passive = this.host.Passive('%s_%s_killer'%(name, c), v, 'killer', c)


    def __call__(this):
        this.passive()


class def_c_atk(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        Listener('def')(c_atk)
    
    def c_atk(this, e):
        if e.host != this.host:
            return 
        this.host.Selfbuff('def_chain', this.v)(15)

class def_c_energy(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        Listener('def')(c_energy)
    
    def c_energy(this, e):
        pass

class lo(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        Timer(trigger)(3)

    def trigger(this, t):
        this.host.Selfbuff('lastoffense', this.v)(15)


class sts(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)
        this.host.Selfbuff('striker', this.v)(-1)


class sls(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v

    def __call__(this):
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)
        this.host.Selfbuff('slayer', this.v)(-1)

class dc(Ability):
    def __init__(this, name, v):
        this.name = name
        this.v = v
        idx = 0
        if v == 1:
            buff = [0.04,0.10,0.20]
        elif v == 2:
            buff = [0.05,0.13,0.25]
        elif v == 3:
            buff = [0.06,0.15,0.30]

    def __call__(this):
        Listener('dragon')(d_atk)
    
    def d_atk(this, e):
        if e.host != this.host:
            return 
        if this.idx <= 2:
            this.host.Selfbuff('dragon_claw', this.buff[this.idx])(-1)
            this.idx+=1
