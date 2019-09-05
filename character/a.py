import __init__
from core.action import *


logset('act')

Action.init()
a = Action('foo')
a.interrupt_by = ['bar']
a()

b = Action('bar')
b.conf.startup = 1.2
b()

Action.init()

c = Action('baz')
c.conf.recovery = 1.9+1.2
c()

Timer.run()
#print(a.conf)
logcat()

