from core.ctx import *
from core import env
from core.skada import *

default_ex = ['wand','blade']

def solo(name, duration=120, ex=default_ex):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 1
    }
    env.run()
    Skada.div(env.root['duration'], env.root['sample'])

def solo_range(name, duration=120, ex=default_ex):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 256
    }
    env.run()
    Skada.div(env.root['duration'], env.root['sample'])
    env.root['range']['min'][name] /= env.root['duration']
    env.root['range']['max'][name] /= env.root['duration']


def team(conf):
    env.root = conf
    env.run()
    Skada.div(env.root['duration'],env.root['sample'])

def this_character(time=120, ex=default_ex, verbose=0, mass=0):
    import sys
    from core import characterbase as cb
    import statistic

    argv = sys.argv
    if len(argv) >= 2:
        verbose = int(argv[1])
    if len(argv) >= 3:
        duration = int(argv[2])
    if len(argv) >= 4:
        ex_lite = argv[3]
        ex = []
        ex_set = {}
        for i in ex_lite:
            if i == 'k':
                ex_set['blade'] = 1
                katana = 1
            elif i == 'r':
                ex_set['wand'] = 1
            elif i == 'd':
                ex_set['dagger'] = 1
            elif i == 'b':
                ex_set['bow'] = 1
        for i in ex_set:
            ex.append(i)

    cs = cb.Character.get_sub()

    statistic.loglevel(verbose)
    if mass and verbose<=0:
        for i in cs:
            solo_range(i, time, ex) 
    else:
        for i in cs:
            solo(i, time, ex) 

    if verbose == 0:
        statistic.show_detail()
    elif verbose == 1:
        statistic.show_rotation()
    elif verbose == 2:
        statistic.show_log()
    elif verbose == -2:
        statistic.show_csv()
    else:
        statistic.show_detail()


if __name__ == '__main__':
    logset(['all'])
    root = {
     '1p.name'     : 'Mikoto'
    ,'1p.slot.a1'  : 'VC'
    ,'1p.slot.a2'  : 'BN'
    ,'2p.name'     : 'Aeleen'
    ,'2p.acl'      : '''
        `s1
        `s2
        `fsf, x=5
    '''
    ,'target.name' : 'dummy'
    ,'ex'          : ['wand','blade']
    ,'duration'    : 120
    ,'sample'      : 1
    }
    team(root)
    logcat()



