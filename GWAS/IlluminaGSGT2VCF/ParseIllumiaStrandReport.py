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
    refCache = ''

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

    def checkAndGetAllele(chr, start, left, middle, right, alleles):
        # print(start)
        # print(seq)
        seq = getSeq(left,middle,right)
        ref_a = str(refGenome[chr][start:start+len(seq)])
        # print(ref_a)
        # print(seq)
        global refCache
        refCache = ref_a
        # print(ref_a)
        # if ref_a == seq:
        if compareSeqSkipN(ref_a, seq):
            return alleles
        elif compareSeqSkipN(ref_a,str(Seq(seq).reverse_complement())):
            return [str(Seq(x).reverse_complement()) for x in alleles]
        else:
            seq = getSeq(left,str(Seq(middle).reverse_complement()),right)
            if compareSeqSkipN(ref_a, seq):
                return [str(Seq(x).reverse_complement()) for x in alleles]

        return []

    inData = False
    chrSet=set([str(x) for x in range(1,23)])
    [chrSet.add(x) for x in ['X','Y','MT']]
    for line in sys.stdin:
        line = line.strip()
        if line:
            if inData:
                ss = line.split()
                chr = ss[chrCol]
                snpName = ss[snpNameCol]
                pos = int(ss[posCol])

                #*** Try correct annotations ****
                if chr == '0': # read additional info from snpname if read chr and pos info. failed.
                    ctemp = snpName.split(':',1)
                    if len(ctemp) == 2:
                        chr = ctemp[0]
                        pos = int(ctemp[1].split('-',1)[0])
                    # else:
                        # sys.stderr.write('WARN: 0 chr, skipped: %s\n'%(line))
                        # continue

                if chr =='0' and snpName.startswith('chr'):
                    ctemp = snpName.strip('chr').split('_')
                    chr = ctemp[0]
                    pos = int(ctemp[1])

                if chr == '0':
                    sys.stderr.write('WARN: 0 chr, skipped: %s\n'%(line))
                    continue
                if pos <= 0:
                    sys.stderr.write('WARN: 0 pos, skipped: %s\n'%(line))
                    continue

                if chr =='XY':
                    chr ='X'
                if chr == 'M':
                    chr = 'MT'

                if chr not in chrSet:
                    sys.stderr.write('WARN:_No_This_CHR_skipped: %s\n'%(line))
                    continue

                out = []

                out.append(snpName)
                out.append(chr)

                # out.append(ss[posCol])

                try:
                    left = ss[seqCol].split('[',1)
                    right = left[1].split(']',1)

                    alleles = right[0].split('/')
                    left = left[0][(len(left[0])-flankingSize):len(left[0])]
                    right = right[1][0:flankingSize]


                    alleles = ss[seqCol].split('[',1)[1].split(']',1)[0].split('/')
                    alleles = [x.upper() for x in alleles]
                except IndexError:
                    sys.stderr.write('WARN: Parse alleles error, skipped: %s\n'%(line))
                    continue
                    # sys.exit(-1)

                # sn = snpName.split('-')
                # if len(sn)==3 and len(sn[1])>=2 and len(sn[2])>=2: #for complex index.
                #     alleles = sn[1:]
                #     alleles = [x[1:] for x in alleles]

                #matching with ref.
                # seq = getSeq(left, alleles[0], right)
                # *** check wether matching allele1
                start = pos - flankingSize -1
                refPos = pos -1 #shift one base left, from 1 based to 0 based.
                if alleles[0] != '-':
                    # print('here1')
                    results = checkAndGetAllele(chr,start,left,alleles[0],right, alleles)
                else:
                    # pos = pos +1
                    results = checkAndGetAllele(chr,start+1,left,alleles[0],right, alleles)

                # *** if matching allele1 failed, try matching allele2.
                # print(results)
                if not results:
                    # seq = getSeq(left, alleles[1], right)
                    if alleles[1] != '-':
                        # print('here2')
                        results = checkAndGetAllele(chr,start,left,alleles[1],right, alleles)
                    else:
                        # pos = pos +1
                        results = checkAndGetAllele(chr,start+1,left,alleles[1],right, alleles)
                    # results = checkAndGetAllele(chr,start,seq, alleles)
                    # if success swap ref and alt.
                    results = results[::-1]

                # print(results)
                if results:
                    #check and normalize indels.
                    if results[0] == '-' or results[1] == '-':
                        pos = pos -1 #shift include one base more.
                        refPos = refPos -1 #still shift one base left to include that allele.
                        r = str(refGenome[chr][refPos:refPos+1])
                        results = [r + x.strip('-') for x in results]
                        # results = [left[-1] + x.strip('-') for x in results]

                    out.append(str(pos))
                    [out.append(x) for x in results]
                else:
                    sys.stderr.write('WARN: not match with ref:(line) %s; (ref) %s\n'%(line,refCache))
                    #sys.stderr.write('WARN(refSeq): '+str(refGenome[chr][start:start+len(seq)])+'\n')
                    continue
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
