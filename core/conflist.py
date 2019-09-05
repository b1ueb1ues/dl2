from ctx import *

root = Conf()

# root
root._1p = character # conf character
    character.star     # int 
    character.ele      # string element
    character.wt       # string weapon type
    character.atk      # int atk
    character.a1       # tuple ability (prefix, affix, value)
    character.a2       # tuple ability (prefix, affix, value)
    character.a3       # tuple ability (prefix, affix, value)
    character.a        # conf abilities (conbined weapon, wp, character, auto generate)
    character.ex       # string co-ability
    character.slot = slot     # conf slot
        slot.w   # string weapon
        slot.d   # string dragon
        slot.a1  # string amulet
        slot.a2  # string amulet

root._2p    # conf character
root._3p    # conf character
root._4p    # conf character

root.target      # conf dummy
    target.hp   # int 
    target.od   # int
    target.bk   # int 
    target.def_ # int

root.ex # list ex

# player
.

# target
conf.hp # number
conf.od  # number
conf.bk # number
conf.def_ # number
