import __init__
from core.ctx import *
from core.skill import Fs_group


class Fs_alt(object):
    def __init__(this, host, conf2, ssbuff):
        this.host = host
        this.level = 0

        conf22 = Conf(conf2)

        this.fs_alt = Fs_group(host, conf22.get)
        this.log = Logger('fs')
        this.loghost = host.name

        this.buff = ssbuff
        ssbuff.on_end.append(this.on_buff_end)

    def off(this):
        this.buff.off()

    def on_buff_end(this):
        if this.level == 1:
            this.host.fs = this.host.a_fs[0]
            this.level = 0
            if this.log:
                this.log(this.loghost, '%s, fs_alt -'%(this.host.name))

    def alt(this, duration):
        this.buff.on(duration)
        if this.level == 0:
            this.host.fs = this.fs_alt
            this.level = 1
            if this.log:
                this.log(this.loghost, '%s, fs_alt +'%this.host.name)
    __call__ = alt

    def reset(this):
        this.host.fs = this.host.a_fs[0]
        this.level = 0

