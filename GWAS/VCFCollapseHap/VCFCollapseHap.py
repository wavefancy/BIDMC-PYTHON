#!/usr/bin/env python3

"""

    Collapse phased haplotype as single base presentatoin.
    1. Only consider top two major haplotypes,
        set other haplotype as missing.
    @Author: wavefancy@gmail.com

    Usage:
        VCFCollapseHap.py
        VCFCollapseHap.py -h | --help | -v | --version | -f | --format

    Notes:
        1. *** Input VCF should be phased and no missing. ***
        2. Read results from stdin, and output results to stdout.
        3. See example by -f.

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
    #in vcf.txt
    ------------------------
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  HG00096 HG00097
6       29523659        rs576797222     AC      A       100     PASS    .   .   0|1     0|0
6       29523670        rs7757931       C       A       100     PASS    .   .   0|1     1|0
6       29523699        rs575636863     C       A       100     PASS    .   .   1|0     0|1

    #output:
    ------------------------
CHR     POS     ID      0.5000  0.2500  0.2500
6       29523659        rs576797222     AC      A       AC
6       29523670        rs7757931       C       A       A
6       29523699        rs575636863     A       C       C
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    seqCol = 10 -1 #0 based.

    #load all data.
    data = [] #[[allele code],[allele code] ... ], each line one haplotpe.
    metaData = [] #chr and pos
    title = ''
    for line in sys.stdin:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                ss = line.split()
                #metaData.append(ss[:5])
                metaData.append(ss[:seqCol])
                ss = ss[seqCol:]
                if not data:
                    for x in range(2*len(ss)): # each person two haps.
                        data.append([])

                for x in range(len(ss)):
                    data[2*x].append(ss[x][0])
                    data[2*x +1 ].append(ss[x][2])
            else:
                if line.startswith('#CHROM') or line.startswith('#chrom'):
                    title = line
                else:
                    sys.stdout.write('%s\n'%(line))

    #hap frequency
    haps = {}   # hapseq -> hapNum
    hapData = [] # all haplotpes.
    for x in data:
        hap = ''.join(x)
        hapData.append(hap)
        if hap not in haps:
            haps[hap] = 1
        else:
            haps[hap] = haps[hap] + 1

    #sort by haplotype frequency.
    hap_fre = [] # [(hap, freq), () ... ]
    for k,v in haps.items():
        hap_fre.append((k,v/len(data)))
    hap_fre = sorted(hap_fre, key=lambda x : x[1], reverse=True)
    #print(hap_fre)
    outAlleles = []
    for x in hapData:
        if x == hap_fre[0][0]:
            outAlleles.append('A')
        elif x == hap_fre[1][0]:
            outAlleles.append('G')
        else:
            outAlleles.append('.')


    #output results
    # sys.stdout.write('CHR\tPOS\tID')
    # for _,f in hap_fre:
    #     sys.stdout.write('\t%.4f'%(f))
    # sys.stdout.write('\n')
    #

    #get haplotype configuration.
    hapcodes = []
    for h, _ in hap_fre:
        allele = []
        for i in range(len(metaData)):
            if h[i] == '0':
                allele.append( metaData[i][3])
            elif h[i] == '1':
                allele.append( metaData[i][4])
            else:
                sys.stderr.write('ERROR: can not recognize this genotype code: %s\n'%(h[i]))
                sys.exit(status=-1)
        hapcodes.append('|'.join(allele))
            #sys.stdout.write('\t%s'%(allele))
        #sys.stdout.write('\n')
    sys.stdout.write('#Tophap1, A: %s, fre: %.4f\n'%(hapcodes[0], hap_fre[0][1]))
    sys.stdout.write('#Tophap2, G: %s, fre: %.4f\n'%(hapcodes[1], hap_fre[1][1]))
    sys.stdout.write('%s\n'%(title))

    out = metaData[0][:seqCol]
    out[3] = 'A'
    out[4] = 'G'
    for i in range(0,len(outAlleles),2):
        out.append(outAlleles[i] + '|' + outAlleles[i+1])

    sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
