#!/usr/bin/env python3

"""
    Convert impute2 legend format to merlin frequency format.
    Usage:
        Impute2Legend2MerlinFreq.py -c cname -m maf
        Impute2Legend2MerlinFreq.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -c cname       Chromosome name.
        -m maf         Minor allele frequency filter, only output sites with MAF > this value.
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
# input 4 column: pos ref alt altFre
------------------------------------
60086 G C 0.00102249488752556
60105 G A 0.5

# output:
------------------------------------
M chr19:60086
A G 0.9990
A C 0.0010
M chr19:60105
A G 0.5000
A A 0.5000
    ''');


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #pedfile = args['-p']
    cname = args['-c']
    maf = float(args['-m'])

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                altFre = float(ss[3])
                m = min(altFre, 1-altFre)
                if m <= maf:
                    continue

                sys.stdout.write('M %s:%s\n'%(cname,ss[0]))
                sys.stdout.write('A %s %.4f\n'%(ss[1], 1-altFre))
                sys.stdout.write('A %s %.4f\n'%(ss[2], altFre))
            except ValueError:
                sys.stderr.write('WARN: parse value error(SKIPPED): %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
