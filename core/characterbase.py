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
from mod.energy import *
from core import eventevent
from core.condition import *



class Conf_chara(Config):
    def default(this):
        return {
            'name'        : None
            ,'star'       : 5
            ,'ele'        : 'flame'
            ,'wt'         : 'blade'
            ,'atk'        : 520
            ,'a1'         : None
            ,'a3'         : None

            ,'ex'         : None
            ,'rotation'   : 0
            ,'acl'        : 0

            ,'param_type' : ['', 'atk', 'dmg', 'cc', 'cd',
                             'sp', 'fsp', 'spd', 'bt', 
                             'killer','energy', # 'def', 'ks'
                             'x','fs','sd']
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
        if c['ex'] :
            this.self_ex = c['ex']
        else:
            this.self_ex = c['wt']
            c['ex'] = c['wt']

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
    #s = this.Skill.s_prev
    #fsc = 0
    #x = 0
    #fs = 0
    #if e.type == 'x':
    #    if e.hit == e.last:
    #        x = e.idx
    #    else:
    #        x = e.idx*10+e.hit
    #        default = 0
    #elif e.type == 'fs':
    #    if e.hit == e.last:
    #        fsc = 1
    #    else:
    #        default = 0
    #    fs = e.hit
"""

default_acl_other = """\
    #s1 = this.s1
    #s2 = this.s2
    #s3 = this.s3
    #doing = this.Action.doing.name
    #s = this.Skill.s_prev
"""

class Character(object):
    # conf = {}       # rewrite by child
    # or
    # def conf(this): # rewrite by child
    #     return {}
    def dconf(this): # rewrite by child
        return {}
    def init(this): # rewrite by child
        pass
    s1_proc = None # rewrite a function by child
    s2_proc = None # rewrite a function by child
    s3_proc = None # rewrite a function by child
    s1_end = None # rewrite a function by child
    s2_end = None # rewrite a function by child
    s3_end = None # rewrite a function by child

    def __init__(this, rootconf=None):
        if type(this.conf) == dict:
            Conf_chara(this, this.conf)()
        else:
            Conf_chara(this, this.conf())()

        if not this.conf['name']:
            this.conf['name'] = this.__class__.__name__
            this.name = this.__class__.__name__

        if rootconf:
            rootconf[this.name] = this.conf
            this.team_ex = rootconf['ex']
            this.ex = this.team_ex
        this.hitcount = 0
        this.t_hitreset = Timer(this.hitreset)

        this.Event = eventevent.Event(this)
        this.Listener = eventevent.Listener(this.Event)
        #this.Event.this = this

        this.e_hit = this.Event('hit')
        this.e_acl = this.Event('acl')
        this.e_acl.type = 'sp'

        this.logsp = Logger('sp')
        this.loghit = Logger('hit')
        this.logx = Logger('x')
        this.logd = Logger('dbg')

        this.child_init = this.init
        this.init = this.character_init

        this.condition = Condition()
        if not rootconf['condi'] :
            this.condition.unset()


    # after settle down all config
    def character_init(this, conf_param=None):
        this.classinit()

        if this.s1_proc:
            this.conf['s1']['proc'] = [this.s1_proc]
        if this.s2_proc:
            this.conf['s2']['proc'] = [this.s2_proc]
        if this.s3_proc:
            this.conf['s3']['proc'] = [this.s3_proc]
        if this.s1_end:
            this.conf['s1']['on_end'] = [this.s1_end]
        if this.s2_end:
            this.conf['s2']['on_end'] = [this.s2_end]
        if this.s3_end:
            this.conf['s3']['on_end'] = [this.s3_end]

        this.s1 = this.Skill('s1', this, this.conf['s1'])
        this.conf['s1'] = this.s1.conf
        this.s2 = this.Skill('s2', this, this.conf['s2'])
        this.conf['s2'] = this.s2.conf
        this.s3 = this.Skill('s3', this, this.conf['s3'])
        this.conf['s3'] = this.s3.conf

        this.Energy = Energy(this)

        import basecombo
        wtconf = Conf()(basecombo.wtconf[this.conf['wt']]).get
        this.wtconf = wtconf
        this.x1 = this.Combo('x1', this, wtconf['x1'])
        this.x2 = this.Combo('x2', this, wtconf['x2'])
        this.x3 = this.Combo('x3', this, wtconf['x3'])
        this.x4 = this.Combo('x4', this, wtconf['x4'])
        this.x5 = this.Combo('x5', this, wtconf['x5'])
        #this.conf['x1'] = this.x1.conf
        #this.conf['x2'] = this.x2.conf
        #this.conf['x3'] = this.x3.conf
        #this.conf['x4'] = this.x4.conf
        #this.conf['x5'] = this.x5.conf
        wtconf['x1'] = this.x1.conf
        wtconf['x2'] = this.x2.conf
        wtconf['x3'] = this.x3.conf
        wtconf['x4'] = this.x4.conf
        wtconf['x5'] = this.x5.conf

        this.a_x = [this.x1, this.x2, this.x3, this.x4, this.x5, this.x1]
        this.a_s = [this.s1, this.s2, this.s3]

        this.fs = Fs_group(this, wtconf)
        this.a_fs = [this.fs]
        if 'fsf' in wtconf:
            this.fsf = this.Fs('fsf', this, wtconf['fsf'])
            wtconf['fsf'] = this.fsf.conf

        this.conf.update(wtconf)

        #print(Conf(this.conf))
        conf_update = this.dconf()
        Conf(this.conf)(conf_update)
        if conf_param:
            Conf(this.conf)( Conf(conf_param) )

        this.setup()
        this.child_init()

        setup = '%s*,%s,%s,str:%s|%s,[%s+%s][%s],[%s],'%(this.star, this.ele, this.wt,
                    this.atk, int(this.Dp.get('atk')*this.atk),
                    this.a.a1.__class__.__name__ ,
                    this.a.a2.__class__.__name__ ,
                    this.conf['slot']['d'],
                    str(this.condition)
                )
        if this.__doc__ :
            setup += this.__doc__
        log_('info',this.name,'setup', setup)

        import core.acl
        global default_acl_prepare
        conf_acl = this.conf['acl']
        if type(conf_acl) == str:
            conf_acl = {'cancel':conf_acl, 'rotation':None, 'other':None}
            this.conf['acl'] = conf_acl

        if conf_acl['rotation']:
            this.Listener('idle')(this.l_rotation)
            this.Listener('cancel')(this.l_rotation)
            this.Listener('acl')(this.l_rotation)
        else:
            this.Listener('idle')(this.l_idle)
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
                this.Listener('cancel')(this.think_cancel)
                this.acl_cancel = _acl.cancel
                #this.Listener('cancel')(this.acl_cancel)
            if conf_acl['other']:
                this.Listener('acl')(this.think_other)
                this.acl_other = _acl.other
                #this.Listener('acl')(this.acl_other)

        this.e_idle = this.Event('idle')
        this.e_idle()
        this.debug()

    def debug(this):
        pass

    @classmethod
    def get_sub(cls):
        subclasses = {}
        for i in cls.__subclasses__():
            subclasses[i.__name__] = i
        return subclasses


    def setup(this):
        this.Passive('base_crit_chance', this.base_crit, 'cc')()
        this.Passive('base_crit_damage', 0.7, 'cd')()

        if this.conf['a1']:
            this.a1 = this.Ability('chara_a1', *this.conf['a1'])()
        if this.conf['a3']:
            this.a3 = this.Ability('chara_a3', *this.conf['a3'])()

        import config.slot_common
        slot_d = config.slot_common.get(this.ele, this.wt)
        if 'slot' in this.conf:
            slot_d.update(this.conf['slot'])
        this.conf['slot'] = slot_d

        this.d = this.Dragon(this.conf['slot']['d'])
        this.w = this.Weapon(this.conf['wt'], this.conf['slot']['w'] )
        if 'a' in this.conf['slot'] :
            amulets = this.conf['slot']['a'].split('+')
            this.conf['slot']['a1'] = amulets[0]
            this.conf['slot']['a2'] = amulets[1]
        this.a = this.Amulet(this.conf['slot']['a1'], this.conf['slot']['a2'])

        this.d.init()
        this.w.init()
        this.a.init()

        ex = {}
        for i in this.team_ex:
            ex[i] = 1
        ex[this.conf['ex']] = 1

        if len(ex) > 4:
            print('ex-skill cannot more than 4')
            raise
        for i in ex:
            if i == 'blade':
                this.Passive('ex_blade',  0.10, 'atk', 'ex')()
            elif i == 'wand':
                this.Passive('ex_wand',   0.15, 's',  'ex')()
            elif i == 'dagger':
                this.Passive('ex_dagger', 0.10, 'cc',  'p')()
            elif i == 'bow':
                this.Passive('ex_bow',    0.15, 'sp',  'p')()
            elif i == None:
                pass
            elif type(i) == str:
                pass
            else:
                this.Passive(*i)()

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
            this.logsp(this.name, name, sp,
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )
        this.e_acl()
        if this.Skill.s_prev:
            this.Skill.s_prev = None

    def charge_fs(this, name, sp):
        sp = int(sp) * floatsingle.tofloat(this.mod('sp')+this.mod('fsp')-1)
        sp = floatsingle.tofloat(sp)
        sp = floatsingle.ceiling(sp)
        this.s1.charge(sp)
        this.s2.charge(sp)
        this.s3.charge(sp)
        if this.logsp :
            this.logsp(this.name, name, sp,
                    '%d/%d, %d/%d, %d/%d'%( \
                    this.s1.sp.cur, this.s1.sp.max,
                    this.s2.sp.cur, this.s2.sp.max,
                    this.s3.sp.cur, this.s3.sp.max)
                    )
        this.e_acl()
        if this.Skill.s_prev:
            this.Skill.s_prev = None


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
            this.logsp(this.name, name, '%d%%'%(charge*100),
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
                this.logx(this.name, 'tap', 'plain start')
            Timer(this.start_x)(0.15)


    def start_x(this, t):
        this.a_x[0]()


    def hit(this, count):
        if this.loghit:
            this.loghit(this.name, 'add', '%d+%d'%(this.hitcount, count) )
        if count :
            this.hitcount += count
            this.t_hitreset(2)
            this.e_hit.hit = this.hitcount
            this.e_hit()


    def hitreset(this, t):
        this.hitcount = 0
        if this.loghit:
            this.loghit(this.name, 'reset', 0)
        this.e_hit.hit = 0
        this.e_hit()


    def l_idle(this, e):
        this.x()


    def l_rotation(this, e):
        pass


    def think_other(this, e):
        this.acl_other(this, e)


    def think_cancel(this, e):
        this.acl_cancel(this, e)



if __name__ == '__main__':
    root = {'ex':'bow'}
    c = Character(root)
    c.init()
    print(c.name)
    print(root)
    
