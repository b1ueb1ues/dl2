import __init__
from core.characterbase import *
from core.conf import *
from character.mikoto import *

stage = {}
stage['1p'] = None
stage['2p'] = None
stage['3p'] = None
stage['4p'] = None
stage['target'] = None


root = {
 '1p.name'   : 'Mikoto'
,'1p.slot.d' : 'Cerb'
,'2p.name'   : 'Elisanne'
,'target'    : 'dummy'
}

def run(rootconf, time):
    c = Conf()
    c(rootconf)
    conf = c.get
    if '1p' in conf:
        name = conf['1p']['name']
        __import__('character.'+name)
        print(Character.get_sub())


if __name__ == '__main__':
    run(root, 0)
