#!/usr/bin/env python3

"""

    Generate data for QQ plot.

    @Author: wavefancy@gmail.com

    Usage:
        QQPlotData.py -x xindex [-y yindex]
        QQPlotData.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output results (x,y) to stdout.
            (x,y) is the point for QQ plot.
        2. If input only have one dataset (-x), the other dataset(-y) will
            be generated from uniform distribution.

    Options:
        -x xindex     Column index for input data set one, index starts from 1.
        -y yindex     Column index for input data set two.
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# echo -e '0.1\\n0.6\\n0.3' | python3 QQPlotData.py  -x 1
-------------------------------------------
1e-01   2.6914e-01
3e-01   3.2691e-01
6e-01   7.0672e-01

#echo -e '0.1 0.2\\n0.6 0.5\\n0.3 0.4' | python3 QQPlotData.py  -x 1 -y 2
-------------------------------------------
1.0000e-01      2.0000e-01
3.0000e-01      4.0000e-01
6.0000e-01      5.0000e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    xindex = int(args['-x']) -1
    yindex = -1
    if args['-y']:
        yindex = int(args['-y']) -1

    xdata = []
    ydata = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                x = float(ss[xindex])
                if yindex >= 0:
                    y = float(ss[yindex])
                    ydata.append(y)
                xdata.append(x)

            except ValueError:
                sys.stderr.write('Parse value error (SKIPPED): %s\n'%(line))
    if not ydata:
        import random
        ydata = [random.random() for x in xdata]

    #sort data and output.
    for x,y in zip(sorted(xdata), sorted(ydata)):
        sys.stdout.write('%.4e\t%.4e\n'%(x,y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
