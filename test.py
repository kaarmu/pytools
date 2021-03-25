
from binary import floorpow2


def from_value(val, nbits=None):    
    il = []
    v = abs(val)
    while v:
        i = floorpow2(v)
        il.append(i)
        input([v, 2**i, i])
        v -= 2**i
    m = max(il) + 1
    bl = [False] * m
    for i in il:
        bl[i] = True



if __name__ == '__main__':
    print(from_value(300))