import __init__
from core.ctx import *


class Skillupgrade(object):
    def __init__(this, host, skillidx, conf2, ssbuff):
        this.host = host
        skillname = 's%d'%skillidx
        this.level = 0

        this.o_on_start = host.conf[skillname]['on_start']
        host.conf[skillname]['on_start'] = this.pause
        Conf.sync(host.conf[skillname])

        conf22 = Conf()
        conf22.update(Conf(host.conf[skillname]))
        conf22.update(Conf(conf2))

        this.s_upgraded = host.Skill('%s+'%skillname, host, conf22.get)
        this.s_upgraded.sp = host.s1.sp
        this.log = Logger('s')

        this.buff = ssbuff
        this.o_on_end = ssbuff.on_end
        ssbuff.on_end = this.on_buff_end

    def pause(this):
        if this.o_on_start:
            this.o_on_start()
        this.buff.append(this.host.s1.conf['recovery'])

    def on_buff_end(this):
        if this.level == 1:
            this.host.s1 = this.host.a_s[0]
            this.level = 0
            if this.log:
                this.log('%s, skill -'%(this.host.name))
        this.o_on_end()

    def upgrade(this, duration):
        this.buff.on(duration)
        if this.o_on_end:
            this.o_on_end()
        if this.level == 0:
            this.host.s1 = this.s_upgraded
            this.level = 1
            if this.log:
                this.log('%s, skill +'%this.host.name)
    __call__ = upgrade

    def reset(this):
        this.host.s1 = this.host.a_s[0]
        this.level = 0

