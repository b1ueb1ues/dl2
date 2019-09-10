import __init__
from core.ctx import *


class Target(object):
    def __init__(this, conf):
        this.odbk = 0 # 0: normal, 1: od, -1: bk
        this.od = 0
        this.bk = -1

        this.conf = conf
        this.config(conf)
        this.conf.sync_target = this.sync_conf

        this.skada = {}
        Event('dmg')(this.l_dmg)


    def classinit(this):
        conf = Conf()
        conf.src = this.conf
        this.Dc = Dmg_calc(conf)
        this.Buff = Buff(this.Dc)
        this.Passive = Passive(this.Dc)
        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)


    def config(this, conf):
        pass


    def init(this):
        this.classinit()
        this.hp = this.base_hp
        this.def_ = this.base_def


    def sync_conf(this, c, cc):
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
        pass


    def defence(this, dmg):
        def_ = this.def_ * this.Dc.get('def')
        true_dmg = dmg.dmg / def_
        for i in dmg.killer :
            if i in this.ks :
                true_dmg += true_dmg * dmg.killer[i]
        if this.odbk == -1 and dmg.bk :
            true_dmg += true_dmg * dmg.bk
        return true_dmg


    def dt(this, dmg):
        pass


    def dt_no_od(this, dmg):
        true_dmg = this.defence(dmg)
        this.recount(true_dmg)
        this.hp -= true_dmg
        if this.hp < 0 :
            this.die()


    def dt_odbk(this, dmg): 
        true_dmg = this.defence(dmg)
        this.recount(true_dmg)
        if this.odbk == 0 :
            this.hp -= true_dmg
            this.od += true_dmg * dmg.to_od
            if verbose('od'):
                log_('od', 'od+', true_dmg * dmg.to_od)
        elif this.odbk == 1:
            this.hp -= true_dmg
            this.bk -= true_dmg * dmg.to_bk
            if verbose('bk'):
                log_('bk', 'od-', true_dmg * dmg.to_od)
        else:
            this.hp -= true_dmg

        if this.hp < 0 :
            this.die()
        if this.odbk == 0 and this.od > this.base_od :
            this.overdrive()
        elif this.odbk == 1 and this.bk < 0:
            this.break_()


    def die(this):
        pass


    def overdrive(this):
        this.odbk = 1
        this.od = -1
        this.bk = this.base_bk
        this.def_ = this.base_def * this.od_def
        log('od','start')
        # clean afflic


    def break_(this):
        this.odbk = -1
        this.bk = -1
        this.def_ = this.base_def * this.bk_def
        def foo(t):
            this.normal()
        Timer(foo)(this.bk_time)
        log('od','end')
        log('bk','start')


    def normal(this):
        this.odbk = 0
        this.od = 0
        this.def_ = this.base_def
        log('bk','end')


if __name__ == '__main__':
    logset(['od','bk','debug'])

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

    tar = Target(c.target)
    tar.init()
    dmg = lobject()
    dmg.dmg = 1000
    dmg.to_od = 1
    dmg.to_bk = 1
    dmg.bk = 0

    def foo(t):
        tar.dt(dmg)
        log('debug', '%d, %d, %d'%(tar.hp, tar.od, tar.bk))
        t(1)
    Timer(foo)()

    Timer.run()
    logcat()
