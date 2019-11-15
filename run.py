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
    ,'condi'       : True
    }
    env.run()
    skada.div(duration, 1)
    d = skada.sum(q=1)
    env.root = bak
    env.root['team_dps'] = d['_Faketeam']['dps']
    return env.root['team_dps']


def solo(name, duration=120, ex=default_ex, condi=True):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 1
    ,'condi'       : condi
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


def solo_range(name, duration=120, ex=default_ex, condi=True):
    env.root = {
     '1p.name'     : name
    ,'2p.name'     : '_Faketeam'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 256
    ,'condi'       : condi
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


def this_character(time=120, ex=default_ex, verbose=-2, mass=0):
    _this_character(time=120, ex=default_ex, verbose=-2, mass=0, condi=True)
    skada.reset()
    _this_character(time=120, ex=default_ex, verbose=-2, mass=0, condi=False)


def _this_character(time=120, ex=default_ex, verbose=-2, mass=0, condi=True):
    import sys
    from core import characterbase as cb
    import statistic

    argv = sys.argv
    ex_lite = ''
    if len(argv) >= 2:
        verbose = int(argv[1])
    if len(argv) >= 3:
        time = int(argv[2])
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
        for i in cs :
            if i[0] != '_':
                solo_range(i, time, ex, condi) 
    else:
        for i in cs :
            if i[0] != '_':
                solo(i, time, ex, condi) 

    if verbose == 0:
        statistic.show_single_detail()
        #statistic.show_detail()
    elif verbose == 1:
        statistic.show_rotation()
    elif verbose == 2:
        statistic.show_log()
    elif verbose == 3:
        statistic.show_log()
    elif verbose == -2:
        statistic.show_csv()
    elif verbose == -5:
        if ex_lite == '':
            print('-,%s,_'%(time) )
        else:
            print('-,%s,%s'%(time, ex_lite))
        a = statistic.show_csv()
        print('-,%s,k%s'%(time, ex_lite))
        if 'blade' in ex:
            statistic.show_csv0(a)
        else:
            statistic.show_csv10(a)
    else:
        statistic.show_single_detail()
        statistic.show_detail()


if __name__ == '__main__':
    pass
