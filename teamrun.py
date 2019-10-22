from run import *
import statistic

logset(['all'])

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
}

team(root)

#logcat()
statistic.show_detail()

