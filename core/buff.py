import __init__
from core.ctx import *


class Selfbuff(object):
    def __init__(this, src, dst):
        this.src = src
        this.dst = dst


    def __call__(this, *args, **kwargs):
        class __Selfbuff(_Selfbuff):
            _static = this
        return __Selfbuff(*args, **kwargs)


class _Selfbuff(object):
    def __init__(this):
        pass




if __name__ == '__main__':

    pass
