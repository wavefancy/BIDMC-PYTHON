#!/usr/bin/env python3

"""

    Compute the Z-score for cosegregation pattern.

    xi is an indicater for successful transmit.
    S = sum(xi). Z = (S-E(S))/SD(S).
    E(xi) = p, Var(xi) = p(1-p), p = (1/2)^ni, ni the affected number of a family.

    @Author: wavefancy@gmail.com

    Usage:
        Zscore4cosegration.py
        Zscore4cosegration.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
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
# each line is the number of affected in a family,
# Positive number: successed in cosegregation check.
# Negative number: failed in cosegregation check.
# ----------------------------------------------------
2
3
-2
4

# output:
# ----------------------------------------------------
3.1383
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data.append(int(line))

    import math
    S = len([x for x in data if x > 0])
    p = [math.pow(0.5, abs(x)) for x in data]

    ES = sum(p)
    VarS = sum([x*(1-x) for x in p])

    Z = (S - ES)/math.pow(VarS, 0.5)
    sys.stdout.write('%.4f\n'%(Z))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
