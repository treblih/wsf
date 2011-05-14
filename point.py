#!/usr/bin/env python

import os
import sys

def point(x, y, fvcom_dir):
    x_t = str(x)
    y_t = str(y)
    i = 1
    #if x >= 200 or y >= 200:
        #print 'Out of range'
        #sys.exit(1)
    try:
        fd_w = open(fvcom_dir + x_t + '_' + y_t + '.plot', 'w')
    except IOError, e:
        print e
    # 200 + empty line = 201
    target_bak = y * 201 + x    
    while i <= 140:
        try:
            fd = open(str(i) + '.plot', 'r')
        except IOError, e:
            print e
        target = target_bak
        while target:
            line = fd.readline()
            target -= 1
        fd_w.write(str(i) + ' ' + line[len(x_t) + len(y_t) + 2:])
        fd.close()

        #line = fd.readline()
        #while line:
            #if line.startswith(x + ' ' + y + ' '):
                #fd_w.write(str(i) + ' ' + line[len(x) + len(y) + 2:])
                #fd.close()
                #break
            #line = fd.readline()
        i += 1
    fd_w.close()
