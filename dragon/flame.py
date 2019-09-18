import __init__
from dragon.dragonbase import *


class Cerberus(Dragon):
    ele = 'flame'
    atk = 127
    a = [('atk',0.60)]
Cerb = Cerberus


class Sakuya(Dragon):
    ele = 'flame'
    atk = 127
    a = [('atk', 0.20),
         ( 'sd', 0.90)]


class Arctos(Dragon):
    ele = 'flame'
    atk = 121
    a = [('atk', 0.45),
         ( 'cd', 0.55)]


class Apollo(Dragon):
    ele = 'flame'
    atk = 126
    a = [('atk', 0.50),
         ('k', 0.20, 'burn')]
