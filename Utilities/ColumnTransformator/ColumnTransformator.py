#!/usr/bin/env python3

"""

    Transform the number of a column.
    @Author: wavefancy@gmail.com

    Usage:
        ColumnTransformator.py -c col -t transformer
        ColumnTransformator.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -c col         Column index for transformer to be applied.
        -t transformer Transform action:
                       maf : to minor allele frequency. min(1-p,p)
                       nlog: negative log. val --> -1.0 * math.log10(float(val))
                       nint: nearst int value.
                       1sub: val -> 1-val
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
    ''');

class P(object):
    col = -1
    action = ''

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    P.col = int(args['-c']) -1
    P.action = args['-t']
    tMap = {'maf','nlog','nint','1sub'}
    if P.action not in tMap:
        sys.stderr.write('Transformer "%s" not supported! Please check!\n'%(P.action))

    import math
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if P.action == 'nlog':
                try:
                    ss[P.col] = -1.0 * math.log10(float(ss[P.col]))
                    ss[P.col] = '%.4e'%(ss[P.col])
                except ValueError:
                    sys.stderr.write('WARNING: Can not parse float value or value 0 in line: %s\n'%(line))
            elif P.action == 'nint':
                try:
                    ss[P.col] = int( float(ss[P.col])+0.5 )
                    ss[P.col] = '%d'%(ss[P.col])
                except ValueError:
                    sys.stderr.write('WARNING: Can not parse float value in line: %s\n'%(line))

            elif P.action == 'maf':
                try:
                    val = float(ss[P.col])
                    ss[P.col] = '%.4f'%(min(val, 1-val))
                except ValueError:
                    ss[P.col] = 'NA'

            elif P.action == '1sub':
                try:
                    val = float(ss[P.col])
                    ss[P.col] = '%.4f'%(1-val)
                except ValueError:
                    ss[P.col] = 'NA'

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
