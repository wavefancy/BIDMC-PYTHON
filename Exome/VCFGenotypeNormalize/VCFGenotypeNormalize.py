#!/usr/bin/env python3

"""

    Normalization of VCF genotype.

    @Author: wavefancy@gmail.com

    Usage:
        VCFGenotypeNormalize.py
        VCFGenotypeNormalize.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, and output results to stdout.
        2. Normalize genotpye, change
            [1/0, 2/1, ./1, ./0] -> [0/1, 1/2, 1/., 0/.].
            RULE: (firstAllele < secondAllele), except '.'.
            ***Do not apply this scripts to phased VCF file.***

    Options:
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
    input vcf example(abstracted):
----------------------
GT:AD:DP:GQ:PL       2/1:2,0:2:6:0,6,54      1/0:1,1:2:21:21,0,22    ./1

    out vcf example: -t PL,GT,GQ
----------------------
GT:AD:DP:GQ:PL       1/2:2,0:2:6:0,6,54      0/1:1,1:2:21:21,0,22    1/.:.:.:.:.
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.

    def reformat(geno):
        '''reformat a genotype record
            [1/0, 2/1, ./1, ./0] -> [0/1, 1/2, 1/., 0/.].
            RULE: (firstAllele < secondAllele), except '.'.
        '''
        ss = geno.split(':')
        if len(ss[0]) == 1: #missing
            return geno

        if ss[0][0] == ss[0][2]:
            return geno
        else:
            if ss[0][2] == '.':
                return geno
            else:
                if ss[0][0] == '.' or ss[0][0] > ss[0][2]:
                    tmp = list(geno)
                    tmp[0], tmp[2] = tmp[2],tmp[0]
                    return ''.join(tmp)
                else:
                    return geno

    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        out = ss[:vcfMetaCols]
        for x in ss[vcfMetaCols:]:
            out.append(reformat(x))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
