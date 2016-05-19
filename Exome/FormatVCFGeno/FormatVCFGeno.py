#!/usr/bin/env python3

"""

    Reformat VCF genotype format.

    @Author: wavefancy@gmail.com

    Usage:
        FormatVCFGeno.py -c col [-g]
        FormatVCFGeno.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. Directly copy comment line, comment line started by '#'.
        3. See example by -f.

    Options:
        -c cols        Column indexes for reformat, 1|1,3. 1 based.
        -g             Only output genotype, genotype should be put at first.
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
#Input data (output from genmod).
------------------------
#Title1 Title2
0/0:6,0:6:18:0,18,165   0/0:11,0:11:27:0,27,405
0/0:9,0:9:0:0,0,241 0/0:7,0:7:15:0,15,225

#output data:
------------------------
#Title1 Title2
0/0:6,0 0/0:11,0
0/0:9,0 0/0:7,0
    ''');

class P(object):
    col = []

if __name__ == '__main__':
    args = docopt(__doc__, version='1.1')
    #version 1.1
    # add option for -g, for only output genotype.
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    P.col = [int(x)-1 for x in args['-c'].split(',')] #shift one column.
    import re
    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.startswith('#'):
                sys.stdout.write('%s\n'%(line))
            else:
                ss = line.split()
                for c in P.col:
                    if args['-g']:
                        ss[c] = ss[c].split(':')[0] #genotype should be put at first.
                    else:
                        ss[c] = ':'.join(ss[c].split(':')[0:2])

                #print(ss)
                sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
