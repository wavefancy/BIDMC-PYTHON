#!/usr/bin/env python

"""

    Intepolate desired point by scipy univariate cubic intepolate.
    @Author: wavefancy@gmail.com

    Usage:
        mannWhitneyUtestR.py -p float
        mannWhitneyUtestR.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout.

    Options:
        -p float      The point for intepolate.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input example
    ------------------------
0       0.942422883     0.937052382     0.93964204
5.87664 0.832453223     0.831524181     0.829448001
11.75328        0.73976121      0.748933403     0.743408757
17.62992        0.603333381     0.631212668     0.624485212
23.50656        0.495268473     0.530872061     0.528108472
29.3832 0.394239821     0.428279775     0.432011193
35.25984        0.321015298     0.346759356     0.355449038
41.13648        0.269207774     0.285845527     0.298540884

    # -p 0.5
    ------------------------
5.0000e-01      2.3241e+01      2.5263e+01      2.5205e+01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    point = float(args['-p'])

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data.append([float(x) for x in line.split()])

    import numpy as np
    from scipy.interpolate import interp1d
    out =[point]

    for i in range(1,len(data[0])):
        xx = []
        yy = []
        for x in data:
            xx.append(x[i])
            yy.append(x[0])
        # print(xx)
        # print(yy)
        ius = interp1d(xx, yy, kind='cubic')
        out.append(ius(point))

    sys.stdout.write('%s\n'%('\t'.join(['%.4e'%(x) for x in out])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
