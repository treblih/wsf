#!/usr/bin/env python

# a, b are both lists, [d, m, s]
# return seconds, a - b
def degree_minus(a, b):
    sec = a[2] - b[2]
    if sec < 0:
        a[1] -= 1
        sec += 60
    min = a[1] - b[1]
    if min < 0:
        a[0] -= 1
        min += 60
    deg = a[0] - b[0]
    return deg * 3600 + min * 60 + sec

def sec2point(sec, dir):
    if dir == 'N':
        step = 11.0
    elif dir == 'E':
        step = 13.0
    else:
        return -1
    # int / int = int; int / float = float
    return round(sec / step)

def point2sec(x, y):
    sec = x * 11 + y * 13


#a = [31, 32, 58]
#b = [30, 55, 40]
a = [120, 36, 10]
b = [119, 52, 32]

print degree_minus(b, a)
