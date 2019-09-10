from core.ctx import *


class Characterbase(object):
    class Mod(Modifier):
        pass

    def __init__(this):
        this.hp = 0
        this.od = 0
        this.bk = 0

        this.odbk = 0 # 0: normal, 1: od, 2: bk

        this.conf = Conf( {
            "hp": 0,
            "od": 0,
            "bk": 0,
            "atk":0,
            "def_":0,
                    })
        this.conf.sync_conf = this.sync_conf


    def init(this):
        this.hp = this.base_hp


    def sync_conf(this, c, cc):
        this.base_hp = c.hp
        this.base_od = c.od
        this.base_bk = c.bk
        this.base_atk = c.atk
        this.base_def = c.def_
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
        this.bk = this.base_bk
        # clean afflic


    def break_(this):
        this.odbk = 2
        this.bk = this.base_bk
        # break debuff 
        # break timer return normal


if __name__ == '__main__':
    c = Characterbase()
    c.conf.hp = 10000
    c.conf.od = 200
    c.conf.bk = 300
    c.init()

    dmg = Dmg(100)
    c.dt(dmg)
    print('-')
    print(c.hp)
    print(c.od)
    print(c.bk)


    dmg = Dmg(200)
    c.dt(dmg)
    print('-')
    print(c.hp)
    print(c.od)
    print(c.bk)

    dmg = Dmg(100)
    c.dt(dmg)
    print('-')
    print(c.hp)
    print(c.od)
    print(c.bk)
