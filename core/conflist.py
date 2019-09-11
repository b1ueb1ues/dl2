# root
root._1p = character # conf character
    character.slot = slot  # conf slot
        slot.w   # string weapon
        slot.d   # string dragon
        slot.a1  # string amulet
        slot.a2  # string amulet

root._2p = character   # conf character
root._3p = character   # conf character
root._4p = character   # conf character

root.target = dummy    # conf dummy
    target.hp      # int 
    target.od      # int base_od
    target.bk      # int base_bk
    target.od_def  # float rate
    target.bk_def  # float rate
    target.bk_time # int
    target.def_    # int
    target.ele     # string element

root.ex # list ex


character
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
    character.s1 = skill  # skill
        s1.sp        # int sp_max
        s1.startup   # int startup frames
        s1.recovery  # int recovery frames
        s1.on_start  # function
        s1.on_end    # function
        s1.proc      # function s1 active proc
        s1.hit       # dict {timing: conf hitattr}
        s1.hitattr = hitattr  # conf 
            hitattr.coef   # float damage coefficent
            hitattr.type   # string type
            hitattr.to_od  # float damage rate to od+ 
            hitattr.to_bk  # float damage rate to od-
            hitattr.killer # {string type: float value} killer state
        s1.hitattr2 = hitattr  # conf 
    character.s2 = skill  # skill
    character.s3 = skill  # skill
