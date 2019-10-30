from core.ctx import *
from core.skada import *
import copy
from core import env

def loglevel(level):
    if level == 0:
        logset(['rotation'])
    elif level == 1:
        logset(['rotation'])
    elif level == 2:
        logset(['buff', 'dmg', 'sp', 'rotation'])
    elif level == 3:
        logset(['all'])
    elif level == -1:
        logset(['rotation'])
    elif level == -2:
        logset([])
    elif level == -5:
        logset([])
        
def show_rotation():
    logcat_(['rotation'])

def show_log():
    logcat_()

def show_single_detail():
    count = {}
    setup = ''
    for i in logget():
        if i[2][0] == '_':
            continue
        if i[1] != 'rotation':
            if i[3] == 'setup' :
                setup = i[4]
            continue
        if i[3] in ['x1','x2','x3','x4','x5']:
            if i[3] not in count :
                count[i[3]] = 0
            count[i[3]] += 1
        if i[4] != None:
            if i[4] not in count :
                count[i[4]] = 0
            count[i[4]] += 1
    a = skada.sum(q=1)
    teamdps = a['_Faketeam']['dps']
    teambase = 0
    if 'team_dps' in env.root:
        teambase = env.root['team_dps']
        #print('fake_team_base: ',env.root['team_dps'])
    for i in a:
        if i[0] != '_':
            single = a[i]['dps']
            teampercent = '%.2f'%((teamdps/teambase-1)*100)
            teamboost = int((teamdps/teambase-1)*10000)
            total = single + teamboost
            print(
                '%s: %s (%s+%s(%s%%))'%(i, total, single, teamboost, teampercent)
                )
    print(setup)
    s = skada.get()
    for i in s:
        if i[0] != '_':
            s[i]['count'] = count
            for j in s[i]:
                print(i, j, s[i][j])


def show_detail():
    skada.sum()
    if 'team_dps' in env.root:
        print('fake_team_base: ',env.root['team_dps'])
    s = skada.get()
    for i in s:
        print(i, s[i])
        #if i[0] != '_':
        #    print(i, s[i])


def show_csv(q=0):
    line = ''
    t = 0
    total = 0
    team_base = env.root['team_dps']

    for i,v in skada._skada.items():
        if i[0] != '_':
            d = v['dps']

    s = skada.sum(q=1)
    for i, v in s.items():
        if i[0] != '_':
            total += v['dps']
            name = i
        else:
            t = v['dps']
            t = int((t/team_base-1)*10000)
            total += t 
    line += '%s,%s,'%(total, name)
    info = ''
    l = logget()
    for i in l:
        if i[1]=='info' and i[3]=='setup' and i[2][0]!='_':
            info = i[4]
    if 'range' in env.root:
        if env.root['range'] != {} :
            info += ';dpsrange:(%d~%d)'%( \
                        env.root['range']['dmin']+env.root['range']['bmin'],
                        env.root['range']['dmax']+env.root['range']['bmax'] )
    line+=info+','

    combo = 0
    fs = 0
    s1 = 0
    s2 = 0
    s3 = 0
    dd = copy.copy(d)
    for i in dd:
        v = d[i]
        if i[0] == 'x':
            combo += v
            del(d[i])
    if 'fs' in d:
        fs = d['fs']
        del(d['fs'])
    if 's1' in d:
        s1 = d['s1']
        del(d['s1'])
    if 's2' in d:
        s2 = d['s2']
        del(d['s2'])
    if 's3' in d:
        s3 = d['s3']
        del(d['s3'])
    tb = t

    line += 'attack:%s,force_strike:%s,skill_1:%s,skill_2:%s,skill_3:%s,team_buff:%s'%(combo, fs, s1, s2, s3, tb)
    for i in d:
        line += ',%s:%s'%(i, d[i])

    if not q:
        print(line)
    return [total, name, info, combo, fs, s1, s2, s3, tb, d]

def show_csv0(a):
    d = a[9]
    line = '%s,%s,%s,'%(a[0],a[1],a[2])
    line += 'attack:%s,force_strike:%s,skill_1:%s,skill_2:%s,skill_3:%s,team_buff:%s'%(a[3],a[4],a[5],a[6],a[7],a[8])
    for i in d:
        line += ',%s:%s'%(i, d[i] )
    print(line)
    
def show_csv10(a):
    d = a[9]
    a[0] = int(a[0]*1.1)
    for i in range(3, 9):
        a[i] = int(a[i]*1.1)

    line = '%s,%s,%s,'%(a[0],a[1],a[2])
    line += 'attack:%s,force_strike:%s,skill_1:%s,skill_2:%s,skill_3:%s,team_buff:%s'%(a[3],a[4],a[5],a[6],a[7],a[8])
    for i in d:
        line += ',%s:%s'%(i, int(d[i]*1.1) )
    print(line)
    
