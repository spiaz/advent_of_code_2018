#%%
from collections import defaultdict

with open("input.txt", 'r') as ifile:
    lines = ifile.readlines()

seq  = [int(l.strip()) for l in lines]

def find_freq(changes):
    return sum(changes)

find_freq(seq)
#%%
def calibrate(changes):
    d = defaultdict(int)
    d[0] += 1 
    is_repeated = False
    f = 0
    while True:
        for c in changes:
            f += c
            d[f] += 1
            if d[f] > 1:
                return f

#%%
assert calibrate([+1, -1]) == 0
assert calibrate([+3, +3, +4, -2, -4]) == 10
assert calibrate([-6, +3, +8, +5, -6]) == 5
assert calibrate ([+7, +7, -2, -7, -4]) == 14

#%%

calibrate(seq)


#%%
