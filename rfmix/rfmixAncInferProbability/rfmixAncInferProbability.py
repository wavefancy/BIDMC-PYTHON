#!/usr/bin/env python

"""

    Get ancestry inference probability from rfmix ForwardBackword output.
    @Author: wavefancy@gmail.com

    Usage:
        rfmixAncInferProbability.py -n nancestry
        rfmixAncInferProbability.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read rfmix ForwardBackword output from stdin, and output to stdout.

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

    #output: -n 2
    ------------------------
0.90    0.80    0.60    0.50
0.90    0.80    0.60    0.70
0.50    0.70    0.80    0.60
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    nanc = int(args['-n']) # number of ancestry.

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = [float(x) for x in line.split()]
            hap_prob = [] #ancestry infer probability for each haplotype.
            for x in range(0, len(ss), nanc):
                hap_prob.append(max(ss[x:x+nanc]))
            sys.stdout.write('%s\n'%('\t'.join(['%.2f'%(x) for x in hap_prob])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
