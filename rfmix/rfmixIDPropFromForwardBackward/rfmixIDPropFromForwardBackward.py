#!/usr/bin/env python

"""
    *****Legency version 1.0, please use updated versioin****
    Estimate expected individual level ancestry from rfmix ForwardBackword output.
    @Author: wavefancy@gmail.com

    Usage:
        rfmixIDPropFromForwardBackward.py -n nancestry
        rfmixIDPropFromForwardBackward.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read rfmix ForwardBackword output from stdin, and output to stdout.
        2. Output each person one line, for expected_Ancestry1 expected_Ancestry2 ...

    Options:
        -n nancestry     Number of reference ancestry.
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
    #rfmix output, 2 person, 3 snps
    ------------------------
0.1 0.9 0.2 0.8 0.4 0.6 0.5 0.5
0.1 0.9 0.2 0.8 0.4 0.6 0.3 0.7
0.5 0.5 0.3 0.7 0.2 0.8 0.6 0.4

    #output:
    ------------------------
anc1    anc2
0.2333  0.7667
0.4000  0.6000
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    nanc = int(args['-n']) # number of ancestry.

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
    sys.stdout.write('%s\n'%('\t'.join([ 'anc' + str(x+1) for x in range(nanc) ])))
    for i in range(0, len(psum), nanc * 2):
        out = []
        for j in range(nanc):
            t = psum[i + j] + psum[i + j + nanc] #each person 2 copies.
            out.append(t/total)
        sys.stdout.write('%s\n'%('\t'.join([ '%.4f'%(x) for x in out ])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
