import __init__
from core.ctx import *
from core.buff import *


class characterbase(object):
    def classinit(this):
        this.Dc = Dmg_calc(this.conf.dc)
        this.Buff = Buff(this.Dc)
        this.Passive = Passive(this.Dc)
        this.Selfbuff = Selfbuff(this.Buff)
        this.Teambuff = Teambuff(this.Buff)
        this.Zonebuff = Zonebuff(this.Buff)
        this.Debuff = Debuff(this.Buff)


    def __init__(this, conf):
        global conf_root
        this.conf = conf
        this.conf.dc.src = this.conf
        this.conf.dc.dst = conf_root.target
        this.ex = conf_root.ex

        this.odbk = 0 # 0: normal, 1: od, 2: bk

    def init(this):
        this.hp = this.base_hp
        this.od = 0
        this.bk = this.base_bk


    def sync_conf(this, c, cc):
        this.base_hp = c.hp
        this.base_od = c.od
        this.base_bk = c.bk
        this.base_atk = c.atk
        this.base_def = c.def_
        if this.base_def <= 0:
            print('base_def:%d <= 0'%this.base_def)
            errrrrrrrrrrr()
        if this.base_od > 0:
            this.dt = this.dt_odbk
        else:
            this.dt = this.dt_no_od


    def dt(this, dmg):
        pass


    def dt_no_od(this, dmg):
        if this.odbk == 0 :
            this.hp -= dmg.dmg
            this.od += dmg.dmg * dmg.to_od
        elif this.odbk == 1:
            this.hp -= dmg.dmg
            this.bk -= dmg.dmg * dmg.to_bk
        else:
            this.hp -= dmg.dmg

        if this.hp < 0 :
            this.die()


    def dt_odbk(this, dmg): # damage take
        if this.odbk == 0 :
            this.hp -= dmg.dmg
            this.od += dmg.dmg * dmg.to_od
        elif this.odbk == 1:
            this.hp -= dmg.dmg
            this.bk -= dmg.dmg * dmg.to_bk
        else:
            this.hp -= dmg.dmg

        if this.hp < 0 :
            this.die()
        if this.base_od > 0 and this.od > this.base_od :
            this.overdrive()
        if this.bk < 0:
            this.break_()


    def die(this):
        pass


    def overdrive(this):
        this.odbk = 1
        this.od = 0
        if this.od != 1:
            this.Buff('od', this.od_def-1.0, 'def')(this.od_time)
        # clean afflic


    def break_(this):
        this.odbk = 2
        this.bk = this.base_bk
        if this.bk_def != 1:
            this.Buff('bk', this.bk_def-1.0, 'def')(this.bk_time)
        def foo(t):
            this.normal()
        Timer(foo)(this.bk_time)


    def normal(this):
        this.odbk = 0

