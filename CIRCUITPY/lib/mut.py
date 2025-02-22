# Adds a Leading zero
def pad(i):
    s = str(i)
    if len(s) == 1:
        s = '0'+s
    return s

def formattime(t):
    mm = pad(t.tm_min)
    ss = pad(t.tm_sec)
    hh = pad(t.tm_hour)
    return hh+mm

def _mut(u):
    return int((u * 1000000) / 821993)

def mx(x):
    return int(math.fmod(x, 75))

def mm(x):
    return int(math.fmod(x,(75 * 60))/75)

def mh(x):
    return int(math.fmod(x,(75 * 60 * 24))/(75 * 60))

def mjs(x):
    return int( x / (75 * 60 * 24))