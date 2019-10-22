import __init__
from core.characterbase import *
from core.targetbase import *
from core.ctx import *

stage = {}
stage['1p'] = None
stage['2p'] = None
stage['3p'] = None
stage['4p'] = None
stage['target'] = None


root = {
 '1p.name'    : 'Elisanne'
,'1p.slot.a1' : 'BB'
,'1p.slot.a2' : 'JotS'
,'2p.name'    : 'Addis'
,'2p.slot.d'  : 'Vayu'
,'target.name': 'dummy'
,'ex' :['blade','wand']
,'duration' : 120
,'sample' : 1
}

def _run():
    global root
    rootconf = root
    time = root['duration']
    c = Conf()
    c(rootconf)
    conf = c.get
    p = {'1p':None, '2p':None, '3p':None, '4p':None}
    for i in p:
        if i in conf:
            name = conf[i]['name']
            p[i] = name
            __import__('character.'+name.lower())
    tname = conf['target']['name']
    __import__('target.'+conf['target']['name'])
    cclass = Character.get_sub()
    target = Target.get_sub()[tname]()
    target.init()
    stage['target'] = target

    cs = {'1p':None, '2p':None, '3p':None, '4p':None}
    for i in cs:
        cname = p[i]
        if cname != None:
            c = cclass[cname](conf)
            cs[i] = c
            c.tar(target)
            if c.ex not in conf['ex']:
                conf['ex'].append(c.ex)
            stage[i] = c
    for i in cs:
        c = cs[i]
        if c != None:
            c.init( conf[i] )
    Timer.run(time)
    return conf

dmax = {}
dmin = {}
def run():
    import random
    global root
    global dmax
    global dmin
    if root['sample'] > 1:
        logset([])
        random.seed(0)

    conf = Conf()(root).get
    p = {'1p':None, '2p':None, '3p':None, '4p':None}
    for i in p:
        if i in conf:
            name = conf[i]['name']
            p[i] = name

    results = {}
    lastresult = {}
    for i in p:
        if p[i] != None:
            #results[p[i]] = []
            lastresult[p[i]] = 0
            dmax[p[i]] = 0
            dmin[p[i]] = -1
    for i in range(root['sample']):
        ctx = Ctx()
        _run()
        r = skada.sum(q=1)
        for i in r:
            d = r[i]['dmg']-lastresult[i]
            #results[i].append(d)
            lastresult[i] = r[i]['dmg']
            if d > dmax[i]:
                dmax[i] = d
            if d < dmin[i] or dmin[i]==-1:
                dmin[i] = d
    if root['sample'] > 1:
        root['range'] = {'min':dmin, 'max':dmax}
        root['dsum'] = r
    else:
        root['range'] = {}
        root['dsum'] = r
    return ctx

        


if __name__ == '__main__':
    logset(['rotation','buff'])
    run()
    logcat()
    print('1-----------')
    skada.div(root['duration'], root['sample'])
    print('2-----------')
    print(dmax)
    print(dmin)
    d = skada.sum(q=1)
    for i in d:
        print(i, d[i]['dmg'])
    print('3-----------')
    print(skada._skada)
