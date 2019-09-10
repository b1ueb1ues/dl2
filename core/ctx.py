import __init__

from core.timer      import *
from core.event      import *
from core.conf       import *
from core.log        import *
from core.condition  import *
from core.dmgcalc    import *
from core.buff       import *


class Ctx(object):
    def __init__(this):
        this.el = Event.init()
        this.tl = Timer.init()
        this.log = Log.init()

    def __call__(this):
        Event.init(this.el)
        Timer.init(this.tl)
        Log.init(this.log)

ctx = Ctx()
