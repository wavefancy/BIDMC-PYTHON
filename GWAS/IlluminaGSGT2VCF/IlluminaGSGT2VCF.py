#!/usr/bin/env python3

"""

    Covert illumina genotyping results (GSGT file) to VCF file.

    @Author: wavefancy@gmail.com

    Usage:
        IlluminaGSGT2VCF.py [-g float]
        IlluminaGSGT2VCF.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin.
        2. *** Multiple input files can be piped together,
            this script will automatically ommit header section in each file ***
        3. *** Only process varints on autochromosome,1..22, skip X, Y and MT. ***
        4. See example by -f.

    Options:
        -g float      Set GC score threshold, default 0.15.
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
# GSGT file.
------------------------
[Header]
GSGT Version,1.9.4
Processing Date,8/31/2017 4:24 PM
Content,,Multi-EthnicGlobal_D1.bpm
Num SNPs,1000
Total SNPs,1000
Num Samples,376
Total Samples,376
File ,1 of 4
[Data]
SNP Name,Sample Name,Allele1 - Forward,Allele2 - Forward,GC Score,X,Y,B Allele Freq,Log R Ratio
10:100012219-GT,WG0283937-DNA_A05_LPC6,G,G,0.4669,0.037,0.801,1.0000,-0.1182
10:100013340-CT,WG0283937-DNA_A05_LPC6,C,C,0.4920,0.037,0.791,1.0000,-0.2098
10:100013459-TCTC-T,WG0283937-DNA_A05_LPC6,I,I,0.4144,0.059,1.220,1.0000,0.0099
10:100013459-TCTC-T,WG0283937-DNA_A10_LPC5,D,D,0.4144,0.059,1.220,1.0000,0.0099
10:100013467-GA,WG0283937-DNA_A05_LPC6,G,G,0.3770,0.068,1.409,1.0000,0.0274
10:100015474-GA,WG0283937-DNA_A05_LPC6,G,G,0.4654,0.027,0.797,1.0000,-0.0228
10:100016685-CT,WG0283937-DNA_A05_LPC6,C,C,0.3828,0.032,0.258,1.0000,-0.1234
10:100017801-CT,WG0283937-DNA_A05_LPC6,C,C,0.4633,0.035,0.887,1.0000,-0.0630
10:100017854-CT,WG0283937-DNA_A05_LPC6,C,C,0.4814,0.028,0.750,1.0000,0.0980
------------------------

#cat test.txt | python3 IlluminaGSGT2TPedFam.py -o myout -g 0.4
# myout.tped
------------------------
10      .       0       100012219       G       G       0       0
10      .       0       100013340       C       C       0       0
10      .       0       100013459       TCTC    TCTC    T       T
10      .       0       100013467       0       0       0       0
10      .       0       100015474       G       G       0       0
10      .       0       100016685       0       0       0       0
10      .       0       100017801       C       C       0       0
10      .       0       100017854       C       C       0       0

# myout.tfam
------------------------
WG0283937-DNA_A05_LPC6  WG0283937-DNA_A05_LPC6  0       0       0       0
WG0283937-DNA_A10_LPC5  WG0283937-DNA_A10_LPC5  0       0       0       0
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
    snpNameCol = 0
    sampleCol = 1
    allele1Col = 2
    allele2Col = 3
    GCScoreCol = 4
    GCScoreThreshold  = 0.15
    if args['-g']:
        GCScoreThreshold = float(args['-g'])

    chrSet = set()
    [chrSet.add(str(x)) for x in range(1,23)]
    # print(chrSet)

    data = [] #[[...],[...]] genotype array.
    from collections import OrderedDict
    snpIndexMap = OrderedDict() # snpName -> row index for snp.
    sampleIndexMap = OrderedDict() #sampleName -> colIndex for snp.

    missingGenotype = '.'

    CacheLine = ''

    def getSnpIndex(snpID, snpIndexMap):
        if snpIndexMap:
            if snpID in snpIndexMap:
                return snpIndexMap[snpID]
            else:
                snpIndexMap[snpID] = len(snpIndexMap)
                return len(snpIndexMap) -1
        else:
            snpIndexMap[snpID] = 0
            return 0

    def getSampleIndex(sampleID, sampleIndexMap):
        if sampleIndexMap:
            if sampleID in sampleIndexMap:
                return sampleIndexMap[sampleID]
            else:
                sampleIndexMap[sampleID] = len(sampleIndexMap)
                return len(sampleIndexMap) -1
        else:
            sampleIndexMap[sampleID] = 0
            return 0

    def addOneEntry(snpID, sampleID, genotype, data, snpIndexMap, sampleIndexMap):
        '''Add one data entry to data matrix'''
        # print(data)
        data[getSnpIndex(snpID, snpIndexMap)][getSampleIndex(sampleID, sampleIndexMap)] = genotype

    def getSNPAlleles(snpName):
        '''Get the two alleles of a snp.'''
        ss = snpName.split('-')
        if len(ss) == 3:
            return ss[1:]
        else:
            return [ss[1][0], ss[1][1]]

    from Bio.Seq import Seq
    def checkAndFixAllele(allele, snpName):
        '''replace I and D annotation in allele'''
        alleles = getSNPAlleles(snpName) + ['I', 'D']
        if allele not in alleles:
            allele = Seq(allele).reverse_complement()

        if allele == alleles[0]:
            return '0'
        elif allele == alleles[1]:
            return '1'
        elif allele == 'I':
            return '0' if len(alleles[0]) > len(alleles[1]) else '1'
        elif allele == 'D':
            return '1' if len(alleles[0]) > len(alleles[1]) else '0'
        else:
            sys.stderr.write('Can not parse allele at: ' + snpName + ', input allele is: '+allele)
            sys.stderr.write('\n'+CacheLine+'\n')
            sys.exit(-1)

    inData = False
    totalSNPs = -1;
    totalSamples = -1;
    import numpy as np
    for line in sys.stdin:
        line = line.strip()
        if line:
            if totalSNPs < 0:
                if line.startswith('Total SNPs'):
                    totalSNPs = int(line.split(',')[1])
            if totalSamples < 0:
                if line.startswith('Total Samples'):
                    totalSamples = int(line.split(',')[1])
                    # print(totalSNPs)
                    # print(totalSamples)
                    data = np.ndarray(shape=(totalSNPs, totalSamples), dtype=object)
                    data.fill('.')

            if line.startswith('[Header]'):
                inData = False
                continue
            if line.startswith('SNP Name'):
                inData = True
                continue

            if inData:
                CacheLine = line
                chrs = line.split(':',1)[0]
                if chrs not in chrSet:
                    continue

                ss = line.split(',')
                snpID = ss[snpNameCol]
                sampleID = ss[sampleCol]
                allele1 = ss[allele1Col]
                allele2 = ss[allele2Col]
                GCScore = float(ss[GCScoreCol])

                geno = ''
                if GCScore < GCScoreThreshold:
                    geno =  missingGenotype
                else:
                    geno = checkAndFixAllele(allele1, snpID) + '/' + checkAndFixAllele(allele2, snpID)

                addOneEntry(snpID,sampleID, geno, data, snpIndexMap, sampleIndexMap)

    #output data.
    snps = snpIndexMap.keys()
    samples = sampleIndexMap.keys()
    # print(samples)

    #output titile.
    sys.stdout.write('##fileformat=VCFv4.2\n')
    sys.stdout.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    c = '''##contig=<ID=1,length=249250621,assembly=GRCh37>
##contig=<ID=2,length=243199373,assembly=GRCh37>
##contig=<ID=3,length=198022430,assembly=GRCh37>
##contig=<ID=4,length=191154276,assembly=GRCh37>
##contig=<ID=5,length=180915260,assembly=GRCh37>
##contig=<ID=6,length=171115067,assembly=GRCh37>
##contig=<ID=7,length=159138663,assembly=GRCh37>
##contig=<ID=8,length=146364022,assembly=GRCh37>
##contig=<ID=9,length=141213431,assembly=GRCh37>
##contig=<ID=10,length=135534747,assembly=GRCh37>
##contig=<ID=11,length=135006516,assembly=GRCh37>
##contig=<ID=12,length=133851895,assembly=GRCh37>
##contig=<ID=13,length=115169878,assembly=GRCh37>
##contig=<ID=14,length=107349540,assembly=GRCh37>
##contig=<ID=15,length=102531392,assembly=GRCh37>
##contig=<ID=16,length=90354753,assembly=GRCh37>
##contig=<ID=17,length=81195210,assembly=GRCh37>
##contig=<ID=18,length=78077248,assembly=GRCh37>
##contig=<ID=19,length=59128983,assembly=GRCh37>
##contig=<ID=20,length=63025520,assembly=GRCh37>
##contig=<ID=21,length=48129895,assembly=GRCh37>
##contig=<ID=22,length=51304566,assembly=GRCh37>
##contigLengthInfo=/cromwell_root/broad-references/hg19/v0/Homo_sapiens_assembly19.fasta
'''
    sys.stdout.write('%s'%(c))
    out = '#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT'.split()
    [out.append(x) for x in samples]
    sys.stdout.write('%s\n'%('\t'.join(out)))

    # print(data)
    for snp in snps:
        geno = data[snpIndexMap[snp]][:len(sampleIndexMap)]
        out = []
        ss = snp.split('-')
        out = ss[0].split(':')
        out.append('.')
        [out.append(x) for x in getSNPAlleles(snp)]
        out.append('.')
        out.append('.')
        out.append('.')
        out.append('GT')
        sys.stdout.write('%s\t'%('\t'.join(out)))
        sys.stdout.write('%s\n'%('\t'.join(geno)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
