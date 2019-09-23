import __init__
from core.ctx import *


class Skillshift(object):
    def __init__(this, host, skillidx, conf2, conf3):
        this.host = host
        skillname = 's%d'%skillidx
        this.level = 0

        this.o_on_end = host.conf[skillname]['on_end']
        host.conf[skillname]['on_end'] = this.shift
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


    def shift(this):
        if this.o_on_end:
            this.o_on_end()
        if this.level == 0:
            this.host.s1 = this.s_level2
            this.level = 1
            if this.log:
                this.log('%s, skill_levelup'%this.host.name,2)
        elif this.level == 1:
            this.host.s1 = this.s_level3
            this.level = 2
            if this.log:
                this.log('%s, skill_levelup'%(this.host.name),3)
        elif this.level == 2:
            this.host.s1 = this.host.a_s[0]
            this.level = 0
            if this.log:
                this.log('%s, skill_leveldown'%(this.host.name),0)

    def reset(this):
        this.host.s1 = this.host.a_s[0]
        this.level = 0

