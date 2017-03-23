#!/usr/bin/env python3

"""
    Convert IBDLD IBD output file for CategoryPlot.py plot.
    Usage:
        IBDLDout4Plot.py
        IBDLDout4Plot.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#IBDLD output:
------------------------------------
FGGU114 FGGU114 Sample_M_FG-GU11_010_010        Sample_M_FG-GU11_010_010        10      323283  29891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.957
FGGU114 FGGU114 Sample_M_FG-GU11_010_010        Sample_M_FG-GU11_010_010        10      323283  17891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.957 20000000  27891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.5

# output:
------------------------------------
C       323282  0
C       323284  2
C       17891320        2
C       17891322        1
C       19999999        1
C       20000001        2
C       27891320        2
C       27891322        1
C       29891320        1
C       29891322        0
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #from interval import interval
    from intervals import IntInterval
    #api: https://github.com/kvesteri/intervals

    intvl = []
    pts = set()
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()[5:]
            for i in range(0,len(ss),6):
                l = int(ss[i])
                r = int(ss[i+1])
                intvl.append(IntInterval([l,r]))
                #IntInterval([1, 4])
                pts.add(l)
                pts.add(r)

    def getCounts(x):
        '''get the number of intervals include this points'''
        return len([y for y in intvl if x in y])

    for x in sorted(list(pts)):
        for k in (x-1,x+1):
            y = getCounts(k)
            sys.stdout.write('C\t%d\t%d\n'%(k,y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
