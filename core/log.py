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


def log(t, name, amount=None, misc=''):
    global _g_verbose
    if t in _g_verbose:
        _g_log.append([now(), t, name, amount, misc])


def logset(v):
    global _g_verbose
    if type(v) == list:
        _g_verbose = v
    elif type(v) == str:
        _g_verbose.append(v)



def __logline(i):
    if i[3] == None:
        print("%-8.3f: %-8s, %-16s,             , %s"%(i[0],i[1],i[2],i[4]))
    elif type(i[3]) == float:
        n = "%s"%(int(i[3]))
        f = i[3] - int(i[3])
        if f >= 1:
            f = 0
        n += "%-.3f"%(f)
        print("%-8.3f: %-8s, %-16s, %-12s, %s"%(i[0],i[1],i[2],n,i[4]))
    elif type(i[3]) == int:
        print("%-8.3f: %-8s, %-16s, %-12d, %s"%(i[0],i[1],i[2],i[3],i[4]))
    else:
        print("%-8.3f: %-8s, %-16s, %-12s, %s"%(i[0],i[1],i[2],i[3],i[4]))


def logcat(filter=None):
    log = _g_log
        
    if filter == None :
        for i in log:
            __logline(i)
    else :
        for i in log:
            for j in filter :
                if i[1] == j:
                    __logline(i)


def logget():
    global _g_log
    return _g_log
