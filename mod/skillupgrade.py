import __init__
from core.ctx import *


class Skillupgrade(object):
    def __init__(this, host, skillidx, conf2, ssbuff):
        this.host = host
        skillname = 's%d'%skillidx
        this.level = 0

        host.conf[skillname]['on_start'].append(this.pause)
        Conf.sync(host.conf[skillname])

        conf22 = Conf()
        conf22.update(Conf(host.conf[skillname]))
        conf22.update(Conf(conf2))

        this.s_upgraded = host.Skill('%s+'%skillname, host, conf22.get)
        this.s_upgraded.sp = host.s1.sp
        this.log = Logger('s')
        this.loghost = host.name

        this.buff = ssbuff
        ssbuff.on_end.append(this.on_buff_end)

    def pause(this):
        this.buff.append(this.host.s1.conf['stop'])

    def on_buff_end(this):
        if this.level == 1:
            this.host.s1 = this.host.a_s[0]
            this.level = 0
            if this.log:
                this.log(this.loghost, 'skill -')

    def upgrade(this, duration):
        this.buff.on(duration)
        if this.level == 0:
            this.host.s1 = this.s_upgraded
            this.level = 1
            if this.log:
                this.log(this.loghost, 'skill +')
    __call__ = upgrade

    def reset(this):
        this.host.s1 = this.host.a_s[0]
        this.level = 0

