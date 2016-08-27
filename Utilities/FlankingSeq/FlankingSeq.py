#!/usr/bin/env python

"""

    Get flanking sequence for a position.
    @Author: wavefancy@gmail.com

    Usage:
        FlankingSeq.py -c chromosomeName -p position -f flankingLegth -r refSeq [-l]
        FlankingSeq.py -h | --help | -v | --version

    Notes:


    Options:
        -c chromosomeName   Sample name.
        -p position         [int] Physical position.
        -f flankingLegth    [int] The number of bp for flanking seq.
        -r refSeq           Fasta file for reference seq.
        -l                  Output one line format.
        -h --help           Show this screen.
        -v --version        Show version.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

if __name__ == '__main__':
    args = docopt(__doc__, version='3.0')

    refSeq = args['-r']
    chr = args['-c']
    pos = int(args['-p'])
    fLen = int(args['-f'])
    onelineFormat = False
    if args['-l']:
        onelineFormat = True
    #print(args)
    #sys.exit(-1)

    from pyfaidx import Fasta
    genes=Fasta(refSeq)
    ranges=[(pos-fLen-1,pos-1),(pos, pos + fLen)] #include x, exclude y.

    #sys.stdout.write('%s\n'%(chr))
    x,y = ranges[0]
    #sys.stdout.write('%d-%d: left-%d\n'%(x+1,y,fLen))
    aleft = []
    for k in range(x,y):
        aleft.append(str(genes[chr][k:k+1]))
        #sys.stdout.write('%s'%(aa))

    aaPos = genes[chr][pos-1:pos]
    #sys.stdout.write('\n%s <--- mutate site: %d\n'%(aa,pos))

    xx,yy = ranges[1]
    #sys.stdout.write('%d-%d: right-%d\n'%(x+1,y,fLen))]
    aright = []
    for k in range(xx,yy):
        aright.append(str(genes[chr][k:k+1]))
        #sys.stdout.write('%s'%(aa))

    if onelineFormat:
        sys.stdout.write('%s\t'%(chr))
        sys.stdout.write('%d\t'%(pos))
        sys.stdout.write('%s\t'%(aaPos))
        sys.stdout.write('%s\t'%(''.join(aleft)))
        sys.stdout.write('%s\n'%(''.join(aright)))

    else:
        sys.stdout.write('%s\n'%(chr))
        sys.stdout.write('%d-%d: left-%d\n'%(x+1,y,fLen))
        sys.stdout.write('%s'%(''.join(aleft)))
        sys.stdout.write('\n%s <--- mutate site: %d\n'%(aaPos,pos))
        sys.stdout.write('%d-%d: right-%d\n'%(xx+1,yy,fLen))
        sys.stdout.write('%s'%(''.join(aright)))
        sys.stdout.write('\n')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
