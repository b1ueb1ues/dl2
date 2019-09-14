from ctx import *


class Hits(object):
    def __init__(this, host, hitattr):
        this.host = host
        this.hitattr = hitattr
        this.timer = []
        idx = 0
        for i in hitattr :
            idx += 1
            t = Timer(this.cb, i)
            t.idx = idx
            this.timer.append(t)


    def on(this):
        for i in this.timer :
            i.on()


    def off(this):
        for i in this.timer :
            i.off()

    
    def cb(this, t):
        this.host._act(t.idx)


class characterbase(object):
    class Mod(Modifier):
        pass

    def __init__(this):
        this.base_atk = 0
        this.base_def = 10
        this.base_hp = 0
        this.base_od = 0
        this.base_bk = 0

        this.hp = 0
        this.od = 0
        this.bk = 0

        this.odbk = 0 # 0: normal, 1: od, 2: bk

        this.conf = Conf()


    def sync_conf(this, c, cc):
        this.base_hp = c.hp
        this.base_od = c.od
        this.base_bk = c.bk
        this.base_atk = c.atk
        this.base_def = c.def_


    def dt(this, dmg): # damage take
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
        if this.od > this.base_od:
            this.overdrive()
        if this.bk < 0:
            this._break()


    def die(this):
        pass


    def overdrive(this):
        this.odbk = 1
        this.od = 0
        this.bk = this.base_bk
        # clean afflic


    def _break(this):
        this.odbk = 2
        this.bk = this.base_bk
        # break debuff 
        # break timer return normal


