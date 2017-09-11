#!/usr/bin/env python3

"""

    Covert illumina genotyping results (GSGT file) to plink tped/tfam file.

    @Author: wavefancy@gmail.com

    Usage:
        IlluminaGSGT2TPedFam.py -o prefix [-g float]
        IlluminaGSGT2TPedFam.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin
        2. *** Multiple input files can be piped together,
            this script will automatically ommit header section in each file ***
        3. See example by -f.

    Options:
        -o prefix     Set output tped/tfam file prefix.
        -g float      Set GC score threshold, default 0.5.
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
Num SNPs,1735862
Total SNPs,1748250
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

    outprefix = args['-o']
    # Column index, 0 based.
    snpNameCol = 0
    sampleCol = 1
    allele1Col = 2
    allele2Col = 3
    GCScoreCol = 4
    GCScoreThreshold  = 0.5
    if args['-g']:
        GCScoreThreshold = float(args['-g'])

    data = [] #[[...],[...]] genotype array.
    snpIndexMap = {} # snpName -> row index for snp.
    sampleIndexMap = {} #sampleName -> colIndex for snp.

    missingGenotype = '0\t0'

    #initialize data.
    data = [[missingGenotype]]
    def expandOneRow(data):
        '''expand the data matrix one row'''
        row = [missingGenotype for x in data[0]]
        data.append(row)

    def expandOneCol(data):
        '''expand the data matrix one Column'''
        [x.append(missingGenotype) for x in data]

    def getSnpIndex(snpID, snpIndexMap, data):
        if snpIndexMap:
            if snpID in snpIndexMap:
                return snpIndexMap[snpID]
            else:
                expandOneRow(data)
                snpIndexMap[snpID] = len(data) -1
                return len(data) -1
        else:
            snpIndexMap[snpID] = 0
            return 0

    def getSampleIndex(sampleID, sampleIndexMap, data):
        if sampleIndexMap:
            if sampleID in sampleIndexMap:
                return sampleIndexMap[sampleID]
            else:
                expandOneCol(data)
                sampleIndexMap[sampleID] = len(data[0]) -1
                return len(data[0]) -1
        else:
            sampleIndexMap[sampleID] = 0
            return 0

    def addOneEntry(snpID, sampleID, genotype, data, snpIndexMap, sampleIndexMap):
        '''Add one data entry to data matrix'''
        # print(data)
        data[getSnpIndex(snpID, snpIndexMap, data)][getSampleIndex(sampleID, sampleIndexMap, data)] = genotype

    inData = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.startswith('[Header]'):
                inData = False
                continue
            if line.startswith('SNP Name'):
                inData = True
                continue

            if inData:
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
                    geno = allele1 + '\t' + allele2

                addOneEntry(snpID,sampleID, geno, data, snpIndexMap, sampleIndexMap)

    #output data.
    snps = sorted(snpIndexMap.keys())
    samples = sorted(sampleIndexMap.keys())

    def checkAndFixAllele(allele, snpArray):
        '''replace I and D annotation in allele'''
        if allele == 'I':
            return snpArray[1] if snpArray[1] > snpArray[2] else snpArray[2]
        elif allele == 'D':
            return snpArray[1] if snpArray[1] < snpArray[2] else snpArray[2]
        else:
            return allele

    pedf = open(outprefix+'.tped','w')
    famf = open(outprefix+'.tfam','w')

    # print(data)
    for snp in snps:
        out = []
        ss = snp.split('-')
        chr_pos = ss[0].split(':')

        out.append(chr_pos[0])
        out.append('.')
        out.append('0')
        out.append(chr_pos[1])

        for s in samples:
            for g in data[snpIndexMap[snp]][sampleIndexMap[s]].split():
                out.append(checkAndFixAllele(g, ss))

        pedf.write('%s\n'%('\t'.join(out)))

    #output tfam
    for s in samples:
        out = [s,s,'0','0','0','0']
        famf.write('%s\n'%('\t'.join(out)))

    pedf.flush()
    pedf.close()
    famf.flush()
    famf.close()

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
