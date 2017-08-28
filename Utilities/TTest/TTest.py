#!/usr/bin/env python3

"""

    Two sample t-test by scipy library.

    @Author: wavefancy@gmail.com

    Usage:
        TTest.py [-g spliter] [-t spliter] [-e]
        TTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output selected lines to stdout.
        2. Output format, [GropName] PValue t-statistic.

    Options:
        -g spliter    Set spliter for group, default ';'.
        -t spliter    Set group title spliter, default ':'.
        -e            Set equal variance of two samples, default unequal variance.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input example:
--------------------------
t1: 1 2 3 4;t2: 6 7 8 9 10
1 2 3 4;6 7 8 9 10
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    gspliter = ';'
    tspliter = ':'
    equalVar = False

    if args['-g']:
        gspliter = args['-g']
    if args['-t']:
        gspliter = args['-t']
    if args['-e']:
        equalVar = True

#-------------------------------------------------
    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            gg = line.split(';')
            g1 = gg[0].split(':')
            g2 = gg[1].split(':')
            # print(gg)

            d1 = []
            d2 = []
            t1 = ''
            t2 = ''
            if len(g1) == 2:
                d1 = [float(x) for x in g1[1].strip().split()]
                t1 = g1[0].strip()
            else:
                d1 = [float(x) for x in g1[0].strip().split()]

            if len(g2) == 2:
                d2 = [float(x) for x in g2[1].strip().split()]
                t2 = g2[0].strip()
            else:
                d2 = [float(x) for x in g2[0].strip().split()]

            r = stats.ttest_ind(d1, d2, equal_var = equalVar)

            out = ''
            if t1:
                out = out + t1 + '\t' + t2 + '\t'

            out += '%.4e'%(r[1]) + '\t'
            out += '%.4e'%(r[0])

            sys.stdout.write('%s\n'%(out))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
