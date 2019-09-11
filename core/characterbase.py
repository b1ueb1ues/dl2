import __init__
from core.ctx import *
from core.buff import *
from core.action import *


class Skill(object):
    def __init__(this, host):
        this.host = host
        this.s_prev = ''
        this.first_x_after_s = 0
        silence = 0



    def __call__(this, *args, **kwargs):
        def __Skill(_Skill):
            _static = this
        return __Skill(*args, **kwargs)


class _Skill(object):
    _static = Static({
        's_prev'          : '<nop>' ,
        'first_x_after_s' : 0       ,
        'silence'         : 0       ,
        })
    charged = 0
    sp = 0
    silence_duration = 1.9
    name = '_Skill'
    def __init__(this, name=None, conf=None, host=None):
        this.charged = 0
        if name:
            this.name = name
        if conf:
            this.conf = conf
            conf.sync_skill = this.sync_sp
            this.ac = S(this.name, this.conf, this.actionhit)
        if host:
            this.host = host

        this._static.silence = 0
        this.silence_end_timer = Timer(this.cb_silence_end)
        this.silence_end_event = Event('silence_end')
        this.init()

    def __call__(this):
        return this.cast()

    def sync_sp(this,c):
        this.sp = c.sp

    def init(this):
        pass

    def charge(this,sp):
        this.charged += sp   
        #if this.charged > this.sp:  # should be 
            #this.charged = this.sp

    def cb_silence_end(this, e):
        if loglevel >= 2:
            log('silence','end')
        this._static.silence = 0
        this.silence_end_event()


    def check(this):
        if this.sp == 0:
            return 0
        elif this._static.silence == 1:
            return 0
        elif this.charged >= this.sp:
            return 1
        else:
            return 0


    def cast(this):
        if not this.check():
            return 0
        else:
            if not this.ac() :
                return 0
            this.charged = 0
            this._static.s_prev = this.name
            # Even if animation is shorter than 1.9, you can't cast next skill before 1.9
            this.silence_end_timer.on(this.silence_duration)
            this._static.silence = 1
            if loglevel >= 2:
                log('silence','start')
            return 1


    def before(this):
        fn = this.name+'_before'
        if fn in dir(this.host):
            return this.host.__getattribute__(fn)(0)
    

    def proc(this):
        fn = this.name+'_proc'
        if fn in dir(this.host):
            return this.host.__getattribute__(fn)(0)


    def actionhit(this, e):
        host = this.host

        tmp = this.before()
        if tmp!= None:
            dmg_coef = tmp
        else:
            dmg_coef = this.conf.dmg

        if dmg_coef :
            host.dmg_make(this.name, dmg_coef)

        if 'buff' in this.conf:
            buffarg = this.conf.buff
            wide = buffarg[0]
            buffarg = buffarg[1:]
            if wide == 'team':
                Teambuff(e.name, *buffarg).on()
            elif wide == 'self':
                Selfbuff(e.name, *buffarg).on()
            elif wide == 'debuff':
                Debuff(e.name, *buffarg).on()
            else:
                Buff(e.name, *buffarg).on()

        this.proc()

class Character(object):
    def default(this, conf):
        conf.name = 'characterbase'
        conf.star = 4
        conf.ele = 'flame'
        conf.wt = 'sword'
        conf.atk = 500
        conf.a1 = ('hp70', 'atk', 10)
        conf.a2 = ('resist', 'stun', 100)
        conf.a3 = ('hit15', 'cc', 10)
        conf.slot.w = 'c534'
        conf.slot.d = 'Cerb'
        conf.slot.a1 = 'RR'
        conf.slot.a2 = 'FP'
        conf.ex = ['blade', 'wand']

    def __init__(this, conf=None):
        this.atk = 2000
        this.killer = {}

        tmp = Conf()             
        this.default(tmp)    # conf prior
        this.config(tmp)     # default < class < param
        if conf:
            tmp(conf)
            conf(tmp)
            tmp = conf
        this.conf = tmp
        this.conf.sync_characterbase = this.sync


    # after settle down all config
    def init(this):
        this.classinit()


    def classinit(this):
        this.Dp = Dmg_param(this.conf)

        this.Passive = Passive(this.Dp)
        this.Buff = Buff(this.Dp)

        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)

        this.Action = Action(this)


    def sync(this, c, cc):
        this.name = c.name
        this.base_atk = c.atk
        if c.wt in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8


    def tar(this, target):
        this.target = target
        this.Dmg = Dmg_calc(this, target)
