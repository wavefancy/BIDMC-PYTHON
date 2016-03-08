#!/usr/bin/env python3

"""

    Compute the number of IBD pair at each position.
    @Author: wavefancy@gmail.com

    Usage:
        IBDPairByPos.py
        IBDPairByPos.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin(output from beagle3 fibd), and output results to stdout.
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
    #output from beagle3 fibd
    ------------------------
    FGGR111 FGGR114 1     5     9.21E-16
    FGGR152 FGGR1351        3     5     6.96E-13
    FGGR111 FGGR114 4     6    1.79E-19

    #output:
    ------------------------
    1       1
    2       1
    3       2
    4       3
    5       1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    covMap = {} #{pos->cov}
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                start = int(ss[2])
                end = int(ss[3])
                for x in range(start, end):
                    if x not in covMap:
                        covMap[x] = 1
                    else:
                        covMap[x] = covMap[x] + 1

            except ValueError:
                sys.stderr.write('Warning: Parse value error at line: %s\n'%(line))

    #output results.
    out = sorted(covMap.items(), key=lambda x: x[0])
    for k,v in out:
        sys.stdout.write('%d\t%d\n'%(k,v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
