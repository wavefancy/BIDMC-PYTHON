#!/usr/bin/env python3

"""

    Extract AAChange information from ANNOVAR output, 'AAChange' field.
    @Author: wavefancy@gmail.com

    Usage:
        AAChangeInfoExtractor.py -c col [-t task]
        AAChangeInfoExtractor.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout,
            add additional columns for extracted
        2. See example by -f.

    Options:
        -c cols        Column index for AAChange field
        -t int         What type of information to extract.
                        1: protein position (default).

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
#example input
-----------------------------
x1  7   0   186 95
x2  31  10  3183    1731
x3  x   x   x   x

# cat test.txt | python3 FisherExactTest.py -c 2,3 -t 4,5
-----------------------------
x1      7       0       186     95      7.6810  5.8515e-02
x2      31      10      3183    1731    1.6859  9.7437e-02
WARNING: parse int error for line(skipped): x3  x   x   x   x
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    taskMap = {'1':'ProteinLocation'}
    task = 'ProteinLocation'
    if args['-t']:
        if args['-t'] not in taskMap:
            sys.stderr.write('ERROR: please set proper value for -t.\n')
            sys.exit(-1)
        else:
            task = taskMap[args['-t']]
    col = int(args['-c']) -1

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            out = ''
            if task == 'ProteinLocation':
                xx = ss[col].split(':p.')
                if len(xx) != 2:
                    out = 'ProteinLocation'
                else:
                    out = xx[1][1:-1]

            ss.append(out)
            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
