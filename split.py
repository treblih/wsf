#!/usr/bin/env python

#import Gnuplot, Gnuplot.funcutils
#from numpy import *

#g = Gnuplot.Gnuplot()
#x = arange(5, dtype='float_')
#g.plot(Gnuplot.File('~/ibm.dat'))
#raw_input('nihao)

# Error Handling Example With Shutdown and File-Like Objects - Chapter 2

#import sys, urllib2

#req = urllib2.Request(sys.argv[1])
#fd = urllib2.urlopen(req)
#print "Retrieved", fd.geturl()
#info = fd.info()
#for key, value in info.items():
    #print "%s = %s" % (key, value)

import sys, os

if __name__ == '__main__':
    filename = 1
    try:
        fd = open('/media/sda6/CONCENTRATION.DAT', 'r')
    except IOError, e:
        print '%s' % e
        sys.exit(1)
    while 1:
        try:
            fd_w = open('/home/hask/FVCOM/' + str(filename) + '.dat', 'w')
        except IOError:
            print 'Opening %d for writing' % filename
            sys.exit(1)
        i = 0
        while i <> 200:
            line = fd.readline()
            if not line:
                fd_w.close()
                sys.exit(0)
            fd_w.write(line)
            i += 1
        fd_w.close()
        filename += 1
