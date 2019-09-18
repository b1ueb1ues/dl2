from conf import *

c = {
        'conf.s1.attr.1.coef' : 2
    }

a = Conf(c)


print(a.conf.s1.attr['1'])
