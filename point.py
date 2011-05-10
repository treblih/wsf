#!/usr/bin/env python

import os
import sys

if __name__ == '__main__':
    os.chdir('/home/hask/FVCOM')
    x_t = '100'
    y_t = '100'
    x = int(x_t)
    y = int(y_t)
    i = 1
    if x >= 200 or y >= 200:
        print 'Out of range'
        sys.exit(1)
    try:
        fd_w = open(x_t + '_' + y_t + '.plot', 'w')
    except IOError, e:
        print e
    while i <= 140:
        try:
            fd = open(str(i) + '.plot', 'r')
        except IOError, e:
            print e
        target = x * 200 + y
        #line = fd.readline()
        #while line:
            #if line.startswith(x + ' ' + y + ' '):
                #fd_w.write(str(i) + ' ' + line[len(x) + len(y) + 2:])
                #fd.close()
                #break
            #line = fd.readline()
        i += 1
    fd_w.close()
