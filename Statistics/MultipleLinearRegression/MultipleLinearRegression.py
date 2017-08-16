#!/usr/bin/env python

"""

    Perform multiple linear regression, Y ~ X1 + X2 + ... Xn
    @Author: wavefancy@gmail.com

    Usage:
        MultipleLinearRegression.py
        MultipleLinearRegression.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read from stdin and output to stdout. Y, X1, X2, each variable one line.
        2. Output results from stdout.

    Options:
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
    #input example, each line two samples, separated by ';'
    ------------------------
0.80  0.83  1.89  1.04  1.45  1.38  1.91  1.64  0.73  1.46; 1.15  0.88  0.90  0.74  1.21

    #output example (benchmarked with R, wilcox.test)
    ------------------------
1.2721e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # if(args['--format']):
    #     ShowFormat()
    #     sys.exit(-1)

    import numpy as np
    import statsmodels.api as sm
    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            data.append([float(x) for x in ss])

    y = data[0]
    x = data[1:]
    def reg_m(y, x):
        ones = np.ones(len(x[0]))
        X = sm.add_constant(np.column_stack((x[0], ones)))
        for ele in x[1:]:
            X = sm.add_constant(np.column_stack((ele, X)))
        results = sm.OLS(y, X).fit()
        return results

    print(reg_m(y,x).summary())

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
