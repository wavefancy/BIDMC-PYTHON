#!/usr/bin/env python3

"""

    Compute basic statistics for a each row

    @Author: wavefancy@gmail.com

    Usage:
        BasicStatistics4Row.py [-t]
        BasicStatistics4Row.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.

    Options:
        -t            Output title.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #input:
    ------------------------
1   2   3
4   5   6

    #output: cat in.txt | python3 BasicStatistics4Row.py -t
    ------------------------
Min     1%Q     25%Q    Mean    Median  75%Q    99%Q    Max     SD      SE
1.0000  1.5000  1.5000  2.0000  2.0000  2.5000  2.9800  3.0000  0.8165  0.5774
4.0000  4.5000  4.5000  5.0000  5.0000  5.5000  5.9800  6.0000  0.8165  0.5774
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    if args['-t']:
        sys.stdout.write('Min\t1%Q\t25%Q\tMean\tMedian\t75%Q\t99%Q\tMax\tSD\tSE\n')

    import numpy as np
    from scipy import stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            vals = [float(x) for x in ss]

            minV = min(vals)
            q1 = np.percentile(vals,1)
            q25 = q1 = np.percentile(vals,25)
            meanV = np.mean(vals)
            medianV = np.median(vals)
            q75 = np.percentile(vals,75)
            q99 = np.percentile(vals,99)
            #print(q99)
            maxV = max(vals)
            sdV = np.std(vals)
            se = stats.sem(vals)
            sys.stdout.write('%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n'%(minV,q1,q25,meanV,medianV,q75,q99, maxV, sdV, se))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
