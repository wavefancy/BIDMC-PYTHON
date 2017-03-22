#!/usr/bin/env python3

"""
    Generate all possible pairs of a list.
    Usage:
        allPairsOfList.py [-p|-c]
        allPairsOfList.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -c             All the combinations of a list, no repeat.
        -p             All the ordered combinations of a list, no repeat.
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
#input:
------------------------------------
A   B
C   D
E   F

# -c
------------------------------------
A   B   C   D
A   B   E   F
C   D   E   F

# -p
------------------------------------
A   B   C   D
A   B   E   F
C   D   A   B
C   D   E   F
E   F   A   B
E   F   C   D
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data.append(line)

    import itertools
    if args['-c']:
        for x, y in itertools.combinations(data,2):
                sys.stdout.write('%s\t%s\n'%(x,y))
    if args['-p']:
        for x, y in itertools.permutations(data,2):
                sys.stdout.write('%s\t%s\n'%(x,y))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
