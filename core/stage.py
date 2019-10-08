
class _Fake_event():
    def __init__(this, target):
        this.target = target
    def __call__(this):
        for i in this.target:
            i(this)

class Stage():
    @classmethod
    def init(cls)
        cls.help = []
        cls.harm = []

    def add(this,ctype, c=None):
        if ctype == 'help':
            this.help.append(c)
        elif ctype == 'harm':
            this.harm.append(c)

    def help(this):
        return _Fake_event(this.help)

    def harm(this):
        return _Fake_event(this.harm)

    def _1p(this):
        return cls.help[0]




