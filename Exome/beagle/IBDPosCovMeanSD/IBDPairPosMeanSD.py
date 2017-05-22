#!/usr/bin/env python3

"""

    Compute the mean and standard devidation of the number of IBD pairs at each position.
    @Author: wavefancy@gmail.com
    @version: 1. add function to output maxium value.

    Usage:
        IBDPairPosMeanSD.py <infiles>... [-m]
        IBDPairPosMeanSD.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read input from file list(output from IBDPairByPos.py), and output results to stdout.
        2. ***Out put POS has been shift to 1 based.***
        3. See example by -f.

    Options:
        -m            Output the number of IBD sharing of min and max shifting from mean.
                      mean - min, max - mean.
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
    #output from IBDPairByPos.py
    #in file1
    ------------------------
1       1
2       1
3       2
4       3
5       1

    #in file2
    ------------------------
1       1
2       5
3       3
4       4
6       1

    #output:
    ------------------------
Pos     Mean    Std
1       1.0000  0.0000
2       3.0000  2.0000
3       2.5000  0.5000
4       3.5000  0.5000
5       1.0000  0.0000
6       1.0000  0.0000
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    minmax = False
    if args['-m']:
        minmax = True

    covMap = {} #{pos -> [cov1, cov2 ... ]}
    for file in args['<infiles>']:
        with open(file,'r') as input:
            for line in input:
                line = line.strip()
                if line:
                    ss = line.split()
                    try:
                        pos = int(ss[0])
                        cov = int(ss[1])
                        if pos not in covMap:
                            covMap[pos] = []
                        covMap[pos].append(cov)

                    except ValueError:
                        sys.stderr.write('Warning: parse value error at: %s\n'%(line))


    #output results:
    from numpy import mean, std
    out = sorted(covMap.items(), key=lambda x: x[0])
    if minmax:
        sys.stdout.write('Pos\tMean\tStd\tMean-Min\tMax-Mean\n')
    else:
        sys.stdout.write('Pos\tMean\tStd\n')
    for k,v in out:
        if minmax:
            m = mean(v)
            sys.stdout.write('%d\t%.4f\t%.4f\t%.4f\t%.4f\n'%(k+1, m, std(v), m - min(v), max(v) -m ))
        else:
            sys.stdout.write('%d\t%.4f\t%.4f\n'%(k+1, mean(v), std(v)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
