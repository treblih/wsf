#!/usr/bin/env python

import locale
# a, b are both lists, [d, m, s]
def deglist_minus(a, b):
    sec = a[2] - b[2]
    if sec < 0:
        a[1] -= 1
        sec += 60
    min = a[1] - b[1]
    if min < 0:
        a[0] -= 1
        min += 60
    deg = a[0] - b[0]
    return [deg, min, sec]

def deglist_plus(a, b):
    sec = a[2] + b[2]
    min = 0
    deg = 0
    if sec >= 60:
        sec -= 60
        min += 1
    min += (a[1] + b[1])
    if min >= 60:
        min -= 60
        deg += 1
    deg += (a[0] + b[0])
    return [deg, min, sec]

def deglist2sec(deglist):
    return deglist[0] * 3600 + \
           deglist[1] * 60 + deglist[2]

def sec2deglist(sec):
    deg, sec = divmod(sec, 3600)
    min, sec = divmod(sec, 60)
    return [deg, min, sec]



#def sec2point(sec, dir):
    #if dir == 'N':
        #step = 11.0
    #elif dir == 'E':
        #step = 13.0
    #else:
        #return -1
    ## int / int = int; int / float = float
    #return int(round(sec / step))

a = [31, 32, 58]
b = [30, 55, 40]
#a = [120, 36, 10]
#b = [119, 52, 32]

#c = deglist2sec(deglist_minus(a, b))
#d = deglist_plus(sec2deglist(c), b)
#print d[0], d[1], d[2]
#print sec2deglist()

#print  point2degtext(100, [30, 55, 40], 'N')
