#!/usr/bin/env python3

"""

    Compute pvalue for binomial test.
    @Author: wavefancy@gmail.com

    Usage:
        BinomialTest.py -s sindex -t tindex -p pindex [-a alt]
        BinomialTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin and output results to stdout, add one column for pvalue.
        2. See example by -f.

    Options:
        -s sindex      Column index for successful trials.
        -t tindex      Column index for total number of trials.
        -p pindex      Column index for the probability of success.
        -a alt         ‘two-sided’(Default), ‘greater’, ‘less’.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#example
--------------------
echo '500 10000 0.5' | python3 BinomialTest.py -s 1 -t 2 -p 3 -a less
500     10000   0.5     0.0000e+00
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    sindex = int(args['-s']) -1
    tindex = int(args['-t']) -1
    pindex = int(args['-p']) -1
    alt = 'two-sided'
    if args['-a']:
        alt = args['-a']

    from scipy import stats
    #api: print(stats.binom_test.__doc__)
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                s = int(ss[sindex])
                t = int(ss[tindex])
                p = float(ss[pindex])

                pv = stats.binom_test(s, t, p, alternative=alt)
                ss.append('%.4e'%(pv))
            except ValueError:
                ss.append('pValue')

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
