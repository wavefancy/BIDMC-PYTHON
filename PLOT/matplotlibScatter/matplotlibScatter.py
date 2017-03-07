#!/usr/bin/env python3
"""

    Plot scatter plot by matplotlib.
    @Author: wavefancy@gmail.com

    Usage:
        matplotlibScatter.py -o filename -x xtitle -y ytitle [--qqab]
        matplotlibScatter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin.
        2. See example by -f.

    Options:
        -y ytitle     Title for y.
        -x xtitle     Title for x.
        -o filename   Output file name: output.png[|.pdf.jpg].
        --qqab        Add qqplot abline, slop 1, default False.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mt
import matplotlib.gridspec as gridspec
import copy
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

class Parameters():
    # colors = ['#01759E','#0285FF','#0091C2','#4F1AB7']
    colors = ['#004586','#FF420E','#FFD320','#60A229', '#7E0021','#83CAFF']
    Canvas_width = 6.83	#inches
    Canvas_height = 6.83
    Fig_width = 0.87
    Fig_height = 0.80
    Bottom_margin = 0.15
    Left_margin = 0.09 # percentage.

    DPI = 300
    Output_format = 'png'

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    outFile = args['-o'] #+ '.png'
    xlabel = args['-x']
    ylabel = args['-y']
    qqabline = False
    if args['--qqab']:
        qqabline = True
    #-----------------------------------

    p = Parameters()

    fig = plt.figure(figsize=(Parameters.Canvas_width,Parameters.Canvas_height), dpi=Parameters.DPI)
    gs = gridspec.GridSpec(1,1) #1 row, 2 columns
    #gs.update(left=p.Left_margin,bottom=p.Bottom_margin, right=p.Left_margin + p.Fig_width,wspace=0.25)
    ax1 = plt.subplot(gs[0,0])
    #ax2 = plt.subplot(gs[0,1])

    xx = []
    yy = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = float(ss[0])
                y = float(ss[1])

                xx.append(x)
                yy.append(y)
            except ValueError:
                sys.stderr.write('WARN: parse value error (skipped):%s\n'%(line))

    mm = max(max(xx),max(yy))
    mi = min(min(xx),min(yy))

    ax1.plot([mi,mm],[mi,mm],color='red')
    ax1.scatter(xx,yy,color='grey')

    fontSize = 12
    ax1.tick_params(axis='x', which='major', labelsize=fontSize)
    ax1.tick_params(axis='y', which='major', labelsize=fontSize)

    ax1.set_xlabel(xlabel,**{'fontsize':fontSize})
    ax1.set_ylabel(ylabel,**{'fontsize':fontSize})

    fig.tight_layout()
    fig.savefig(outFile)
