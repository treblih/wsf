#!/usr/bin/env python

import os
import sys
import glob

if __name__ == '__main__':
    if not os.path.isdir('/home/hask/FVCOM/.concentration'):
        os.mkdir('/home/hask/FVCOM/.concentration')
    os.chdir('/home/hask/FVCOM/.concentration')

    filename = 1
    tmp = []
    try:
        fd = open('/media/sda6/CONCENTRATION.DAT', 'r')
    except IOError, e:
        print e
        sys.exit(1)
    while filename < 141:
        try:
            fd_w = open(str(filename) + '.dat', 'w')
        except IOError, e:
            print e
            sys.exit(1)
        i = 0
        while i < 200:
            tmp.append(fd.readline())
            i += 1
        while i > 0:
            fd_w.write(tmp.pop())
            i -= 1
        fd_w.close()
        filename += 1
