#!/usr/bin/env python

"""

    Normalize site observed ancestry by genome-wide average.
    2*ID_average - ExpectedCopiesOfPop1Ancestry.
    @Author: wavefancy@gmail.com

    Usage:
        HapmixEPop1NormalizedByIDAverage.py -a IDaverage
        HapmixEPop1NormalizedByIDAverage.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read ExpectedCopiesOfPop1Ancestry from stdin, and output to stdout.

    Options:
        -a IDaverage     Individual average for pop1, one line one person.
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
    #ExpectedCopiesOfPop1Ancestry, one column each person.
    ------------------------
1 1 2 1 2 2
1 2 2 1 2 2

    #id average:
    ------------------------
0.8
0.5
0.1

    #output:
    ------------------------
0.40    0.00    -0.20
-0.60   0.00    -0.20
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    idav = [] # 2*ID_average
    with open(args['-a'],'r') as ifile:
        for line in ifile:
            line = line.strip()
            if line:
                idav.append(2 * float(line))

    checkLen = True
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            ss = [float(x) for x in ss] #number of pop1 copy for each person.

            if checkLen:
                if len(ss) != len(idav):
                    sys.stderr.write('Error: numbr of individuals in ID_average file is not the same as that in sys.stdin.\n')
                    sys.exit(-1)
                else:
                    checkLen = False

            out = [ '%.2f'%(y-x) for x,y in zip(idav, ss)]
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
