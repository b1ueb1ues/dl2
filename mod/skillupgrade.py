import __init__
from core.ctx import *


class Skillupgrade(object):
    def __init__(this, host, skillidx, conf2, ssbuff):
        this.host = host
        skillname = 's%d'%skillidx
        this.level = 0

        Conf.sync(host.conf[skillname])

        conf22 = Conf()
        conf22.update(Conf(host.conf[skillname]))
        conf22.update(Conf(conf2))


        this.s_upgraded = host.Skill('%s_2'%skillname, host, conf22.get)
        this.s_upgraded.sp = host.s1.sp
        this.log = Logger('s')


    def upgrade(this):
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

