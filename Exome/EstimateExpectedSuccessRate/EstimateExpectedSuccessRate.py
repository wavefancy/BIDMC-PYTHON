#!/usr/bin/env python3

"""

    Estimate the expected success rate for each gene.

    @Author: wavefancy@gmail.com

    Usage:
        EstimateExpectedSuccessRate.py -t totalEvents
        EstimateExpectedSuccessRate.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output results to stdout.
        3. Output results to stdout.

    Options:
        -t int          Total number of events.
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    input example(-t 100):
----------------------
x1      3
x2      5
x3      10

#output
----------------------
x1      3       1.6667e-01
x2      5       2.7778e-01
x3      10      5.5556e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    totalEvents = args['-t']

    oTotal = 0
    content = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            x = int(ss[1])
            content.append((ss[0],x))
            oTotal += x

    #output
    for x in content:
        out = [x[0], str(x[1])]
        out.append('%.4e'%(x[1]*1.0/oTotal))
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
