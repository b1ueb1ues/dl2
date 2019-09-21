import test
from core import benchmark

r = 0
a = {}
a['a'] = 1
def foo():
    global a
    global r
    if a['a']:
        r+=1


benchmark.run(foo, 10000000)
print(r)
