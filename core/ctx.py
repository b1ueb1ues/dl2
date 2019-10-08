import __init__

from core.timer      import *
from core.event      import *
from core.conf       import *
from core.log        import *
from core.condition  import *
from core.dmg        import *
from core.buff       import *


ctx = 0
class Ctx(object):
    def __init__(this):
        global ctx
        this.el = Event.init()
        this.tl = Timer.init()
        this.log = Log.init()
        ctx = this

    def __call__(this):
        global ctx
        Event.init(this.el)
        Timer.init(this.tl)
        Log.init(this.log)
        ctx = this

dprint = print
