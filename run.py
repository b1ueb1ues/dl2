from core.ctx import *
from core import env
from core.skada import *

def solo(name, duration=120, ex=['wand','blade']):
    env.root = {
     '1p.name'     : name
#,'2p.name'     : 'Elisanne'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 1
    }
    env.run()
    Skada.div(env.root['duration'], env.root['sample'])

def solo_range(name, duration=120, ex=['wand','blade']):
    env.root = {
     '1p.name'     : name
#,'2p.name'     : 'Elisanne'
    ,'target.name' : 'dummy'
    ,'ex'          : ex
    ,'duration'    : duration
    ,'sample'      : 256
    }
    env.run()
    Skada.div(env.root['duration'], env.root['sample'])

def team(conf):
    env.root = conf
    env.run()
    Skada.div(env.root['duration'],env.root['sample'])

def this_character(time=120, ex=['wand', 'blade'], verbose=0, mass=0):
    import sys
    from core import characterbase as cb
    import statistic

    argv = sys.argv
    if len(argv) >= 2:
        verbose = argv[1]
    if len(argv) >= 3:
        time = argv[2]
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
    if mass:
        for i in cs:
            solo_range(i, time, ex) 
    else:
        for i in cs:
            solo(i, time, ex) 

    #statistic.show_rotation()
    #statistic.show_detail()
    statistic.show_csv()


if __name__ == '__main__':
    root = {
     '1p.name'     : 'Mikoto'
    ,'2p.name'     : 'Elisanne'
    ,'target.name' : 'dummy'
    ,'ex'          : ['wand','blade']
    ,'duration'    : 120
    ,'sample'      : 1
    }
    team(root)



