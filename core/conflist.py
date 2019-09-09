from ctx import *

root = Conf()

# root
root._1p = character # conf character
    character.name     # string
    character.star     # int 
    character.ele      # string element
    character.wt       # string weapon type
    character.atk      # int base_attack
    character.a1       # tuple ability (prefix, affix, value)
    character.a2       # tuple ability (prefix, affix, value)
    character.a3       # tuple ability (prefix, affix, value)
    character.a        # conf abilities (conbined weapon, wp, character, \
                       #     auto generate)
    character.ex       # string co-ability
    character.slot = slot  # conf slot
        slot.w   # string weapon
        slot.d   # string dragon
        slot.a1  # string amulet
        slot.a2  # string amulet
    character.s1 = skill  # skill
        s1.hitattr   # dict {timing: coef}
        s1.sp        # int sp_max
        s1.startup   # int startup frames
        s1.recovery  # int recovery frames
        s1.on_start  # function
        s1.on_end    # function
        s1.proc      # function s1 active proc
        #s1.hit       # function s1 damage
    character.s2 = skill  # skill
    character.s3 = skill  # skill
    character.dc     # damage calculator (gen by Dmg_calc)

root._2p = character   # conf character
root._3p = character   # conf character
root._4p = character   # conf character

root.target = dummy    # conf dummy
    target.hp   # int 
    target.od   # int
    target.bk   # int 
    target.def_ # int
    target.ele  # string element

root.ex # list ex

