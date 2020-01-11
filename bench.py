from core.ctx import *
from target.hms import *
from character.mikoto import *
from character.natalie import *
from character.elisanne import *
from character.addis import *
from core import benchmark
from core.skada import *
from run import *

root = {
 '1p.name'     : 'Mikoto'
,'1p.slot.a1'  : 'VC'
,'1p.slot.a2'  : 'BN'
,'2p.name'     : 'Aeleen'
,'2p.slot.a1'  : 'SDO'
,'2p.acl'      : '''
    #import core.log
    #core.log.log_('dbg','Aeleen', e.type)
    `s1, fs=1
    `s1
    `s2
    `fs, x=5
'''
,'target.name' : 'dummy'
,'ex'          : []
,'duration'    : 120
,'sample'      : 1
,'condi'       : True
}


def foo():
    team(root);

logset([])
foo()
#benchmark.run(foo, 1000)

#logcat()
#Skada.sum()
