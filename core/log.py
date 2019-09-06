import __init__
from core.timer import *


_g_log = []
_g_verbose = []


class Log(object):
    @classmethod
    def init(cls, l=None):
        global _g_log
        if not l:
            l = {}
            l['log'] = []
        _g_log = l['log']
        return l
    

class Logger(object):
    def __init__(this, src, dst):
        this.src = src
        this.dst = dst

    def __call__(this, t, name, amount=None, misc=''):
        log(t, name, amount, misc, this.src, this.dst)


def log(t, name, amount=None, misc='', src=None, dst=None):
    global _g_verbose
    if t in _g_verbose:
        _g_log.append([now(), t, name, amount, misc, src, dst])


def logset(v):
    global _g_verbose
    if type(v) == list:
        _g_verbose = v
    elif type(v) == str:
        _g_verbose.append(v)


def __catline(i):
    src = i[5]
    dst = i[6]
    if src!=None and dst==None:
        srcdst = '%s->   \t'%(src, dst)
    elif src!=None and dst!=None:
        srcdst = '%s->%s\t'%(src, dst)
    elif src==None and dst==None:
        srcdst = '%s->%s\t'%(src, dst)
    elif src==None and dst!=None:
        srcdst = '   ->%s\t'%(src, dst)

    if i[3] == None:
        print("%-7.3f %s: %-8s, %-16s,             , %s"%(i[0],srcdst,i[1],i[2],i[4]))
    elif type(i[3]) == float:
        n = "%s"%(int(i[3]))
        f = i[3] - int(i[3])
        if f >= 1:
            f = 0
        n += "%-.3f"%(f)
        print("%-7.3f %s->%s: %-8s, %-16s, %-12s, %s"%(i[0],i[5],i[6],i[1],i[2],n,i[4]))
    elif type(i[3]) == int:
        print("%-7.3f %s->%s: %-8s, %-16s, %-12d, %s"%(i[0],i[5],i[6],i[1],i[2],i[3],i[4]))
    else:
        print("%-7.3f %s->%s: %-8s, %-16s, %-12s, %s"%(i[0],i[5],i[6],i[1],i[2],i[3],i[4]))


def __saveline(fw, i):
    if i[3] == None:
        fw.write("%-7.3f,%s->%s, %-8s, %-16s,             , %s\n"%(i[0],i[5],i[6],i[1],i[2],i[4]))
    elif type(i[3]) == float:
        n = "%s"%(int(i[3]))
        f = i[3] - int(i[3])
        if f >= 1:
            f = 0
        n += "%-.3f"%(f)
        fw.write("%-7.3f,%s->%s, %-8s, %-16s, %-12s, %s\n"%(i[0],i[5],i[6],i[1],i[2],n,i[4]))
    elif type(i[3]) == int:
        fw.write("%-7.3f,%s->%s, %-8s, %-16s, %-12d, %s\n"%(i[0],i[5],i[6],i[1],i[2],i[3],i[4]))
    else:
        fw.write("%-7.3f,%s->%s, %-8s, %-16s, %-12s, %s\n"%(i[0],i[5],i[6],i[1],i[2],i[3],i[4]))


def logsave(logname):
    log = _g_log
    f = open(logname,'w')
        
    for i in log:
        __saveline(f, i)


def logcat(filter=None):
    log = _g_log
        
    if filter == None :
        for i in log:
            __catline(i)
    else :
        for i in log:
            for j in filter :
                if i[1] == j:
                    __catline(i)


def logget():
    global _g_log
    return _g_log

if __name__ == '__main__':
    logset('act')
    logset('debug')
    l = Logger('src','dst')
    l('act','test')
    l('debug','int', 2)
    l('debug','float', 2.1)
    logcat()
    logsave('log.txt')
