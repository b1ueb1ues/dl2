import __init__
from core.ctx import *
from core.buff import *
from core.action import *


class Skill(object):
    def __init__(this, host):
        this.host = host
        this.s_prev = ''
        this.first_x_after_s = 0
        this.silence = 0
        this.silence_duration = 2.1 # 0.1 button lag, 2s ui hide
        this.t_silence_end = Timer(this.silence_end)
        this.e_silence_end = Event('silence_end')
        this.log = Logger('s')



    def __call__(this, *args, **kwargs):
        class __Skill(_Skill):
            _static = this
        return __Skill(*args, **kwargs)


    def silence_end(this, t):
        if this.log:
            this.log(this.host.name+', silence','end')
        this.silence = 0
        this.e_silence_end()


    def silence_start(this):
        this.silence = 1
        this.t_silence_end(this.silence_duration)


class Sp(object):
    def __init__(this, sp_max):
        this.cur = 0
        this.max = sp_max


class Conf_skl(Config):
    def default(this, conf):
        conf.sp       = 0
        conf.startup  = 0.1 # ui lag
        conf.recovery = 2
        conf.on_start = None
        conf.on_end   = None
        conf.proc     = None
        conf.hit      = []
        conf.hitattr  = []


    def sync(this, c):
        this.sp.max = c.sp
        this.hit    = c.hit
        this.proc   = c.proc


class _Skill(object):
    def __init__(this, name, host, conf=None):
        this.name = name
        this.host = host
        this.sp = Sp(0)
        this.firsthit = 1

        this.conf = Conf_skl(this, conf)

        this.ac = host.Action(this.name, this.conf)

        this.log = Logger('s')
        this.src = this.host.name+', '


    def __call__(this):
        return this.cast()


    def init(this):
        this.dmg = {}
        for i in this.conf.hitattr:
            attr = this.conf.hitattr[i]
            attr.name = this.name
            this.dmg[i] = this.host.Dmg(attr)


    def charge(this, sp):
        this.sp.cur += sp   
        #if this.charged > this.sp:  # should be 
            #this.charged = this.sp


    def check(this):
        if this.sp.max == 0:
            if this.log:
                this.log(this.src+this.name, 'failed','no skill')
            return 0
        elif this._static.silence == 1:
            if this.log:
                this.log(this.src+this.name, 'failed','silence')
            return 0
        elif this.sp.cur < this.sp.max:
            if this.log:
                this.log(this.src+this.name, 'failed','no sp')
            return 0
        else :
            return 1


    def cast(this):
        if this.log:
            this.log(this.src+this.name, 'tap')
        if not this.check():
            return 0
        else:
            if this.log:
                this.log(this.src+this.name, 'cast')
            if this.ac():
                this.active()
                this.firsthit = 1
                this.sp.cur = 0
                this._static.s_prev = this.name
                # Even if animation is shorter than 2s
                # you can't cast next skill before 2s, after which ui shows
                this._static.silence_start()
                return 1
            else:
                return 0


    def before(this):
        pass
    

    def proc(this):
        pass


    def buff(this, t):
        if t.wide == 'team':
            this.host.Teambuff(this.name, t.value, *t.buffarg)(t.time)
        elif t.wide == 'self':
            this.host.Selfbuff(this.name, t.value, *t.buffarg)(t.time)
        elif t.wide == 'debuff':
            print('cant proc debuff at skill start')
            errrrrrrrrrr()
     #       this.host.target.Debuff(this.name, t.value, *t.buffarg)(t.time)
        elif t.wide == 'zone':
            this.host.Zonebuff(this.name, t.value, *t.buffarg)(t.time)
        else:
            this.host.Buff(this.name, t.value, *t.buffarg)(t.time)


    def dmg_make(this, t):
        t.dmg()

        if this.firsthit:
            this.firsthit = 0
            if 'debuff' in this.conf:
                buffarg = this.conf.debuff
                t.wide = buffarg[0]
                t.value = buffarg[1]
                t.time = buffarg[2]
                t.buffarg = buffarg[3:]
                this.host.target.Debuff(this.name, t.value, *t.buffarg)(t.time)
            if this.proc:
                this.proc()


    def active(this):
        this.before()

        for i in this.hit:
            t = Timer(this.dmg_make)(i[0])
            t.dmg = this.dmg[i[1]]

        if 'buff' in this.conf:
            buffarg = this.conf.buff
            t = Timer(this.buff)(0.15)
            t.wide = buffarg[0]
            t.value = buffarg[1]
            t.time = buffarg[2]
            t.buffarg = buffarg[3:]

        #this.proc()


class Combo(object):
    def __init__(this, host):
        this.host = host
        this.x_prev = ''
        this.log = Logger('x')



    def __call__(this, *args, **kwargs):
        class __Combo(_Combo):
            _static = this
        return __Combo(*args, **kwargs)



class Conf_cmb(Config):
    def default(this, conf):
        conf.sp       = 0
        conf.startup  = 0 # only for c1
        conf.recovery = 2
        conf.on_start = None
        conf.on_end   = None
        conf.proc     = None
        conf.hit      = {}
        conf.hitattr  = []


    def sync(this, c):
        this.sp      = c.sp
        this.hit     = c.hit
        this.hitattr = c.hitattr
        this.proc    = c.proc



class _Combo(object):
    def __init__(this, name, host, conf=None):
        this.name = name
        this.host = host
        this.sp = 0
        this.firsthit = 1
        this.hit_count = 1
        this.hit_next = 0

        this.conf = Conf_cmb(this, conf)

        this.ac = host.Action(this.name, this.conf)

        this.log = Logger('x')
        this.src = this.host.name+', '


    def __call__(this):
        return this.cast()


    def init(this):
        this.hit_count = len(this.hit)
        this.dmg = {}
        for i in this.conf.hitattr:
            attr = this.conf.hitattr[i]
            attr.name = this.name
            this.dmg[i] = this.host.Dmg(attr)


    def cast(this):
        if this.log:
            this.log(this.src+this.name, 'tap')
        else:
            if this.ac():
                this.active()
                this.firsthit = 1
                this._static.x_prev = this.name
                return 1
            else:
                return 0


    def proc(this):
        pass


    def dmg_make(this, t):
        if this.ac.status != 1:
            return

        t.dmg()

        if this.firsthit:
            this.firsthit = 0
            this.host.charge('x', this.sp)
            if this.proc:
                this.proc()

        if this.hit_next < this.hit_count :
            hitlabel = this.hit[this.hit_next]
            t = Timer(this.dmg)(this.hit_next)
            t.dmg = this.dmg[hitlabel]
            this.hit_next += 1


    def active(this):
        print(this.hit_next, this.hit_count)
        print(this.hit)
        print(this.dmg)

        if this.hit_next < this.hit_count :
            timing   = this.hit[this.hit_next][0]
            hitlabel = this.hit[this.hit_next][1]
            t = Timer(this.dmg_make)(timing)
            t.dmg = this.dmg[hitlabel]
            this.hit_next += 1
