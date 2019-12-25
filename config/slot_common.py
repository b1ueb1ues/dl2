
def get(ele, wt, stars=None):
    slot = {}

    if ele == 'flame':
        slot['d'] = 'Sakuya'
    elif ele == 'water':
        slot['d'] = 'Siren'
    elif ele == 'wind':
        slot['d'] = 'Vayu'
    elif ele == 'light':
        slot['d'] = 'Cupid'
    elif ele == 'shadow':
        slot['d'] = 'Shinobi'

    slot['a'] = 'RR+BN'

    if wt == 'sword':
        slot['a'] = 'RR+FP'
    if wt == 'blade':
        slot['a'] = 'RR+BN'
    if wt == 'dagger':
        if ele == 'water':
            slot['a'] = 'TB+The_Prince_of_Dragonyule'
        else:
            slot['a'] = 'TB+LC'
    if wt == 'axe': 
        slot['a'] = 'KFM+FitF'
    if wt == 'lance': 
        slot['a'] = 'RR+BN'
    if wt == 'wand': 
        slot['a'] = 'RR+FoG'
    if wt == 'bow':
        slot['a'] = 'RR+FoG'
    
    slot['w'] = 'c534_'+ele
    return slot

