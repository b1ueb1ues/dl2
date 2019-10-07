from core.ctx import *


class Energy():
#    def e_dmg_proc(this, name, amount):
#        this.dmg_proc_old(name, amount)  # should prevent damage in next dmg_proc
#
#        if not this.energized :
#            return
#        if this.energized == 1 and name[0] != 's':
#            return
#
#        if this.energized == 1:
#            if this.energy_consume and this.energy_consume[name[:2]]:
#                this.energized = name[:2]
#            else:
#                this.energized = name[:2]
#
#        if this.energized == name[:2] :
#            boost = this.get_energy_boost()
#            log('dmg','o_%s_energized'%name, amount*boost, 'energy boost')
#
#    def get_energy_boost(this):
#        sd = this.a.Dp.get('s')
#        this.energy_mod.on()
#        sd2 = this.a.Dp.get('s')
#        this.energy_mod.off()
#        return sd2/sd-1

    def __call__(this):
        if this.energized :
            return 5
        else:
            return this.energy

    def e_s_end(this):
        if this.energized == -1 :
            this.energized = 0
            this.energy_buff.off()
            this.energy_mod.off()

    def e_s_proc(this):
        if this.energized == 1:
            this.energized = -1

    def l_add_energy(this, e):
        this.self(e.count)

    def self(this, count):
        if not this.energized :
            this.energy += count
            if this.energy > 0:
                this.energy_buff.off()
                this.energy_buff.set(this.energy).on(-1)
            if this.energy >= 5 :
                this.energy = 0
                this.energized = 1
                this.energy_mod()
                this.energized_event()

    def team(this, count):
        this.e_add.count = count
        this.e_add()
        

    def __init__(this, a):
        this.a = a

        this.energy_mod = a.Passive('energized', 0.5, 's')

        this.energy = 0
        this.energized = 0
        this.energized_event = Event('energized')
        this.e_add = Event('add_energy')

        this.energy_buff = a.Buff('energy',-1,'energy','energy')

        if not a.s1.conf['no_energy']:
            a.s1.conf['proc'].append(this.e_s_proc)
            a.s1.conf['on_end'].append(this.e_s_end)
        if not a.s2.conf['no_energy']:
            a.s2.conf['proc'].append(this.e_s_proc)
            a.s2.conf['on_end'].append(this.e_s_end)
        if not a.s3.conf['no_energy']:
            a.s3.conf['proc'].append(this.e_s_proc)
            a.s3.conf['on_end'].append(this.e_s_end)
        Conf.sync(a.s1.conf)
        Conf.sync(a.s2.conf)
        Conf.sync(a.s3.conf)

        Listener('add_energy')(this.l_add_energy)

        this.log_e = Logger('energy')


