#!/usr/bin/env python3

"""

    Compute the allele frequency for haps/sample format.

    @Author: wavefancy@gmail.com

    Usage:
        HapsAlleleFre.py [-n int] [-s  int] [-m string]
        HapsAlleleFre.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        3. Output results to stdout.

    Options:
        -n int          Column index for snp name, int, default 2.
        -s int          Column index for seq start(including), int, default 6.
        -m string       Set the missing code for allele, default -9.
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    missingCode = '-9'  # [-m]
    nameIndex = 2       # [-n]
    seqStart = 6        # [-s]

    if args['-m']:
        missingCode = args['-m']
    if args['-s']:
        seqStart = int(args['-s'])
    if args['-n']:
        nameIndex = int(args['-n'])
    nameIndex -= 1
    seqStart -= 1

    from collections import Counter
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()

            alleles = Counter(ss[seqStart:])
            #remove missing
            noM = {}
            total = 0
            for k in alleles.keys():
                if k != missingCode:
                    noM[k] = alleles[k]
                    total += alleles[k]
            #output frequency
            #print(noM)
            out = ['%s:%.4f'%(x,noM[x]*1.0/total) for x in sorted(noM.keys())]
            sys.stdout.write('%s\t%s\n'%(ss[nameIndex], '_'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
