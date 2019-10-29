import __init__
from core.ctx import *


class Skillshift(object):
    def __init__(this, host, skillidx, conf2, conf3):
        this.host = host
        skillname = 's%d'%skillidx
        this.level = 0
        this.hit = 0

        host.conf[skillname]['on_end'].append(this.shift)
        host.conf[skillname]['proc'].append(this.on_hit)
        Conf.sync(host.conf[skillname])

        conf22 = Conf()
        conf22.update(Conf(host.conf[skillname]))
        conf22.update(Conf(conf2))

        conf33 = Conf()
        conf33.update(Conf(host.conf[skillname]))
        conf33.update(Conf(conf3))

        this.s_level2 = host.Skill('%s_2'%skillname, host, conf22.get)
        this.s_level3 = host.Skill('%s_3'%skillname, host, conf33.get)
        this.s_level2.sp = host.s1.sp
        this.s_level3.sp = host.s1.sp
        this.log = Logger('s')
        this.loghost = host.name


    def on_hit(this):
        this.hit = 1

    def shift(this):
        if this.hit:
            return
        else:
            this.hit = 0
        if this.level == 0:
            this.host.s1 = this.s_level2
            this.level = 1
            if this.log:
                this.log(this.loghost, 'skill_levelup', 2)
        elif this.level == 1:
            this.host.s1 = this.s_level3
            this.level = 2
            if this.log:
                this.log(this.loghost, 'skill_levelup', 3)
        elif this.level == 2:
            this.host.s1 = this.host.a_s[0]
            this.level = 0
            if this.log:
                this.log(this.loghost, 'skill_leveldown', 0)

    def reset(this):
        this.host.s1 = this.host.a_s[0]
        this.level = 0

