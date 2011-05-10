#!/usr/bin/env python

import os
import sys
import glob

if __name__ == '__main__':
    os.chdir('/home/hask/FVCOM')

    #filename = 1
    #try:
        #fd = open('/media/sda6/CONCENTRATION.DAT', 'r')
    #except IOError, e:
        #print '%s' % e
        #sys.exit(1)
    #while 1:
        #try:
            #fd_w = open(str(filename) + '.dat', 'w')
        #except IOError:
            #print 'Opening %d for writing' % filename
            #sys.exit(1)
        #i = 0
        #while i <> 200:
            #line = fd.readline()
            #if not line:
                #fd_w.close()
                #sys.exit(0)
            #fd_w.write(line)
            #i += 1
        #fd_w.close()
        #filename += 1

    for dat in glob.glob('*.dat'):
        index = os.path.splitext(dat)[0]
        try:
            fd = open(dat, 'r')
            fd_w = open(index + '.plot', 'w')
        except IOError, e:
            print e
        y = 199
        line = fd.readline()
        while line:
            for x, num in enumerate(line.split()):
                newline = str(x) + ' ' + str(y) + ' ' + num + '\n'
                fd_w.write(newline)
            fd_w.write('\n')
            y -= 1
            line = fd.readline()
        fd.close()
        fd_w.close()
