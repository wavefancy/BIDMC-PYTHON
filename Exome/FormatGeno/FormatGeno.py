#!/usr/bin/env python3

"""

    Format the genotype output from ExomeModelFilter.
    @Author: wavefancy@gmail.com

    Usage:
        FormatGeno.py
        FormatGeno.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
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
    S55     3       5       CHRNA7  chr15   3
    S55     3       5       NCAM2   chr21   3
    FGJG1   3       4       JAK3    chr19   2
    FGJG1   3       4       KRT3    chr12   3
    FGJG1   3       4       NKD2    chr5    4
    FGJG1   3       4       MKLN1   chr7    1
    FGEG    3       21      RET     chr10   2       Auto-Dominant-CAKUT
    FGEG    3       21      COLEC12 chr18   6
    FGEG    3       21      NUDT6   chr4    2
    FGEG    3       21      C6orf222        chr6    5

    #output:
    ------------------------
    FamilyName      #SeqMember      #hitGeneNum     GeneList
    S55     3       5       CHRNA7-chr15-3  NCAM2-chr21-3
    FGJG1   3       4       JAK3-chr19-2    KRT3-chr12-3    NKD2-chr5-4     MKLN1-chr7-1
    FGEG    3       21      RET-chr10-2-Auto-Dominant-CAKUT COLEC12-chr18-6 NUDT6-chr4-2    C6or
    f222-chr6-5
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from collections import OrderedDict
    idGeno = OrderedDict() #{idName - [geno list.]}
    for line in sys.stdin:
        line = line.strip()
        if line:
            #print(line)
            ss = line.split(';')
            for i in range(len(ss)):
                temp = ss[i].split('[')
                if len(temp) == 2:
                    ss[i] = temp[1]
                if ss[i][-1] == ']' or ss[i][-1] == ')':
                    ss[i] = ss[i][0:-1]

            #store data.
            for x in ss:
                temp = x.split(':',maxsplit=1)
                if temp[0] not in idGeno:
                    idGeno[temp[0]] = []
                idGeno[temp[0]].append(temp[1])

    #output results
    sys.stdout.write('%s\n'%('\t'.join(idGeno.keys())))
    genoArr = []
    for k in idGeno.keys():
        genoArr.append(idGeno[k])
    #print(genoArr)
    for i in range(len(genoArr[0])):
        out = []
        for x in genoArr:
            out.append(x[i])
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
