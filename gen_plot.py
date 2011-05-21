#!/usr/bin/env python
#-*-coding:utf-8-*-

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
    from deglist import *
    def point2degtext(n, deglist, dir):
        if dir == 'N':
            deglist = deglist_plus(sec2deglist(n * 11), deglist)
        elif dir == 'E':
            deglist = deglist_plus(sec2deglist(n * 13), deglist)
        else :
            return ''
        return str(deglist[0]) + '°' + str(deglist[1]) + '′' + str(deglist[2]) + '″'

    os.chdir('/home/hask/FVCOM/.concentration/')
    i = 1
    g = Gnuplot.Gnuplot()
    g('set view map')
    g('set grid')
    g('set samples 200,200')
    g('set isosamples 200,200')
    g("set cblabel 'mg/L'")
    # 0-199, so '200' 200 won't appear
    N = [30, 55, 40]
    E = [119, 52, 32]
    strs = map(lambda x: point2degtext(x, N, 'N'), range(20, 181, 40))
    g('set xtics offset 0, -1')
    g('set xtics rotate by 270')
    g("set xtics ('0' 0, '" + strs[0] + "' 20, '40' 40, '" + strs[1] + "' 60, \
                  '80' 80, '" + strs[2] + "' 100, '120' 120, '" + strs[3] + "' 140, \
                  '160' 160, '" + strs[4] + "' 180, '200' 199)")
    strs = map(lambda y: point2degtext(y, E, 'E'), range(20, 181, 40))
    g("set ytics ('0' 0, '" + strs[0] + "' 20, '40' 40, '" + strs[1] + "' 60, \
                  '80' 80, '" + strs[2] + "' 100, '120' 120, '" + strs[3] + "' 140, \
                  '160' 160, '" + strs[4] + "' 180, '200' 199)")

    g('set term png size 600,600')

    g("set output '100.png'")
    g("splot '100.dat' matrix with image")
    #while i <= 140:
        #plot = str(i) + '.plot'
        #png = str(i) + '.png'
        #g('set output \'' + png + '\'')
        #g.splot(Gnuplot.File(plot))
        #i += 1

