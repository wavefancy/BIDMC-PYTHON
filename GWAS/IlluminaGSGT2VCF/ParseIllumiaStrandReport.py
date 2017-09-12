#!/usr/bin/env python3

"""

    Parse Illumina Strand Report file, matching with reference fasta file.
    *** The output AlleleA is ref allele, AlleleB is alt allele for vcf file.

    @Author: wavefancy@gmail.com

    Usage:
        ParseIllumiaStrandReport.py  -r <ref.fa>
        ParseIllumiaStrandReport.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
            Output five columns: SNP_Name chr pos AlleleA AlleleB.

    Options:
        -r <ref.fa>   Reference fasta file.
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

    from pyfaidx import Fasta
    from Bio.Seq import Seq
    refFile = args['-r']
    refGenome = Fasta(refFile, sequence_always_upper=True)
    # outprefix = args['-o']
    # Column index, 0 based.
    snpNameCol = 1
    chrCol = 4
    posCol = 5
    seqCol = 6
    flankingSize = 10

    def getSeq(left, middle, right):
        '''Get the whole seq peace for matching'''
        if middle == '-':
            return (left + right).upper()
        else:
            return (left + middle + right).upper()

    def compareSeqSkipN(seq1, seq2):
        '''Compare seq, do not compare site with allele N'''
        for x,y in zip(seq1, seq2):
            if x == 'N' or y == 'N':
                continue
            elif x != y:
                return False
        return True

    def checkAndGetAllele(chr, start, seq, alleles):
        # print(start)
        # print(seq)
        ref_a = str(refGenome[chr][start:start+len(seq)])
        # print(ref_a)
        # if ref_a == seq:
        if compareSeqSkipN(ref_a, seq):
            return alleles
        # elif ref_a == str(Seq(seq).reverse_complement()):
        elif compareSeqSkipN(ref_a, str(Seq(seq).reverse_complement())):
            return [str(Seq(x).reverse_complement()) for x in alleles]
        else:
            return []

    inData = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if inData:
                ss = line.split()
                chr = ss[chrCol]
                if chr == '0':
                    continue
                if chr =='XY':
                    chr ='X'
                out = []
                out.append(ss[snpNameCol])
                out.append(ss[chrCol])
                pos = int(ss[posCol])
                # out.append(ss[posCol])

                try:
                    left = ss[seqCol].split('[',1)
                    right = left[1].split(']',1)

                    alleles = right[0].split('/')
                    left = left[0][(len(left[0])-flankingSize):len(left[0])]
                    right = right[1][0:flankingSize]


                    alleles = ss[seqCol].split('[',1)[1].split(']',1)[0].split('/')
                except IndexError:
                    sys.stderr.write('WARN: Parse alleles error, skipped: %s\n'%(line))
                    continue
                    # sys.exit(-1)

                #matching with ref.
                seq = getSeq(left, alleles[0], right)
                start = pos - flankingSize -1
                if alleles[0] != '-':
                    results = checkAndGetAllele(chr,start,seq, alleles)
                else:
                    results = checkAndGetAllele(chr,start+1,seq, alleles)


                if not results:
                    seq = getSeq(left, alleles[1], right)
                    if alleles[1] != '-':
                        results = checkAndGetAllele(chr,start,seq, alleles)
                    else:
                        results = checkAndGetAllele(chr,start+1,seq, alleles)
                    # results = checkAndGetAllele(chr,start,seq, alleles)

                if results:
                    #check and normalize indels.
                    if results[0] == '-' or results[1] == '-':
                        pos = pos -1
                        results = [left[-1] + x.strip('-') for x in results]

                    out.append(str(pos))
                    [out.append(x) for x in results]
                else:
                    sys.stderr.write(line+'\n')
                    sys.stderr.write(str(refGenome[chr][start:start+len(seq)])+'\n')
                    # sys.exit(-1)

                # print(line)
                # print(str(refGenome[chr][start:start+len(seq)]))
                sys.stdout.write('%s\n'%('\t'.join(out)))
            else:
                if line.startswith('Index'):
                    inData = True

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
