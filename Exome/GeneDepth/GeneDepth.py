#!/usr/bin/env python3

"""

    Compute reads coverage depth for gene.

    @Author: wavefancy@gmail.com

    Usage:
        GeneDepth.py
        GeneDepth.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read 'samtools bedcov' output from stdin, and output to stdout.
        4. See example by -f.

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
    #Output from 'samtools bedcov'
    ------------------------
chr1    1   5   name1+1 8
chr1    6   10  name1+2 5
chr2    10  50  name2   30

    #output: geneName, averageCoverage
    ------------------------
name1   1.62
name2   0.75
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from collections import OrderedDict
    dataMap = OrderedDict() #genaName -> [[length],[totalCoverage]] ...
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                left = int(ss[1])
                right  = int(ss[2])
                gname = ss[3].split('+')[0]
                cov = int(ss[4])
                if gname not in dataMap:
                    dataMap[gname] = [[],[]]
                dataMap[gname][0].append(right - left)
                dataMap[gname][1].append(cov)

            except ValueError:
                sys.stderr.write('Warning: parse value error at line: %s\n'%(line))

    #output results.
    for k,v in dataMap.items():
        sys.stdout.write('%s\t%.2f\n'%(k, sum(v[1])*1.0/sum(v[0])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
