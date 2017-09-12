#!/usr/bin/env python3

"""

    Parse Illumina Strand Report file.

    @Author: wavefancy@gmail.com

    Usage:
        ParseIllumiaStrandReport.py
        ParseIllumiaStrandReport.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
            Output five columns: SNP_Name chr pos AlleleA AlleleB.

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
# Strand report file.
------------------------
## Manifest Strand Report
## Input manifest: Multi-EthnicGlobal_D1
## Analysis date: 8/31/2017 3:56:59 PM
## Tool and version: Illumina Manifest Strand Reporter 1.0.0
## Strand(s) reported: Forward/Reverse
Index	SNP_Name	Ilmn_ID	Build	Chr	Coord	Forward_Seq	Forward_Allele1	Forward_Allele2
1	10:100012219-GT	10:100012219-GT-0_B_F_2298934103	37	10	100012219	GCCACCTTGGAGCCATTGAGAGTGAGGAGGTCGTAGTGGGTGAAGACCTCAATGCTGTG[T/G]TAATGCCTGCAGAAGGGGTAGAGCTGTCAGTGCGGCAGCAACAGGAGAGGGTCCTCTCT	T	G
2	10:100013340-CT	10:100013340-CT-0_T_R_2299260687	37	10	100013340	CTAGTGCCAATGCATGGGCAGGCTCTAACCTGTGGCACTGGTGCCAAACCCAGCTATCG[T/C]GTCCAGTCTTTGGACGAAAGTCAGTCCGGCCCAGATTGTAGATCTGTGTGGAGAAGCGC	T	C
3	10:100013459-TCTC-T	10:100013459-TCTC-T-0_M_R_2301504613	37	10	100013459	CAATAGGCGGCGGTATCCGTAGGGCCAGTCCATGTGATCCGCAGACTTGGAGAGGCAGTT[-/CTC]CTCGTGGGCACAATACAGCTGGCTGAGCGGGCGGTCCTCCAAGTAGGCCGTCTCCTGCA	I	D
4	10:100013467-GA	10:100013467-GA-0_T_F_2299260694	37	10	100013467	GCGGTATCCGTAGGGCCAGTCCATGTGATCCGCAGACTTGGAGAGGCAGTTCTCCTCGT[A/G]GGCACAATACAGCTGGCTGAGCGGGCGGTCCTCCAAGTAGGCCGTCTCCTGCACTAGCT	A	G

#output: snpName chr pos allele1 allele2
------------------------
10:100012219-GT 10      100012219       T       G
10:100013340-CT 10      100013340       T       C
10:100013459-TCTC-T     10      100013459       CTC     -
10:100013467-GA 10      100013467       A       G
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #version 2.0
    # 1. add function to output allele as 0/1 format
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # outprefix = args['-o']
    # Column index, 0 based.
    snpNameCol = 1
    chrCol = 4
    posCol = 5
    seqCol = 6

    inData = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if inData:
                ss = line.split()
                out = []
                out.append(ss[snpNameCol])
                out.append(ss[chrCol])
                out.append(ss[posCol])

                try:
                    alleles = ss[seqCol].split('[',1)[1].split(']',1)[0].split('/')
                except IndexError:
                    alleles = ss[snpNameCol].split('-')[1:3]
                    # sys.stderr.write(line+'\n')
                    # sys.exit(-1)
                if len(alleles[1]) > len(alleles[0]):
                    alleles = [alleles[1], alleles[0]]
                [out.append(x) for x in alleles]

                sys.stdout.write('%s\n'%('\t'.join(out)))
            else:
                if line.startswith('Index'):
                    inData = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
