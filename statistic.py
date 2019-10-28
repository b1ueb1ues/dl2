from core.ctx import *
from core.skada import *
import copy
from core import env

def loglevel(level):
    if level == 0:
        logset([])
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
        
def show_rotation():
    logcat(['rotation'])

def show_log():
    logcat()

def show_single_detail():
    a = skada.sum(q=1)
    teamdps = a['_Faketeam']['dmg']
    teambase = 0
    if 'team_dps' in env.root:
        teambase = env.root['team_dps']
        #print('fake_team_base: ',env.root['team_dps'])
    for i in a:
        if i[0] != '_':
            single = a[i]['dmg']
            teampercent = '%.2f'%((teamdps/teambase-1)*100)
            teamboost = int((teamdps/teambase-1)*10000)
            total = single + teamboost
            print(
                '%s: %s (%s+%s(%s%%))'%(i, total, single, teamboost, teampercent)
                )
    s = skada.get()
    for i in s:
        if i[0] != '_':
            print(i, s[i])

def show_detail():
    skada.sum()
    if 'team_dps' in env.root:
        print('fake_team_base: ',env.root['team_dps'])
    s = skada.get()
    for i in s:
        if i[0] != '_':
            print(i, s[i])

def show_csv():
    line = ''
    t = 0
    total = 0
    team_base = env.root['team_dps']

    for i,v in skada._skada.items():
        if i[0] != '_':
            d = v['dmg']

    s = skada.sum(q=1)
    for i, v in s.items():
        if i[0] != '_':
            total += v['dmg']
            name = i
        else:
            t = v['dmg']
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

    print(line)


def show_csv_10():
    line = ''
    t = 0
    total = 0
    team_base = env.root['team_dps']

    for i,v in skada._skada.items():
        if i[0] != '_':
            d = v['dmg']

    for i, v in env.root['dsum'].items():
        if i[0] != '_':
            total += int( env.root['dsum'][i]['dmg'] \
                    / env.root['sample'] / env.root['duration'] )
            name = i
        else:
            t = v['dmg'] / env.root['sample'] / env.root['duration']
            t = int((t/team_base-1)*10000)
            total += t 
    line += '%s,%s,'%( int(total*1.1) , name)

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

    line += 'attack:%s,force_strike:%s,skill_1:%s,skill_2:%s,skill_3:%s,team_buff:%s'%(int(1.1*combo), int(1.1*fs), int(1.1*s1), int(1.1*s2), int(1.1*s3), int(1.1*tb))
    for i in d:
        line += ',%s:%s'%(i, int(1.1*d[i]))

    print(line)

