#!/usr/bin/env python

import sys, os
from numpy import *
import Gnuplot, Gnuplot.funcutils

os.chdir('/home/hask/FVCOM')
i = 1
g = Gnuplot.Gnuplot()
g('set pm3d map')
#g('set hidden3d')
g('set samples 200,200')
g('set isosamples 200,200')
g('set term png size 500,500')

while i <= 140:
    plot = str(i) + '.plot'
    png = str(i) + '.png'
    g('set output \'' + png + '\'')
    g.splot(Gnuplot.File(plot))
    i += 1
