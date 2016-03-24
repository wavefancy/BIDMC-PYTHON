#!/usr/bin/env python

"""

    Replace content according to key map values.
    @Author: wavefancy@gmail.com

    Usage:
        KeyMapReplace.py -p <key-value-pair-file> -k <kcol> [-r <rcol>] [-a aValue]
        KeyMapReplace.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and replace content based on key-map values.
        2. Output results to stdout.

    Options:
        -p <key-map-pair-file>  Key value pairs, one entry one line.
        -k <kcol>     Colum as key in stdin, column index starts from 1.
        -r <rcol>     Colum to replace in stdin, column index starts from 1.
        -a aValue     Add one column at line end, other than replace one column,
                        add 'aValue' if no key matching.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
    #kv_map:
    ------------------------
2   K
2   c
2   a

    #input:
    ------------------------
1   a
2   c
3   d

    #output: -p kv_map -k 1 -r 2
    ------------------------
1       a
2       K
3       d

    #output: -p kv_map -k 1 -a aval
    ------------------------
1       a       aval
2       c       K
3       d       aval
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #print(args)
    #sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)
    if args['-a'] and args['-r']:
        sys.stderr.write('ERROR: option -a|-r can only be applied by one of them.\n')
        sys.exit(-1)

    #read key-value pairs
    kv_map = {}
    for line in open(args['-p'],'r'):
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0] not in kv_map:
                kv_map[ss[0]] = ss[1]
            else:
                sys.stderr.write('Warning: Duplicate keys, only keep first entry. Skip: %s\n'%(line))

    #Replace one colum
    kcol = int(args['-k']) -1
    if args['-r']:
        rcol = int(args['-r']) -1
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[kcol] in kv_map:
                    ss[rcol] = kv_map[ss[kcol]]
                sys.stdout.write('%s\n'%('\t'.join(ss)))

    if args['-a']:
        val = args['-a']
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[kcol] in kv_map:
                    sys.stdout.write('%s\t%s\n'%('\t'.join(ss), kv_map[ss[kcol]]))
                else:
                    sys.stdout.write('%s\t%s\n'%('\t'.join(ss), val))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
