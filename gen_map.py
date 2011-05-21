#!/usr/bin/env python

import sys, os
from numpy import *
import Gnuplot, Gnuplot.funcutils

def plot(x, y, plot, png):
    g = Gnuplot.Gnuplot()
    g('set grid')
    g('set term png size 800,500')
    g('set output \'' + png + '\'')
    g('set style data lines')
    g.plot(Gnuplot.File(plot))

if __name__ == '__main__':
    os.chdir('/home/hask/FVCOM/.concentration/')
    i = 1
    g = Gnuplot.Gnuplot()
    g('set view map')
    g('set grid')
    g('set samples 200,200')
    g('set isosamples 200,200')
    g("set cblabel 'mg/L'")
    # 0-199, so '200' 200 won't appear
    g("set xtics ('0' 0, '20' 20, '40' 40, '60' 60, '80' 80, \
      '100' 100, '120' 120, '140' 140, '160' 160, '180' 180)")
    g("set ytics ('0' 0, '20' 20, '40' 40, '60' 60, '80' 80, \
      '100' 100, '120' 120, '140' 140, '160' 160, '180' 180)")
    g('set term png size 600,600')
    g("set output '100.png'")
    g("splot '100.dat' matrix with image")
    #while i <= 140:
        #plot = str(i) + '.plot'
        #png = str(i) + '.png'
        #g('set output \'' + png + '\'')
        #g.splot(Gnuplot.File(plot))
        #i += 1
