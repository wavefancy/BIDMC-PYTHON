#!/usr/bin/env python3

"""

    Format the genotype output from ExomeModelFilter.
    @Author: wavefancy@gmail.com

    Usage:
        FormatGenoLineByFamily.py -c int
        FormatGenoLineByFamily.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -c int           Column index for genotype column, starts from 1.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #Genotype column from: ExomeModelFilter
    ------------------------
(KFH-4[KFH19:1/1:0,157];KFH20:0/1:84,70;KFH18:0/1:102,107),(CPMC139[CPMC139:1/1:0,101])
(FGGU1[FGGU11:0/1:16,13;FGGU117:0/1:14,19;FGGU1112:./.;FGGU114:0/1:13,18];FGGU1110:./.)
(FGGU1[FGGU11:0/1:19,23;FGGU117:0/1:13,12;FGGU1112:./.:3,0;FGGU114:0/1:17,14];FGGU1110:0/0:13,0)

    #output:
    ------------------------
FGGU11  FGGU117 FGGU1112        FGGU114 FGGU1110
0/1:16,13       0/1:14,19       ./.     0/1:13,18       ./.
0/1:19,23       0/1:13,12       ./.:3,0 0/1:17,14       0/0:13,0
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    col = int(args['-c']) -1

    from collections import OrderedDict
    idGeno = OrderedDict() #{idName - [geno list.]}
    for line in sys.stdin:
        line = line.strip()
        if line:
            lineContent = line.split()
            ss = lineContent[col]
            outArr = [lineContent[x] for x in range(len(lineContent)) if x != col]

            #split by family
            fams = ss.split(')')[:-1]
            if len(fams) <= 0:
                out = ['FamilyName', 'IdName', 'Genotype', 'Disease']
                sys.stdout.write('%s\n'%('\t'.join(out + outArr)))
            else:
                for f in fams:
                    f = f.strip(',').strip('(')
                    fss = f.split('[')
                    fname = fss[0]
                    fss = fss[1].split(']')
                    #affected individuals.
                    for a in fss[0].split(';'):
                        aSS = a.split(':')
                        out = [fname, aSS[0], aSS[1], '1']
                        sys.stdout.write('%s\n'%('\t'.join(out + outArr)))
                    #unaffected individuals.
                    if fss[1]:
                        for u in fss[1][1:].split(';'):
                            uSS = u.split(':')
                            out = [fname, uSS[0], uSS[1],'0']
                            sys.stdout.write('%s\n'%('\t'.join(out + outArr)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
