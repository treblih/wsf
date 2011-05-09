#!/usr/bin/env python

import os

if __name__ == '__main__':
    os.chdir('/home/hask/FVCOM')
    x = '100'
    y = '100'
    i = 1
    try:
        fd_w = open(x + '_' + y + '.plot', 'w')
    except IOError, e:
        print e
    while i <= 140:
        try:
            fd = open(str(i) + '.plot', 'r')
        except IOError, e:
            print e
        line = fd.readline()
        while line:
            line = fd.readline()
            if line.startswith(x + ' ' + y + ' '):
                fd_w.write(str(i) + ' ' + line[len(x) + len(y) + 2:])
                fd.close()
                break
        i += 1
    fd_w.close()
