#!/usr/bin/env python3

"""

    Prepare data for ploting manhatton plot by CategoryPlot2.
    @Author: wavefancy@gmail.com

    Usage:
        manhattonDataHelper.py
        manhattonDataHelper.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
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
    #Output from: FamilyHitByGene.py
    ------------------------
chr1 100 10
chr1 200 5
chr1 300 2
chr2 300 5
chr2 500 15

    #output:
    ------------------------
    FamilyName      #SeqMember      #hitGeneNum     GeneList
    S55     3       5       CHRNA7-chr15-3  NCAM2-chr21-3
    FGJG1   3       4       JAK3-chr19-2    KRT3-chr12-3    NKD2-chr5-4     MKLN1-chr7-1
    FGEG    3       21      RET-chr10-2-Auto-Dominant-CAKUT COLEC12-chr18-6 NUDT6-chr4-2    C6or
    f222-chr6-5
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.2')
    # version 2.2: add the option for abline.
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    colors = ['#2678B2','#FD7F28','#339F34','#D42A2F']
    colorIndex = 0
    def getColor():
        'Rotately get the color code.'
        return colors[colorIndex++%len(colors)]

    chrs = []
    shif = 0
    currentMinPos = 0
    outPos = []
    outValues = []
    outColors = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                pos = int(ss[1])
                val = float(ss[2])
                if len(chrs) ==0 or chrs[-1] != ss[0]:
                    chrs.append(ss[0])
                    currentMinPos = pos
                    shif =

            except ValueError:
                sys.stdout.write('Can not parse value at line (skipped):%s\n'%(line))







sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
