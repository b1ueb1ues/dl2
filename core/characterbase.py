import __init__
from core.ctx import *
from core.buff import *
from core.action import *
from core.skill import *
from core import floatsingle
from ability import *
from amulet import *
from weapon import *
from dragon import *



class Conf_chara(Config):
    def default(this):
        return {
            'name'        : 'characterbase'
            ,'star'       : 5
            ,'ele'        : 'flame'
            ,'wt'         : 'blade'
            ,'atk'        : 520
            ,'a1'         : None
            ,'a3'         : None

            ,'ex'         : ['blade', 'wand']
            #,'ex'        : ['blade']
            ,'rotation'   : 0
            ,'acl'        : 0

            ,'param_type' : ['atk', 'dmg', 'cc', 'cd',
                             'sp', 'spd', 'buff', 
                             'killer', # 'def', 'ks'
                             'x','fs','s']
            ,'s1' : None
            ,'s2' : None
            ,'s3' : None

            ,'acl.cancel' : """
                `s1
                `s2
                `s3
            """
            ,'acl.other' : None
            ,'acl.rotation' : None
            #,'acl.rotation' : """
            #    c1fsend
            #"""
            
            }
    

    def sync(this, c):
        this.name     = c['name']
        this.base_atk = c['atk']
        this.wt       = c['wt']
        this.ele      = c['ele']
        this.star     = c['star']
        this.ex       = c['ex']
        if c['wt'] in ['sword', 'blade', 'dagger', 'axe', 'lance']:
            this.base_def = 10
        else:
            this.base_def = 8
        if c['wt'] in ['axe'] :
            this.base_crit = 0.04
        else:
            this.base_crit = 0.02


default_acl_cancel = """\
    #s1 = this.s1
    #s2 = this.s2
    #s3 = this.s3
    #fsc = 0
    #x = 0
    #fs = 0
    #if e.type == 'x':
    #    if e.hit == e.last:
    #        x = e.idx
    #    else:
    #        x = e.idx*10+e.hit
    #elif e.type == 'fs':
    #    if e.hit == e.last:
    #        fsc = 1
    #    fs = e.hit
"""
default_acl_other = """\
    #s1 = this.s1
    #s2 = this.s2
    #s3 = this.s3
    #doing = this.Action.doing.name
"""

class Character(object):
    #conf = {}       # rewrite by child
    # or
    # def conf(this): # rewrite by child
    #     return {}
    def dconf(this, conf): # rewrite by child
        return 1
    def init(this): # rewrite by child
        pass
    s1_proc = None # rewrite a function by child
    s2_proc = None # rewrite a function by child

    def __init__(this, rootconf=None):
        if type(this.conf) == dict:
            Conf_chara(this, this.conf)()
        else:
            Conf_chara(this, this.conf())()
        if rootconf:
            rootconf[this.name] = this.conf
            this.conf['ex'] = rootconf['ex']
            this.ex = rootconf['ex']
        this.hitcount = 0
        this.t_hitreset = Timer(this.hitreset)
        this.e_hit = Event('hit')
        this.e_acl = Event('acl')
        this.e_acl.type = 'charge'
        this.e_acl.host = this

        this.logsp = Logger('sp')
        this.loghit = Logger('hit')
        this.logx = Logger('x')

        this.child_init = this.init
        this.init = this.character_init



    # after settle down all config
    def character_init(this):
        this.classinit()

        if this.s1_proc:
            this.conf['s1']['proc'] = [this.s1_proc]
        if this.s2_proc:
            this.conf['s2']['proc'] = [this.s2_proc]
        #if 'proc' not in this.conf['s1']:
        #    this.conf['s1']['proc'] = this.s1_proc
        #if 'proc' not in this.conf['s2']:
        #    this.conf['s2']['proc'] = this.s2_proc
        this.s1 = this.Skill('s1', this, this.conf['s1'])
        this.conf['s1'] = this.s1.conf
        this.s2 = this.Skill('s2', this, this.conf['s2'])
        this.conf['s2'] = this.s2.conf
        this.s3 = this.Skill('s3', this, this.conf['s3'])
        this.conf['s3'] = this.s3.conf

        import config.weapon
        wtconf = Conf()(config.weapon.wtconf[this.conf['wt']]).get
        this.x1 = this.Combo('x1', this, wtconf['x1'])
        this.x2 = this.Combo('x2', this, wtconf['x2'])
        this.x3 = this.Combo('x3', this, wtconf['x3'])
        this.x4 = this.Combo('x4', this, wtconf['x4'])
        this.x5 = this.Combo('x5', this, wtconf['x5'])
        this.conf['x1'] = this.x1.conf
        this.conf['x2'] = this.x2.conf
        this.conf['x3'] = this.x3.conf
        this.conf['x4'] = this.x4.conf
        this.conf['x5'] = this.x5.conf

        this.a_x = [this.x1, this.x2, this.x3, this.x4, this.x5, this.x1]
        this.a_s = [this.s1, this.s2, this.s3]

        this.fs = Fs_group(this, wtconf)
        if 'fsf' in wtconf:
            this.fsf = this.Fs('fsf', this, wtconf['fsf'])
            wtconf['fsf'] = this.fsf.conf

        conf_update = {}
        this.dconf(conf_update)
        Conf(this.conf)(conf_update)

        this.setup()
        this.child_init()

        import core.acl
        global default_acl_prepare
        conf_acl = this.conf['acl']
        if type(conf_acl) == str:
            conf_acl = {'cancel':conf_acl, 'rotation':None, 'other':None}
            this.conf['acl'] = conf_acl

        if conf_acl['rotation']:
            Listener('idle')(this.l_rotation)
            Listener('cancel')(this.l_rotation)
            Listener('acl')(this.l_rotation)
        else:
            Listener('idle')(this.l_idle)
            core.acl.acl_module_init(this)
            if type(conf_acl['cancel']) == str:
                acl = default_acl_cancel + conf_acl['cancel']
                acl_str = core.acl.acl_module_add(acl, 'cancel')
                conf_acl['cancel'] = {'str':acl_str}
            if type(conf_acl['other']) == str:
                acl = default_acl_other + conf_acl['other']
                acl_str = core.acl.acl_module_add(acl, 'other')
                conf_acl['other'] = {'str':acl_str}
            core.acl.acl_module_end()
            import importlib
            _acl = importlib.import_module('core._acl.' \
                                            +this.__class__.__name__)
            if conf_acl['cancel']:
                Listener('cancel')(this.think_cancel)
                this.acl_cancel = _acl.cancel
            if conf_acl['other']:
                Listener('acl')(this.think_other)
                this.acl_other = _acl.other

        this.e_idle = Event('idle')
        this.e_idle.host = this
        this.e_idle()



    def setup(this):
        this.Passive('base_crit_chance', this.base_crit, 'cc')()
        this.Passive('base_crit_damage', 0.7, 'cd')()

        if this.conf['a1']:
            this.a1 = this.Ability('chara_a1', *this.conf['a1'])()
        if this.conf['a3']:
            this.a3 = this.Ability('chara_a3', *this.conf['a3'])()

        this.d = this.Dragon(this.conf['slot']['d'])
        this.w = this.Weapon(this.conf['wt'], this.conf['slot']['w'] )
        this.a = this.Amulet(this.conf['slot']['a1'], this.conf['slot']['a2'])

        this.d.init()
        this.w.init()
        this.a.init()

        ex = {}
        for i in this.ex:
            ex[i] = 1
        ex[this.wt] = 1

        for i in ex:
            if i == 'blade':
                this.Passive('ex_blade',  0.10, 'atk', 'ex')()
            elif i == 'wand':
                this.Passive('ex_wand',   0.15, 's',  'ex')()
            elif i == 'dagger':
                this.Passive('ex_dagger', 0.10, 'cc',  'p')()
            elif i == 'bow':
                this.Passive('ex_bow',    0.15, 'sp',  'p')()

        from config import forte
        this.atk = this.base_atk * forte.c(this.ele, this.wt)
        this.atk += this.d.atk * forte.d(this.ele)
        this.atk += this.w.atk + this.a.atk
        this.atk = int(this.atk)
        log_('info','%s, base_atk'%(this.name),this.atk)
        

    def classinit(this):
        this.Dp = Dmg_param(this)
        this.mod = this.Dp.get

        this.Passive = Passive(this.Dp)
        this.Buff = Buff(this.Dp)

        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)

        this.Action = Action(this, this.Dp)
        this.Skill = Skill(this)
        this.Combo = Combo(this)
        this.Fs = Fs(this)

        this.Ability = Ability(this)
        this.Dragon = Dragon(this)
        this.Weapon = Weapon(this)
        this.Amulet = Amulet(this)


    def tar(this, target):
        this.target = target
        this.Dmg = Dmg_calc(this, target)


    def charge(this, name, sp):
        sp = int(sp) * floatsingle.tofloat(this.mod('sp'))
        sp = floatsingle.tofloat(sp)
        sp = floatsingle.ceiling(sp)
        this.s1.charge(sp)
        this.s2.charge(sp)
        this.s3.charge(sp)
        if this.logsp :
            this.logsp('%s, %s'%(this.name, name), sp,
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )
        this.e_acl()


    def charge_p(this, name, sp):
        if type(sp) == str and sp[-1] == '%':
            charge = int(sp[:-1]) / 100
        elif type(sp) == int :
            charge = sp
        elif type(sp) == float :
            charge = sp
        else:
            charge = 0

        this.s1.charge( floatsingle.ceiling(this.conf['s1']['sp'] * charge) )
        this.s2.charge( floatsingle.ceiling(this.conf['s2']['sp'] * charge) )
        this.s3.charge( floatsingle.ceiling(this.conf['s3']['sp'] * charge) )
        if this.logsp:
            this.logsp('%s, %s'%(this.name, name), '%d%%'%(charge*100),
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )
        #this.think_pin('prep')


    def x(this):
        doing = this.Action.doing.conf
        if doing['type'] == 'x' :
            this.a_x[doing['idx']]()
        elif doing['type'] == 'fs' :
            this.a_x[0]()
        else:
            if this.logx:
                this.logx('%s, tap'%this.name, 'plain start')
            Timer(this.start_x)(0.15)


    def start_x(this, t):
        this.a_x[0]()


    def hit(this, count):
        if this.loghit:
            this.loghit('add', '%d+%d'%(this.hitcount, count) )
        if count :
            this.hitcount += count
            this.t_hitreset(2)
            this.e_hit.hit = this.hitcount
            this.e_hit()


    def hitreset(this, t):
        this.hitcount = 0
        if this.loghit:
            this.loghit('reset', 0)
        this.e_hit.hit = 0
        this.e_hit()


    def l_idle(this, e):
        if e.host != this:
            return
        this.x()


    def l_rotation(this, e):
        pass


    def think_other(this, e):
        if e.host != this:
            return
        this.acl_other(this, e)

    def think_cancel(this, e):
        if e.host != this:
            return
        this.acl_cancel(this, e)



if __name__ == '__main__':
    root = {'ex':'bow'}
    c = Character(root)
    c.init()
    print(c.name)
    print(root)
    
