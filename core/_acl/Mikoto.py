
def cancel(this, e):
    if e.hit == e.last:
        x = e.idx
    else:
        x = e.idx*10+e.hit
#   ----------------------------------
    if x==5 :
        if this.s1():
            return 's1'
    if x==5 :
        if this.s2():
            return 's2'
    if x==5 :
        if this.s3():
            return 's3'
    if x==5 :
        if this.fsf():
            return 'fsf'
    return 0

def other(this, e):
    doing = this.Action.doing.name
#   ----------------------------------
    if this.s3():
        return 's3'
    return 0
