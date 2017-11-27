#!/usr/bin/env python3

"""

    Compute the sum of the gene ranking score of known gene set or random gene set.
    @Author: wavefancy@gmail.com

    Usage:
        Sum4RandomKnownGeneSet.py (-k file | -s int -r int)
        Sum4RandomKnownGeneSet.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output results to stdout.
        2. Input data format: two columns, gene_name and ranking score.


    Options:
        -k file       Known gene set. One gene name one line.
        -s int        The number of genes for random selection.
        -r int        The number of times for repeating the random selection process.
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
1       1
2       2
3       3
4       4
5       5
6       7

#Output example: -k <(echo -e '1\n2')
------------------------
3

#Output example: -r 3 -s 4
------------------------
1.6000e+01
1.4000e+01
1.0000e+01
          ''');

if __name__ == '__main__':
<<<<<<< HEAD
    args = docopt(__doc__, version='2.0')
    #version 2.0
    #1. add function for line comments.

    knownGeneSet = set()
    sSize = -1 #random selection gene set size
    rTimes = -1 #repeating times for the random selection.

    if args['-k']:
        with open(args['-k'], mode='r') as kf:
            for line in kf:
                line = line.strip()
                if line:
                    knownGeneSet.add(line)
=======
    args = docopt(__doc__, version='1.0')

    knownGenes = set()
    sSize = -1 # random selection gene set size.
    rTimes = -1 # the number of times for random selection.

    if args['-k']:
        with open(args['-k'],'r') as target:
            for line in target:
                if line:
                    line = line.strip()
                    knownGenes.add(line)
>>>>>>> a22d0c762b78e4204d9c6d7538620e8f71dcb051

    if args['-s']:
        sSize = int(args['-s'])
    if args['-r']:
        rTimes = int(args['-r'])
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    allData = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            allData.append((ss[0],float(ss[1])))

<<<<<<< HEAD
    if knownGeneSet:
        out = [x for x in allData if x[0] in knownGeneSet]
        if len(out) != len(knownGeneSet):
            sys.stderr.write('ERROR: Gene missing or repeat in input data!!!\n')
            sys.exit(-1)
        sys.stdout.write('%.4e\n'%(sum[x[1] for x in out]))

    if rTimes >0:
        import numpy.random as r
        for i in range(rTimes):
            tt = r.choice(allData, size=sSize, replace=False)
            sys.stdout.write('%.4e\n'%(sum[x[1] for x in out]))
=======
    if knownGenes:
        out = [x for x in allData if x[0] in knownGenes]
        if len(out) != len(knownGenes):
            sys.stderr.write('ERROR: Not all genes in known genes has weight or repeat entries from stdin.\n')
            sys.exit(-1)

        sys.stdout.write('%.4e\n'%(sum([x[1] for x in out])))

    # print(allData)
    allData = [x[1] for x in allData]
    import numpy.random as random
    if rTimes >0:
        for i in range(rTimes):
            out = random.choice(allData,size=sSize,replace=False)
            # print(out)
            sys.stdout.write('%.4e\n'%(sum([x for x in out])))
>>>>>>> a22d0c762b78e4204d9c6d7538620e8f71dcb051

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
