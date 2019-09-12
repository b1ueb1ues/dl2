import __init__
from core.ctx import *



class Target(object):
    def default(this, conf):
        conf.def_    = 10
        conf.od_def  = 1
        conf.bk_def  = 0.6
        conf.bk_time = 10

        conf.name    = 'target'
        conf.ele     = 'on'
        conf.hp      = 1000000
        conf.od      = 200000
        conf.bk      = 200000


    def __init__(this, conf=None):
        this.odbk = 0 # 0: normal, 1: od, -1: bk
        this.od = 0
        this.bk = -1

        tmp = Conf()             
        this.default(tmp)    # conf prior
        this.config(tmp)     # default < class < param
        if conf:
            tmp(conf)
            conf(tmp)
            tmp = conf
        this.conf = tmp
        this.conf.sync_target = this.sync

        this.skada = {}
        #Event('dmg')(this.l_dmg)
        #this.e_ks = Event('killer')
        this.logdbg = Logger('debug')
        this.logod = Logger('od')
        this.logbk = Logger('bk')
        this.logdmg = Logger('dmg')


    def classinit(this):
        conf = Conf()
        conf.src = this.conf
        this.Dp = Dmg_param(this.conf)
        this.Buff = Buff(this.Dp)
        this.Passive = Passive(this.Dp)
        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)


    def config(this, conf):
        pass


    # after all config settle down
    def init(this):
        this.classinit()
        this.hp = this.base_hp
        this.def_ = this.base_def
        this.od_ks = this.Dp('od', 'ks', 'od', 1)
        this.bk_ks = this.Dp('bk', 'ks', 'bk', 1)


    def sync(this, c, cc):
        this.base_def = c.def_

        this.base_hp = c.hp
        this.base_od = c.od
        this.base_bk = c.bk

        this.od_def = c.od_def
        this.bk_def = c.bk_def
        this.bk_time = c.bk_time

        if this.base_def <= 0:
            print('base_def:%d <= 0'%this.base_def)
            errrrrrrrrrrr()
        if this.base_od > 0:
            this.dt = this.dt_odbk
        else:
            this.od = -1
            this.dt = this.dt_no_od


    def recount(this, dmg):
        if this.logdmg:
            this.logdmg('%s, %s'%(dmg.hostname, dmg.name), dmg.dmg, 'hp: %d'%(this.hp) )


    def dt(this, dmg):
        print('targetbase dt not init')
        errrrrrrrrrrrrrrrrrrrr()


    def dt_no_od(this, dmg):
        this.recount(dmg)
        this.hp -= dmg.dmg
        if this.hp < 0 :
            this.die()


    def dt_odbk(this, dmg): 
        this.recount(dmg)
        true_dmg = dmg.dmg
        if this.odbk == 0 :
            this.hp -= true_dmg
            this.od += true_dmg * dmg.to_od
            if this.logod:
                this.logod('%s, od+'%dmg.hostname, true_dmg * dmg.to_od)
        elif this.odbk == 1:
            this.hp -= true_dmg
            this.bk -= true_dmg * dmg.to_bk
            if this.logbk:
                this.logbk('%s, od-'%dmg.hostname, true_dmg * dmg.to_bk)
        else:
            this.hp -= true_dmg

        if this.hp < 0 :
            this.die()
        if this.odbk == 0 and this.od > this.base_od :
            this.overdrive()
        elif this.odbk == 1 and this.bk < 0:
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
        ##
        # TODO: clean afflic
        #

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
        c.target.def_ = 10
        c.target.od_def = 1
        c.target.bk_def = 0.6
        c.target.bk_time = 5

        c._1p.atk = 3000

        conf_root = c

        tar = Target()
        tar.init()
        dmg = lobject()
        dmg.dmg = 100
        dmg.to_od = 1
        dmg.to_bk = 1

        def foo(t):
            tar.dt(dmg)
            if this.logdbg:
                this.logdbg('%d, %d, %d'%(tar.hp, tar.od, tar.bk))
            t(1)
        Timer(foo)()
        Timer.run()
    logcat()
