#!/usr/bin/env python3

"""

    Compute the P value for using known genes as seeds, compared with random seeds.
    Output from: Rscript PPIRandomWalkWithRestart.R -n <file> -r <s>-<t>
    @Author: wavefancy@gmail.com

    Usage:
        PV4KnownSet.py
        PV4KnownSet.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Input data format: gene_name, weight_known_genes_as_seeds, weight_random_selected_seeds...

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
import signal
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def ShowFormat():
    '''File format example'''
    print('''
#Input example
------------------------
1 6.888e-02 6.888e-02 6.888e-02
2 1.150e-01 1.631e-02 1.150e-01
3 3.637e-01 2.499e-02 3.637e-01
4 3.390e-01 7.215e-02 3.390e-01
5 7.215e-02 3.390e-01 7.215e-02
6 2.499e-02 1.150e-01 2.499e-02
7 1.631e-02 3.637e-01 1.631e-02

#Output example:
------------------------
1       0.0000e+00
2       0.0000e+00
3       0.0000e+00
4       0.0000e+00
5       5.0000e-01
6       5.0000e-01
7       5.0000e-01
          ''');

if __name__ == '__main__':

    args = docopt(__doc__, version='1.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            name = ss[0]
            ss = [float(x) for x in ss[1:]]
            num = len([x for x in ss[1:] if x > ss[0]]) #number of observation >X.
            pv = num*1.0/(len(ss)-1)

            sys.stdout.write('%s\t%.4e\n'%(name, pv))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
