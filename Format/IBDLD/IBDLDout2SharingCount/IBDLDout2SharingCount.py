#!/usr/bin/env python3

"""
    Convert IBDLD IBD output file to the number of IBD sharing pairs for inquery sites.
    Usage:
        IBDLDout2SharingCount.py -i IBDLDoutFile -c int
        IBDLDout2SharingCount.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -i file        IBDLD output file.
        -c int         Column index for position, 1 based.
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
#IBDLD output (-i):
------------------------------------
FGGU114 FGGU114 Sample_M_FG-GU11_010_010        Sample_M_FG-GU11_010_010        10      323283  29891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.957
FGGU114 FGGU114 Sample_M_FG-GU11_010_010        Sample_M_FG-GU11_010_010        10      323283  17891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.957 20000000  27891321        chr10:323283:A:G        chr10:29891321:T:C      263     2.5

#Input from stdin
------------------------------------
pos
17891311
17891341
20000000
20000011

# output:
------------------------------------
pos     IBDSharingPairs
17891311        2
17891341        1
20000000        2
20000011        2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    posCol = int(args['-c'])-1

    from intervals import IntInterval
    #api: https://github.com/kvesteri/intervals

    intvl = []
    #pts = set()
    with open(args['-i'],'r') as ibdfile:
        for line in ibdfile:
            line = line.strip()
            if line:
                ss = line.split()[5:]
                for i in range(0,len(ss),6):
                    l = int(ss[i])
                    r = int(ss[i+1])
                    intvl.append(IntInterval([l,r]))
                    #IntInterval([1, 4])
                    #pts.add(l)
                    #pts.add(r)

    def getCounts(x):
        '''get the number of intervals include this points'''
        return len([y for y in intvl if x in y])

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                pos = int(ss[posCol])
                sys.stdout.write('%s\t%d\n'%(line, getCounts(pos)))

            except ValueError:
                sys.stdout.write('%s\tIBDSharingPairs\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
