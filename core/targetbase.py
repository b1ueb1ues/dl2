import __init__
from core.ctx import *
from core.skada import *


class Conf_tar(Config):
    def default(this):
        return {
         'def_'    : 10
        ,'od_def'  : 1
        ,'bk_def'  : 0.6
        ,'bk_time' : 10

        ,'name'    : 'target'
        ,'ele'     : 'on'
        ,'hp'      : 1000000
        ,'od'      : 200000
        ,'bk'      : 200000

        ,'ks'      : []
        ,'param_type':['def','ks','dt']

        ,'resist.poison'    : 0
        ,'resist.burn'      : 0
        ,'resist.paralysis' : 0
        ,'resist.blind'     : 0
        ,'resist.bog'       : 0
        ,'resist.freeze'    : 0
        ,'resist.stun'      : 0
        ,'resist.sleep'     : 0
        }


    def sync(this, c):
        this.name     = c['name']
        this.base_def = c['def_']

        this.base_hp  = c['hp']
        this.base_od  = c['od']
        this.base_bk  = c['bk']

        this.od_def   = c['od_def']
        this.bk_def   = c['bk_def']
        this.bk_time  = c['bk_time']

        this.ks = c['ks']

        this.resist = c['resist']

        if this.base_def <= 0:
            print('base_def:%d <= 0'%this.base_def)
            raise
        if this.base_od > 0:
            this.dt = this.dt_odbk
        else:
            this.od = -1
            this.dt = this.dt_no_od


class Target(object):
    def __init__(this, conf_root=None):
        this.conf_root = conf_root

        this.odbk = 0 # 0: normal, 1: od, -1: bk
        this.od = 0
        this.bk = -1

        Conf_tar(this, this.conf)()

        this.skada = skada.get()
        #Event('dmg')(this.l_dmg)
        #this.e_ks = Event('killer')
        this.logdbg = Logger('debug')
        this.logod = Logger('od')
        this.logbk = Logger('bk')
        this.logdmg = Logger('dmg')
        this.od_count = 0

    @classmethod
    def get_sub(cls):
        subclasses = {}
        for i in cls.__subclasses__():
            subclasses[i.__name__] = i
        return subclasses


    def classinit(this):
        this.Dp = Dmg_param(this)
        this.Buff = Buff(this.Dp)
        this.Buff.listener.off()
        this.Passive = Passive(this.Dp)
        #this.Selfbuff = Selfbuff(this.Buff)
        #this.Teambuff = Teambuff(this.Buff)
        #this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)
        this.mod = {}
        #this.Dot_group = None
        #this.Afflics = None


    # after all config settle down
    def init(this):
        this.classinit()
        this.hp = this.base_hp
        this.def_ = this.base_def
        this.od_ks = this.Dp('od', 'ks', 'od', 1)
        this.bk_ks = this.Dp('bk', 'ks', 'bk', 1)
        for i in this.ks:
            this.Passive('ks_%s'%i, 1, 'ks', i)()


    def recount(this, hostname, dmgname, dmg, odmg):
        if hostname not in this.skada:
            this.skada[hostname] = {
                    'dmg':{},
                    'odmg':{},
                    'otime':0
                    }
        hostdmg = this.skada[hostname]['dmg']
        hostodmg = this.skada[hostname]['odmg']
        if dmgname in hostdmg:
            hostdmg[dmgname] += dmg
        else:
            hostdmg[dmgname] = dmg

        if odmg:
            if dmgname in hostodmg:
                hostodmg[dmgname] += odmg
            else:
                hostodmg[dmgname] = odmg
            for i in this.skada:
                this.skada[i]['otime'] += now() - this.od_start
            this.od_start = now()

        if this.logdmg:
            this.logdmg('%s, %s'%(hostname, dmgname), dmg,
                    'hp: %d-%d'%(this.hp, dmg) )


    def dt(this, dmg):
        print('targetbase dt not init')
        raise


    def dt_no_od(this, dmg):
        this.recount(dmg.hostname, dmg.name, dmg.dmg, 0)
        this.hp -= dmg.dmg
        if this.hp < 0 :
            this.die()


    def dt_odbk(this, dmg): 
        true_dmg = dmg.dmg
        if this.odbk == 0 :
            this.hp -= true_dmg
            this.od += true_dmg * dmg.to_od
            if this.logod:
                this.logod('%s, od+'%dmg.hostname, true_dmg * dmg.to_od,
                        'od: %d/%d'%(this.od, this.base_od) )
            this.recount(dmg.hostname, dmg.name, true_dmg, 0)
        elif this.odbk == 1:
            this.hp -= true_dmg
            this.bk -= true_dmg * dmg.to_bk
            if this.logbk:
                this.logbk('%s, od-'%dmg.hostname, true_dmg * dmg.to_bk,
                        'bk: %d/%d'%(this.bk, this.base_bk) )
            this.recount(dmg.hostname, dmg.name, true_dmg,
                    int(true_dmg * dmg.to_bk) )
        else:
            this.hp -= true_dmg
            this.recount(dmg.hostname, dmg.name, true_dmg, 0)

        if this.hp < 0 :
            this.die()
        if this.odbk == 0 and this.od > this.base_od :
            this.overdrive()
        elif this.odbk == 1 :
            if this.bk < 0:
                this.break_()


    def die(this):
        Timer.stop()
        return


    def overdrive(this):
        this.odbk = 1
        this.od = -1
        this.bk = this.base_bk
        this.def_ = this.base_def * this.od_def
        this.od_ks()
        if this.logod:
            this.logod('start')
        if 'Afflics' in this.mod:
            this.mod['Afflics'].reset()
        this.od_start = now()

    def clean_afflic(this):
        if 'Afflics' not in this.mod:
            return
        this.mod['Afflics'].reset()

    def break_(this):
        this.odbk = -1
        this.bk = -1
        this.def_ = this.base_def * this.bk_def
        def foo(t):
            this.normal()
        Timer(foo)(this.bk_time)
        this.od_ks.off()
        this.bk_ks()
        if this.logod:
            this.logod('end')
        if this.logbk:
            this.logbk('start')


    def normal(this):
        this.odbk = 0
        this.od = 0
        this.def_ = this.base_def
        this.bk_ks.off()
        if this.logbk:
            this.logbk('end')


if __name__ == '__main__':
    logset(['od','bk','debug'])
    def foo():
        c = Conf()
        c.target.name = 'dummy'
        c.target.hp = 100000
        c.target.od = 200
        c.target.bk = 300

        c._1p.atk = 3000

        conf_root = c

        tar = Target(c.target)
        #tar = Target()
        tar.init()
        dmg = lobject()
        dmg.hostname = 'noone'
        dmg.dmg = 100
        dmg.to_od = 1
        dmg.to_bk = 1

        def foo(t):
            tar.dt(dmg)
            log('debug', '%d, %d, %d'%(tar.hp, tar.od, tar.bk))
            t(60)
        Timer(foo)()
        Timer.run()
    foo()
    logcat()

