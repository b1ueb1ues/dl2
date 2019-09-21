import test
from core import benchmark


class w():
    def __init__(this):
        this.get = {}

bar = 0

a = w()
a.get['a'] = 0
def foo():
    global a
    for i in range(100000000):
        a.get['a'] += 1


benchmark.run(foo)
