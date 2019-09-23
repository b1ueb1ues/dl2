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
        this.silence_duration = 2 # 2s ui hide
        this.t_silence_end = Timer(this.silence_end)
        this.e_silence_end = Event('silence_end')
        this.log = Logger('s')


    def __call__(this, *args, **kwargs):
        return _Skill(this, *args, **kwargs)


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
    default = {
         'type'     : 's'
        ,'sp'       : -1
        ,'startup'  : 0.1 # ui lag  # only for action
        ,'recovery' : 2             # both for action
        ,'on_start' : None 
        ,'on_end'   : None          # only for action
        ,'proc'     : None
        ,'hit'      : []
        ,'attr'     : {}
        }


    def sync(this, c):
        this.sp['max'] = c['sp']
        this.proc      = c['proc']
        this.startup   = c['startup']
        this.on_start  = c['on_start']

        dirty = 0
        if this.attr != c['attr']:
            this.attr = c['attr']
            dirty = 1
        if this.hit != c['hit']:
            this.hit = c['hit']
            dirty = 1
        if dirty:
            this.dmg = {}
            this.hit_count = len(this.hit)
            for i in this.attr:
                label = this.attr[i]
                if i[0] == '_':
                    label['name'] = this.name + i
                else:
                    label['name'] = this.name
                label['proc'] = this.collid
                label['type'] = 's'
                this.dmg[i] = this.host.Dmg(label)
        


class _Skill(object):
    def __init__(this, static, name, host, conf=None):
        this._static = static
        this.name = name
        this.host = host
        this.sp = {'max':-1, 'cur':0}
        this.firsthit = 1
        this.hit_prev = -1
        this.hit_next = 0
        this.hit_count = 0

        this.hit = None
        this.attr = None

        this.speed_cache = host.Dp.cache
        this.speed_get = host.Dp.get_

        this.log = Logger('s')
        this.src = host.name+', '

        Conf_skl(this, conf)()
        this.ac = host.Action(this.name, this.conf)
        this.conf = this.ac.conf

    def __call__(this):
        return this.tap()

    def charge(this, sp):
        if this.sp['max'] > 0:
            this.sp['cur'] += sp   
        #if this.charged > this.sp:  # should be 
            #this.charged = this.sp


    def check(this):
        if this.sp['max'] <= 0:
            if this.log:
                this.log(this.src+this.name, 'failed','no skill')
            return 0
        elif this._static.silence == 1:
            if this.log:
                this.log(this.src+this.name, 'failed','silence')
            return 0
        elif this.sp['cur'] < this.sp['max']:
            if this.log:
                this.log(this.src+this.name, 'failed','no sp')
            return 0
        else :
            return 1


    def tap(this):
        if this.log:
            this.log(this.src+this.name, 'tap')
        if not this.check():
            return 0
        else:
            if this.log:
                this.log(this.src+this.name, 'cast')
            if this.ac():
                #this.active() {
                this.firsthit = 1
                this.hit_prev = -1
                this.hit_next = 0
                Timer(this._active)(this.startup)
                #this.active() }
                return 1
            else:
                return 0


    def buff(this, t):
        if type(this.conf['buff']) == tuple:
            buffarg = this.conf['buff']
            this.onebuff(buffarg)
        elif type(this.conf['buff']) == list:
            for i in this.conf['buff']:
                this.onebuff(i)


    def onebuff(this, buffarg):
        wide = buffarg[0]
        value = buffarg[1]
        time = buffarg[2]
        buffarg = buffarg[3:]
        if wide == 'team':
            this.host.Teambuff(this.name, value, *buffarg)(time)
        elif wide == 'self':
            this.host.Selfbuff(this.name, value, *buffarg)(time)
        elif wide == 'debuff':
            print('cant proc debuff at skill start')
            raise
     #       this.host.target.Debuff(this.name, value, *buffarg)(time)
        elif wide == 'zone':
            this.host.Zonebuff(this.name, value, *buffarg)(time)
        else:
            this.host.Buff(this.name, value, *buffarg)(time)


    def _do(this, t):
        if this.ac.status != 1:
            return

        hitlabel = this.hit[this.hit_next][1]
        this.dmg[hitlabel]()

        this.hit_prev = this.hit_next
        this.hit_next += 1

        if this.hit_next < this.hit_count :
            timing = this.hit[this.hit_next][0] - this.hit[this.hit_prev][0]
            #timing /= this.speed() {
            if this.speed_cache['spd']>=0 :
                timing /= this.speed_cache['spd']
            else:
                timing /= this.speed_get('spd')
            #timing /= this.speed() }

            Timer(this._do)(timing)


    def collid(this):
        if this.firsthit:
            this.firsthit = 0
            if this.proc:
                this.proc()
            if 'debuff' in this.conf:
                buffarg = this.conf.debuff
                wide = buffarg[0]
                value = buffarg[1]
                time = buffarg[2]
                buffarg = buffarg[3:]
                this.host.target.Debuff(this.name, value, *buffarg)(time)

# inlined
#    def active(this):
#        this.firsthit = 1
#        this.hit_prev = -1
#        this.hit_next = 0
#        Timer(this._active)(this.startup)


    def _active(this, t):
        static = this._static
        if this.ac.status != 1:
            return

        if this.log:
            this.log('%s, %s'%(this.host.name, this.name),'cutin')

        this.sp['cur'] = 0
        static.s_prev = this.name
        # Even if animation is shorter than 2s
        # you can't cast next skill before 2s, after which ui shows
        #this._static.silence_start() {
        static.silence = 1
        static.t_silence_end(static.silence_duration)
        #this._static.silence_start() }


        if this.on_start :
            this.on_start()

        if this.hit_next < this.hit_count :
            #timing = this.hit[this.hit_next][0] / this.speed() {
            if this.speed_cache['spd'] >= 0 :
                timing = this.hit[this.hit_next][0] / this.speed_cache['spd']
            else:
                timing = this.hit[this.hit_next][0] / this.speed_get('spd')
            # } timing = this.hit[this.hit_next][0] / this.speed()
            Timer(this._do)(timing)

        if 'buff' in this.conf:
            # timing = 0.15/this.speed() {
            if this.speed_cache['spd'] >= 0 :
                timing = 0.15/this.speed_cache['spd']
            else:
                timing = 0.15/this.speed_get('spd')
            # } timing = 0.15/this.speed()
            Timer(this.buff)(timing)


class Combo(object):
    def __init__(this, host):
        this.host = host
        this.x_prev = ''


    def __call__(this, *args, **kwargs):
        r = _Combo(*args, **kwargs)
        r._static = this
        return r


class Conf_cmb(Config):
    default = {
         'type'     : 'x'
        ,'idx'      : 1 # 1~5
        ,'sp'       : 0
        ,'startup'  : 0
        ,'recovery' : 2
       #,'on_start' : None
       #,'on_end'   : None
        ,'proc'     : None
        ,'hit'      : []
        ,'attr'     : {}
        ,'cancel_by': ['s','fs','dodge']
        }


    def sync(this, c):
        this.type    = c['type']
        this.idx     = c['idx']
        this.sp      = c['sp']
        this.attr    = c['attr']
        this.proc    = c['proc']
        
        dirty = 0
        if this.hit != c['hit']:
            this.hit = c['hit']
            dirty = 1
        if this.attr != c['attr']:
            this.attr = c['attr']
            dirty = 1
        if dirty:
            this.dmg = {}
            for i in this.attr:
                this.hit_count = len(this.hit)
                label = this.attr[i]
                label['name'] = this.name
                label['proc'] = this.collid
                label['type'] = 'x'
                this.dmg[i] = this.host.Dmg(label)
        this.e_x.type = this.type
        this.e_x.idx = this.idx
        this.e_x.last = this.hit_count


class _Combo(object):
    def __init__(this, name, host, conf=None):
        this.name = name
        this.host = host
        this.sp = 0
        this.firsthit = 1
        this.hit_count = 0
        this.hit_prev= -1
        this.hit_next = 0
        this.e_x = Event('cancel')
        this.e_x.name = this.name

        this.hit = None
        this.attr = None
        Conf_cmb(this, conf)()

        this.speed_cache = host.Dp.cache
        this.speed_get = host.Dp.get_
        this.ac = host.Action(this.name, this.conf)
        this.conf = this.ac.conf

        this.log = Logger('x')
        this.src = this.host.name+', '
        this.charge = host.charge



    def tap(this):
        if this.log:
            this.log(this.src+this.name, 'tap')

        if this.ac():
            #this.active {
            if this.hit_count :
                this.firsthit = 1
                this.hit_prev= -1
                this.hit_next = 0
                # timing = this.hit[this.hit_next][0] / this.speed() {
                if this.speed_cache['spd']>=0 :
                    timing = this.hit[0][0]/this.speed_cache['spd']
                else:
                    timing = this.hit[0][0]/this.speed_get['spd']
                # } timing = this.hit[this.hit_next][0] / this.speed()
                Timer(this._do)(timing)
            #this.active }
            this._static.x_prev = this.name
            return 1
        else:
            return 0

    __call__ = tap


    def _do(this, t):
        if this.ac.status != 1:
            return

        hitlabel = this.hit[this.hit_next][1]
        this.dmg[hitlabel]()

        this.hit_prev = this.hit_next
        this.hit_next += 1

        if this.hit_next < this.hit_count :
            timing = this.hit[this.hit_next][0] - this.hit[this.hit_prev][0]
            # timing /= this.speed() {
            if this.speed_cache['spd']>=0 :
                timing /= this.speed_cache['spd']
            else:
                timing /= this.speed_get('spd')
            # timing /= this.speed() }

            Timer(this._do)(timing)

        this.e_x.hit = this.hit_next
        this.e_x()


    def collid(this):
        if this.firsthit:
            this.firsthit = 0
            this.charge('x', this.sp)
            if this.proc:
                this.proc()

#  inlined
#    def active(this):
#        if this.hit_count :
#            this.firsthit = 1
#            this.hit_prev= -1
#            this.hit_next = 0
#            timing = this.hit[this.hit_next][0] / this.speed()
#            Timer(this._do)(timing)



class Fs(object):
    def __init__(this, host):
        this.host = host

    def __call__(this, *args, **kwargs):
        return _Fs(this, *args, **kwargs)


class Conf_fs(Config):
    default = {
         'type'      : 'fs'
        ,'sp'        : 0
        ,'startup'   : 0 # charge time, which didn't affect by speed
        ,'recovery'  : 2
       #,'on_start' : None
       #,'on_end'   : None
        ,'proc'      : None
        ,'hit'       : []
        ,'attr'      : {}
        ,'cancel_by' : ['s','dodge']
        }

    def sync(this, c):
        this.type    = c['type']
        this.sp      = c['sp']
        this.attr    = c['attr']
        this.proc    = c['proc']
        this.startup = c['startup']
        
        if this.hit != c['hit']:
            this.hit = c['hit']
            dirty = 1
        if this.attr != c['attr']:
            this.attr = c['attr']
            dirty = 1
        if dirty:
            this.hit_count = len(this.hit)
            this.dmg = {}
            for i in this.attr:
                label = this.attr[i]
                label['name'] = this.name
                label['proc'] = this.collid
                label['type'] = 'fs'
                this.dmg[i] = this.host.Dmg(label)
        this.e_fs.type = this.type
        this.e_fs.name = this.name
        this.e_fs.idx = 0
        this.e_fs.last = this.hit_count


class _Fs(object):
    def __init__(this, static, name, host, conf=None):
        this._static = static
        this.name = name
        this.host = host
        this.sp = 0
        this.firsthit = 1
        this.hit_count = 1
        this.hit_next = 0
        this.e_fs = Event('cancel')

        this.hit = None
        this.attr = None
        Conf_fs(this, conf)()

        this.speed_cache = host.Dp.cache
        this.speed_get = host.Dp.get_
        this.ac = host.Action(this.name, this.conf)
        this.conf = this.ac.conf

        this.log = Logger('fs')
        this.src = host.name+', '
        this.charge = host.charge
        this.t_startup = Timer(this._active)


    def __call__(this):
        return this.hold()


    def hold(this):
        if this.log:
            this.log(this.src+this.name, 'hold')
        if this.ac():
            this.active()
            return 1
        else:
            return 0


    def _do(this, t):
        if this.ac.status != 1:
            return

        hitlabel = this.hit[this.hit_next][1]
        this.dmg[hitlabel]()

        this.hit_prev = this.hit_next
        this.hit_next += 1

        if this.hit_next < this.hit_count :
            timing = this.hit[this.hit_next][0] - this.hit[this.hit_prev][0]
            # timing /= this.speed() {
            if this.speed_cache['spd']>=0 :
                timing /= this.speed_cache['spd']
            else:
                timing /= this.speed_get('spd')
            # } timing /= this.speed()

            Timer(this._do)(timing)

        this.e_fs.hit = this.hit_next
        this.e_fs()


    def collid(this):
        if this.firsthit:
            this.firsthit = 0
            this.charge('fs', this.sp)
            if this.proc:
                this.proc()


    def active(this):
        if this.startup:
            this.t_startup(this.startup)
        else:
            this._active(0)


    def _active(this, t):
        if this.ac.status != 1:
            return

        if this.log:
            this.log('%s, %s'%(this.host.name, this.name),'release')

        if this.hit_count :
            this.firsthit = 1
            this.hit_next = 0
            this.hit_prev = -1
            # timing = this.hit[this.hit_next][0] / this.speed() {
            if this.speed_cache['spd']>=0 :
                timing = this.hit[this.hit_next][0] / this.speed_cache['spd']
            else:
                timing = this.hit[this.hit_next][0] / this.speed_get('spd')
            # } timing = this.hit[this.hit_next][0] / this.speed()
            Timer(this._do)(timing)


class Dodge(object):
    def __init__(this, host):
        this.host = host
        this.x_prev = ''


    def __call__(this, *args, **kwargs):
        r = _Dodge(*args, **kwargs)
        r._static = this
        return r


class Conf_dodge(Config):
    default = {
         'type'      : 'dodge'
        ,'startup'   : 0
        ,'recovery'  : 0.7
       #,'on_start'  : None
       #,'on_end'    : None
        ,'cancel_by' : ['s']
        }


    def sync(this, c):
        this.type    = c['type']
        this.startup = c['startup']
        
        this.e_x.type = this.type
        this.e_x.idx = 0
        this.e_x.last = 0


class _Dodge(object):
    def __init__(this, name, host, conf=None):
        this.name = name
        this.host = host
        this.e_x = Event('cancel')
        this.e_x.name = this.name

        Conf_dodge(this, conf)()

        this.ac = host.Action(this.name, this.conf)
        this.conf = this.ac.conf

        this.log = Logger('dodge')
        this.src = this.host.name+', '


    def __call__(this):
        return this.tap()


    def tap(this):
        if this.log:
            this.log(this.src+this.name, 'tap')

        if this.ac():
            if this.log:
                this.log('start')
            return 1
        else:
            if this.log:
                this.log('failed')
            return 0



class Fs_group(object):
    def __init__(this, host, wtconf):
        this.host = host
        this.a_fs = [0,1,2,3,4,5,6]
        this.a_fs[0] = host.Fs('fs', host, wtconf['fs'])
        wtconf['fs'] = this.a_fs[0].conf
        c_ofs = Conf(wtconf['fs'])
        for i in range(1, 6):
            fsname = 'x%dfs'%i
            if fsname in wtconf:
                c_tmp = Conf()
                c_tmp .update(c_ofs)
                c_fsn = Conf(wtconf[fsname])
                c_tmp.update(c_fsn)
                wtconf[fsname] = c_tmp.get
                this.a_fs[i] = host.Fs('fs', host, wtconf[fsname])
            else:
                this.a_fs[i] = host.Fs('fs', host, wtconf['fs'])
        if 'dfs' in wtconf:
            c_tmp = Conf()
            c_tmp.update(c_ofs)
            c_fsn = Conf(wtconf['dfs'])
            c_tmp.update(c_fsn)
            wtconf[fsname] = c_tmp.get
            this.a_fs[6] = host.Fs('fs', host, wtconf['dfs'])


    def __call__(this):
        doing = this.host.Action.doing.conf
        if doing.type == 'x':
            this.a_fs[doing.idx]()
        elif doing.type == 'dodge':
            this.a_fs[6]()
        else:
            this.a_fs[0]()
