#!/usr/bin/env python3

"""

    Get summary statistics from category data.
    @Author: wavefancy@gmail.com

    Usage:
        CategoryStats.py -c cindex -k vindex (-d|-s)
        CategoryStats.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin and output results to stdout.
        2. See example by -f.

    Options:
        -c cindex      Column index for category name (column index starts from 1).
        -k vindex      Column index for value of each category.
        -d             Output category value diversity, NumberOfDifferentTypeOfValues/TotalNumberOfValues.
        -s             Output category value set.
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
#input example
--------------------
C1  X1
C1  Y1
C2  X
C2  X

# cat test.txt | python3 CategoryStats.py -c 1 -k 2 -d
--------------------
C1      1.0000
C2      0.5000

#cat test.txt | python3 CategoryStats.py -c 1 -k 2 -s
--------------------
C1      X1;Y1
C2      X
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    cindex = int(args['-c']) -1
    vindex = int(args['-k']) -1

    from collections import OrderedDict
    gMap = OrderedDict()

    def findGroupIndex(name):
        '''find the group index for name'''
        for k,v in enumerate(gsets):
            if name in v:
                return k
        return -1 #if not found in any group.

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[cindex] not in gMap:
                gMap[ss[cindex]] = []

            gMap[ss[cindex]].append(ss[vindex])

    #output results
    #print(gMap)
    if args['-d']:
        for k,v in gMap.items():
            sys.stdout.write('%s\t%.4f\n'%(k,len(set(v))*1.0/len(v)))
    elif args['-s']:
        for k,v in gMap.items():
            sys.stdout.write('%s\t%s\n'%(k,';'.join(set(v))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
