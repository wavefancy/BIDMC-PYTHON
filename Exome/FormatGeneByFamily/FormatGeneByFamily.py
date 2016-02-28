#!/usr/bin/env python3

"""

    Format the output of FamilyHitByGene.py, each family one line.
    @Author: wavefancy@gmail.com

    Usage:
        FormatGeneByFamily.py
        FormatGeneByFamily.py -h | --help | -v | --version | -f | --format

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
    #Output from: FamilyHitByGene.py
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

    sys.stdout.write('FamilyName\t#SeqMember\t#hitGeneNum\tGeneList\n')
    def outputOneFamily(data):
        '''Format one family's data'''
        dd = sorted(data, key=lambda x:len(x), reverse=True)
        sys.stdout.write('%s'%('\t'.join(dd[0][0:3])))
        for d in dd:
            sys.stdout.write('\t%s'%('-'.join(d[3:])))
        sys.stdout.write('\n')

    data = [] #[one line],[],[].....
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if data:
                if ss[0] != data[0][0]:
                    outputOneFamily(data)
                    data = []
                    data.append(ss)
                else:
                    data.append(ss)
            else:
                data.append(ss)

    #output the last one
    if data:
        outputOneFamily(data)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
