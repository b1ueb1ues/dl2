from core.ctx import *
from core import env
from core.skada import *

logset('all')

logset('dmg')
logset('buff')
logset('bk')
#logset('dot')
#logset('afflic')
logset('s')
logset('sp')
#logset('act')
#logset('x')

env.root = {
 '1p.name'     : 'Mikoto'
,'1p.slot.a1'  : 'EE'
,'1p.slot.a2'  : 'RR'
,'2p.name'     : 'Elisanne'
,'3p.name'     : 'Natalie'
,'4p.name'     : 'Rena'
,'target.name' : 'dummy'
,'ex'          : []
,'duration'    : 120
,'sample'      : 1
}
env.run()
logcat()
Skada.div(env.root['duration']*env.root['sample'])
d = Skada.sum()



