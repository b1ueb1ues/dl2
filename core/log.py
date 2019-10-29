import __init__
from core.timer import *


_g_log = []
_g_verbose = []


def Logger(t):
    global _g_verbose
    if t in _g_verbose or 'all' in _g_verbose:
        def log(host, name, amount=None, misc=''):
            global _g_log
            _g_log.append([now(), t, host, name, amount, misc])
        return log
    else:
        return None


class Log(object):
    @classmethod
    def init(cls, l=None):
        global _g_log
        if not l:
            l = {}
            l['log'] = []
        _g_log = l['log']
        return l
    

def verbose(t):
    global _g_verbose
    if t in _g_verbose:
        return True
    else:
        return False


def log(t, host, name, amount=None, misc=''):
    global _g_verbose
    if t in _g_verbose or 'all' in _g_verbose:
        _g_log.append([now(), t, host, name, amount, misc])


def log_(t, host, name, amount=None, misc=''):
    global _g_verbose
    _g_log.append([now(), t, host, name, amount, misc])


def logset(v):
    global _g_verbose
    if type(v) == list:
        _g_verbose = v
    elif type(v) == str:
        _g_verbose.append(v)


def __catline(i):
    if i[4] == None:
        print("%-7.3f: %-8s,%s, %-16s,                 , %s"%(i[0],i[1],i[2],i[3],i[5]))
    elif type(i[4]) == float:
        n = "%s"%(int(i[4]))
        f = i[4] - int(i[4])
        if f >= 1:
            f = 0
        n += ("%-.3f"%(f))[1:]
        print("%-7.3f: %-8s, %s, %-16s, %-16s, %s"%(i[0],i[1],i[2],i[3],n,i[5]))
    elif type(i[3]) == int:
        print("%-7.3f: %-8s, %s, %-16s, %-16d, %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    else:
        print("%-7.3f: %-8s, %s, %-16s, %-16s, %s"%(i[0],i[1],i[2],i[3],i[4],i[5]))


def __saveline(fw, i):
    if i[4] == None:
        fw.write("%-7.3f, %-8s, %s, %-16s,                 , %s\n"%(i[0],i[1],i[2],i[3],i[5]))
    elif type(i[4]) == float:
        n = "%s"%(int(i[4]))
        f = i[4] - int(i[4])
        if f >= 1:
            f = 0
        n += ("%-.3f"%(f))[1:]
        fw.write("%-7.3f, %-8s, %s, %-16s, %-16s, %s\n"%(i[0],i[1],i[2],i[3],n,i[5]))
    elif type(i[3]) == int:
        fw.write("%-7.3f, %-8s, %s, %-16s, %-16d, %s\n"%(i[0],i[1],i[2],i[3],i[4],i[5]))
    else:
        fw.write("%-7.3f, %-8s, %s, %-16s, %-16s, %s\n"%(i[0],i[1],i[2],i[3],i[4],i[5]))


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
    logset('debug')
    ld = Logger('debug')
    lf = Logger('foo')
    if ld:
        ld('ld',100)
    if lf:
        lf('lf',100)
    
    #log('debug','name',1.0009)
    logcat()
    #logsave('log.txt')


