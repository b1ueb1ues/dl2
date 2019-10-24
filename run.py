from core.ctx import *
from core import env
from core.skada import *

default_ex = []
#default_ex = ['wand','blade']


def fake_team(duration, ex):
    bak = env.root
    env.root = {
     '1p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 1
    }
    env.run()
    skada.div(duration, 1)
    d = skada.sum(q=1)
    env.root = bak
    env.root['team_dps'] = d['_Faketeam']['dmg']
    return env.root['team_dps']


def solo(name, duration=120, ex=default_ex):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 1
    }
    ctx1 = env.run()
    Ctx()
    tmp = skada.get()
    skada.reset()
    ####
    fake_team(duration, ex)
    ####
    ctx1()
    skada.set(tmp)

    skada.div(env.root['duration'], env.root['sample'])


def solo_range(name, duration=120, ex=default_ex):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 256
    }
    ctx1 = env.run()
    skada.div(env.root['duration'], env.root['sample'])

    dmin = env.root['range']['min'][name] / env.root['duration']
    dmax = env.root['range']['max'][name] / env.root['duration']
    tmin = env.root['range']['min']['_Faketeam'] / env.root['duration']
    tmax = env.root['range']['max']['_Faketeam'] / env.root['duration']

    Ctx()
    tmp = skada.get()
    skada.reset()
    ####
    a = fake_team(duration, ex)
    ####
    ctx1()
    skada.set(tmp)

    bmin = (tmin/env.root['team_dps']-1)*10000
    bmax = (tmax/env.root['team_dps']-1)*10000

    env.root['range'] = {}
    env.root['range']['dmin'] = int(dmin)
    env.root['range']['dmax'] = int(dmax)
    env.root['range']['tmin'] = int(tmin)
    env.root['range']['tmax'] = int(tmax)
    env.root['range']['bmin'] = int(bmin)
    env.root['range']['bmax'] = int(bmax)


def team(conf):
    env.root = conf
    env.run()
    skada.div(env.root['duration'],env.root['sample'])


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
    elif verbose == 3:
        statistic.show_log()
    elif verbose == -2:
        statistic.show_csv()
    else:
        statistic.show_detail()


if __name__ == '__main__':
    pass
