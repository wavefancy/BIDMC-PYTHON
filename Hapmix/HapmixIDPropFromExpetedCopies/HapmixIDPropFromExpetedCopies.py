#!/usr/bin/env python

"""

    Estimate expected individual level ancestry from expected copies of pop1 ancestry.
    @Author: wavefancy@gmail.com

    Usage:
        HapmixIDPropFromExpetedCopies.py
        HapmixIDPropFromExpetedCopies.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. Output each person one line, for expected_copyies_of_pop1_ancestry.

    Options:
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
    #input example, each column one person for expected_number_of_pop1_ancestry.
    ------------------------
0.1 0.9 0.2 0.8 0.4 0.6 0.5 0.5
0.1 0.9 0.2 0.8 0.4 0.6 0.3 0.7
0.5 0.5 0.3 0.7 0.2 0.8 0.6 0.4

    #output:
    ------------------------
0.1167
0.3833
0.1167
0.3833
0.1667
0.3333
0.2333
0.2667
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import numpy
    psum = numpy.empty(0)
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            total += 1
            ss = line.split()
            prob = numpy.array([float(x) for x in ss])
            if len(psum) == 0:
                psum = prob
            else:
                psum = psum + prob

    total = total * 2 # for 2 copies.
    #output title:
    psum = psum / total
    sys.stdout.write('%s\n'%('\n'.join([ '%.4f'%(x) for x in psum ])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
