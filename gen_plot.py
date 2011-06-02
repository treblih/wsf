#!/usr/bin/env python
#-*-coding:utf-8-*-

import sys, os
from numpy import *
import Gnuplot, Gnuplot.funcutils

def plot(dat, png, e, n):
    # /home/hask/FVCOM/.concentration/100_100.dat ->
    # 100_100.dat -> 100_100  -> [100, 100]
    x, y = os.path.split(dat)[1].split('.')[0].split('_')
    e = str(e[0]) + '°' + str(e[1]) + '′' + str(e[2]) + '″'
    n = str(n[0]) + '°' + str(n[1]) + '′' + str(n[2]) + '″'
    g = Gnuplot.Gnuplot()
    g('set grid')
    g('set term png size 800,500')
    g('set output "' + png + '"')
    #g('set style data lines')
    g('unset key')
    g('set xdata time')
    g('set timefmt "%Y-%b-%d/%H:%M')
    g('set format x "%d/%H"')
    g('set xlabel "October - day/hour"')
    g('set ylabel "mg/L"')
    g('set title "(' + x + ', ' + y + ')   N ' + n + '   E ' + e + '"')
    g('plot "' + dat + '" u 1:2 w l')
    #g.plot(Gnuplot.File(dat))

def datestr(day, hour):
    if hour < 10:
        hourtext = '0' + str(hour) + ':00'
        hour += 1
    elif hour < 24:
        hourtext = str(hour) + ':00'
        hour += 1
    else : # hour == 24
        day += 1
        hourtext = '00:00'
        hour = 1
    return [day, hour, '2010-Oct-' + str(day) + '/' + hourtext]

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
    periods = 116

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

    day = 1
    hour = 5
    def dat2png(i):
        global day, hour
        dat = str(i) + '.dat'
        png = str(i) + '.png'
        day, hour, datetime = datestr(day, hour)
        g("set title '" + datetime + "'")
        g("set output '" + png + "'")
        g("splot '" + dat + "' matrix with image")
    map(dat2png, range(1, periods + 1))
