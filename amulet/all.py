import __init__
from amulet import *
from core.ctx import *


class Plunder_Pals(Amulet): #Plunder Pals or Hitting the Books
    atk = 54
    a = [('sd', 0.25)]
PP = Plunder_Pals


class Resounding_Rendition(Amulet):
    atk = 64
    a = [('sd', 0.30),
         ('cc', 0.08,'hp70')]
RR = Resounding_Rendition


class Crystalian_Envoy(Amulet):
    atk = 57
    a = [('atk', 0.13,'hp70')]
CE = Crystalian_Envoy	


class Bonds_Between_Worlds(Amulet):
    atk = 54
    a = [('atk', 0.13,'hp70'),
         ('prep', 0.25)]
Bonds = Bonds_Between_Worlds
BBW = Bonds_Between_Worlds


class Levins_Champion(Amulet):
    atk = 64
    a = [('cd', 0.15),
         ('cc', 0.10,'hp70')]
LC = Levins_Champion


class Valiant_Crown(Amulet):
    atk = 65
    a = [('sd', 0.30),
         ('def_c_atk', 0.10)]
VC = Valiant_Crown


class Tough_Love(Amulet):
    atk = 65
    a = [('sd', 0.25),
         ('lo', 0.50)]
TL = Tough_Love


class Flash_of_Genius(Amulet): # Flash of Genius
    atk = 57
    a = [('atk', 0.20,'hit15')]
FG = Flash_of_Genius
FoG = Flash_of_Genius


class Fresh_Perspective(Amulet):
    atk = 52
    a = [('fs', 0.40),
         ('sd', 0.20)]
FP = Fresh_Perspective


class Bellathorna(Amulet):
    atk = 25
    a = [('bt', 0.20)]
BT = Bellathorna


#class Together_We_Stand(Amulet):
#    atk = 52
#    a = [('sts', 0.5),
#         ('sd', 0.20)]


class First_Rate_Hospitality(Amulet):
    atk = 55
    a = [('atk', 0.08,'hp70'),
         ('def_c_atk', 0.10)]
FRH = First_Rate_Hospitality


class The_Bustling_Hut(Amulet):
    atk = 50
    a = [('def_c_atk', 0.08)]
    def __init__(this, c):
        if c.ele == 'light':
            a = [('def_c_atk', 0.08),
                 ('sp', 0.07)]


class Jewels_of_the_Sun(Amulet):
    atk = 64
    a = [('sp', 0.08),
         ('atk', 0.10, 'hp70')]
JotS = Jewels_of_the_Sun


class Heralds_of_Hinomoto(Amulet):
    atk = 64
    a = [('sd', 0.30),
         ('sp', 0.06)]
HoH = Heralds_of_Hinomoto
HH = Heralds_of_Hinomoto


class One_with_the_Shadows(Amulet):
    atk = 51
    a = [('cc', 0.06),
         ('bk', 0.20)]


class Flower_in_the_Fray(Amulet):
    atk = 52
    a = [('cd', 0.15),
         ('sd', 0.20)]
FitF = Flower_in_the_Fray


class The_Prince_of_Dragonyule(Amulet):
    atk = 63
    a = [('cd', 0.20)]
    def __init__(this, c):
        if c.ele == 'water':
            this.a = [('cd', 0.20)]
            this.a += [('cc', 0.12,'hit15')]


class Evening_of_Luxury(Amulet):
    atk = 65
    a = [('atk', 0.15, 'hp100'),
         ('cd', 0.15)]
EoL = Evening_of_Luxury


class Seaside_Princess(Amulet):
    atk = 65
    a = [('atk', 0.15, 'hp100'),
         ('cd', 0.22, 'hp100')]
SSP = Seaside_Princess


class The_Chocolatiers(Amulet):
    atk = 62
    a = [('prep', 1.00)]
Choco = The_Chocolatiers


class Worthy_Rivals(Amulet):
    atk = 64
    a = [('bk', 0.30),
         ('prep', 0.25)]


class Lord_of_the_Skies(Amulet):
    atk = 46
    a = [('od', 0.10)]


class Witchs_Kitchen(Amulet):
    atk = 57
    a = [('sd', 0.40, 'hp100'),
         ('resist', 0.50, 'blind')]


class Silke_Lends_a_Hand(Amulet):
    atk = 42
    a = [('sd', 0.20),
         ('resist', 0.50, 'blind')]


class Saintly_Delivery(Amulet):
    atk = 42
    a = [('sd', 0.20),
         ('resist', 0.50, 'stun')]


class Luck_of_the_Draw(Amulet):
    atk = 33
    a = [('resist', 0.25, 'paralysis')]
    def __init__(this, c):
        if c.ele == 'shadow':
            this.a = [('resist', 0.25, 'paralysis')]
            this.a += [('bt', 0.25)]


class Lunar_Festivities(Amulet): 
    atk = 51
    a = [('fs', 0.40),
         ('sp', 0.10, 'fs')]


class The_Warrioresses(Amulet):
    atk = 52
    a = [('fs', 0.40),
         ('cd', 0.13)]


class Stellar_Show(Amulet):
    atk = 65
    a = [('fs', 0.50),
         ('cd', 0.15)]
SS = Stellar_Show


class Kung_Fu_Masters(Amulet):
    atk = 64
    a = [('sd', 0.20)]
    def __init__(this, c):
        if c.wt == 'axe':
            this.a = [('sd', 0.20)]
            this.a += [('cc', 0.14)]
KFM = Kung_Fu_Masters


class Forest_Bonds(Amulet):
    atk = 64
    a = [('sp', 0.12, 'fs')]
    def __init__(this, c):
        if c.wt == 'bow':
            this.a = [('sp', 0.12, 'fs')]
            this.a += [('sd', 0.40)]
FB = Forest_Bonds


class Dragon_and_Tamer(Amulet):  
    atk = 57
    def __init__(this, c):
        if c.wt == 'lance':
            this.a = [('sd', 0.40)]
DnT = Dragon_and_Tamer


class Twinfold_Bonds(Amulet):  
    atk = 65
    a = [('atk', 0.15, 'hit15')]
    def __init__(this, c):
        if c.wt == 'dagger':
            this.a = [('sd', 0.40)]
            this.a += [('atk', 0.15, 'hit15')]
TB = Twinfold_Bonds


class Summer_Paladyns(Amulet):  
    atk = 64
    a = [('')]
    def __init__(this, c):
        if c.wt == 'axe':
            this.a = [('sd', 0.40)]

    def dc_energy(this, e):
        e = this.adv.Event('add_energy')
        e.name = 'self'
        e()

    def oninit(this, adv):
        Amulet.oninit(this, adv)
        this.adv = adv
        adv.Listener('defchain',this.dc_energy)


class The_Shining_Overlord(Amulet):
    atk = 65
    a = [('dc', 3)]
    def __init__(this, c):
        if c.wt == 'sword':
            this.a = [('dc', 3)]
            this.a += [('sd', 0.40)]
TSO = The_Shining_Overlord


class Halidom_Grooms(Amulet):
    atk = 50
    a = [('bt', 0.20)]

    def dc_energy(this, e):
        e = this.adv.Event('add_energy')
        e.name = 'self'
        e()

    def oninit(this, adv):
        Amulet.oninit(this, adv)
        this.adv = adv
        adv.Listener('defchain',this.dc_energy)
HG = Halidom_Grooms


class Beach_Batkle(Amulet):
    atk = 50
    a = [('bt', 0.20)]
    def __init__(this, c):
        if c.ele == 'water':
            this.a = [('bt', 0.20), ('sp', 0.07)]
BB = Beach_Batkle


class The_Petal_Queen(Amulet):
    atk = 53

    def startup(this, t):
        e = this.adv.Event('add_energy')
        e.name = 'self'
        e()
        e()
        e()
        e()
        e()

    def oninit(this, adv):
        Amulet.oninit(this, adv)
        this.adv = adv
        adv.Timer(this.startup).on()


class Hanetsuki_Rally(Amulet):
    atk = 51
    a = [('cc', 0.05),('lo', 0.40)]
HR = Hanetsuki_Rally


class Indelible_Summer(Amulet):
    atk = 52
    def __init__(this, c):
        if c.ele == 'water':
            this.a = [('sp', 0.09)]
IS = Indelible_Summer


class Sisters_Day_Out(Amulet):
    atk = 64
    a = [('fs', 0.40)]
    def fs_proc(this, e):
        this.o_fs_proc(e)
        if this.charges > 0:
            this.adv.charge_p('sisters_day_out','25%')
            this.charges -= 1

    def oninit(this, adv):
        Amulet.oninit(this, adv)
        this.charges = 3
        this.adv = adv
        this.o_fs_proc = adv.fs_proc
        adv.fs_proc = this.fs_proc
SDO = Sisters_Day_Out


class Elegant_Escort(Amulet):
    atk = 54
    a = [('k_burn', 0.30)]
EE = Elegant_Escort

class Beautiful_Nothingness(Amulet):
    atk = 52
    a = [('atk', 0.10, 'hp70'),('cc', 0.05)]
BN = Beautiful_Nothingness

class Resurgent_Despair(Amulet):
    atk = 64
    a = [('sp', 0.06)]
    def fs_proc(this, e):
        this.o_fs_proc(e)
        if this.charges > 0:
            this.adv.charge_p('Resurgent_Despair','25%')
            this.charges -= 1

    def oninit(this, adv):
        Amulet.oninit(this, adv)
        this.charges = 3
        this.adv = adv
        this.o_fs_proc = adv.fs_proc
        adv.fs_proc = this.fs_proc
RD = Resurgent_Despair

#amulets = []
#for k in list(globals()):
#    v = globals()[k]
#    if type(v) == type(Conf):
#        if v.__module__ == 'slot.a.all':
#            amulets.append(v)
#
