from core.ctx import *


class Dmg(object):
    def __init__(this, dmg=0):
        this.dmg = dmg
        this.to_od = 1 # rate
        this.to_bk = 1 # rate


class Damagecalc(object):
    @classmethod
    def init(cls):
        def l_cbd(e):
            src = e.src
            dst = e.dst
            name = e.name

            atk = 1.0 * src.mod('atk') * src.base_atk
            _def = dst.mod('def') * dst.base_def
            e.dmg = 1.5/0.6 * atk / _def * src.mod('dmg') * src.dmg_mod(name)
        Event('dc.cbd')(l_cbd) # damageCalculation::calculationBaseDamage


    def __init__(this, src, dst):
        this.src = src
        this.dst = dst


    def calc_basedmg(this, atype):
        atk = 1.0 * this.src.mod('atk') * this.src.base_atk
        _def = this.dst.mod('def') * this.dst.base_def
        return 1.5/0.6 * atk / _def * this.src.mod('dmg') * this.src.mod(atype)


    def __call__(this, name, coef):
        return coef * this.calc_basedmg(name)



if __name__ == '__main__':

    class Mod(Modifier):
        'test'
        pass
    Mod.init()
    m1 = Mod('m1', 'atk', 'p', 0.15)
    print(Mod.mod('atk'))
    print(Mod.mod('def'))

    class Nop(object):
        pass
    src = Nop()
    dst = Nop()

    def mod(name):
        return 1
    src.base_atk = 3000
    src.mod = mod
    dst.base_def = 10
    dst.mod = mod
    src.dmg_mod = mod


    Damagecalc.init()
    e = Event('dc.cbd')
    e.src = src
    e.dst = dst
    e()
    print(e.dmg)

    dc = Damagecalc(src, dst)
    dc.calc_basedmg('test')
