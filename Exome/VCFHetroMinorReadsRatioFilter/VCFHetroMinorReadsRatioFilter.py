#!/usr/bin/env python3

"""

    Filter hetero. genotype based on sample minor reads ratio.
    Minor-read ratio (MRR), which was defined as the ratio of reads for the less
    covered allele (reference or variant allele) over the total number of reads
    covering the position at which the variant was called. (Only applied to hetero sites.)

    @Author: wavefancy@gmail.com

    Usage:
        VCFHetroMinorReadsRatioFilter.py -a cutoff [-b|-p]
        VCFHetroMinorReadsRatioFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as miss if AD tage value < 'minDP'.
        2. ***Only apply to hetero sites.***
        3. Output results to stdout.

    Options:
        -a cutoff       Cutoff for MRR, if MRR < this cutoff, set as missing.
        -b              Input is Freebayes format, read alt allele depth from 'DPR' tag.
        -p              Input is Playtypus format, read alt allele depth from 'NV' tag.
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
GT:AD:DP:GQ:PL       0/1:0,2:2:6:90,6,0      0/1     0/1:0,5:5:6:90,6,0

    out vcf example: -a 3
----------------------
PL:GT:GQ        .       .       0/1:0,5:5:6:90,6,0
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.1')
    # version 1.1
    # Add support for multi-allelic sites.
    # Add support for Freebayes input format.

    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = ['AD']
    if args['-b']:
        tags = ['DPR']    #for Freebayes input format.
    if args['-p']:
        tags = ['NV','NR']

    # gatk, AD: reads coverage for ref and alt allele. ref, alt1, alt2, eg 10,20,0.
    # DRP: total, alt1, alt2 ..., eg. 34,19,0 | 10,2.
    # NV: number of reads for alt allele. alt, or alt1, alt2 ...
    # NR: number of reads for all allele. al11, or all1, all2... *** all1 = all2 = all3 ???.

    cutoff = float(args['-a'])

    def reformat(geno):
        '''mask geno type according MRR cutoff.'''
        if geno[0] == '.':
            return '.'
        else:
            if geno[0] != geno[2]: #only check for hetero genotype.
                ss = geno.split(':')
                alt = 0
                total = 0
                #try:
                if args['-p']: #Playtypus format.
                    alt = sum([int(x) for x in ss[ADIndex[0]].split(',')])   #NV
                    total = sum([int(x) for x in ss[ADIndex[1]].split(',')]) #NR
                else:
                    temp = [int(x) for x in ss[ADIndex[0]].split(',')]
                    alt = sum(temp[1:])
                    if args['-b']:            #Freebayes format.
                        total = temp[0]
                    else:
                        total = alt + temp[0] #gatk format.

                if total == 0:
                    return '.'
                else:
                    mrr = min(alt*1.0/total, 1- alt*1.0/total)
                    #sys.stderr.write('%.4f\n'%(mrr))

                    if mrr < cutoff:
                        return '.'
                    else:
                        return geno
            else:
                return geno

    ADIndex = []
    def setADIndex(oldFormatTags):
        global ADIndex
        ss = oldFormatTags.upper().split(':')
        try:
            ADIndex = [ss.index(t) for t in tags]
            #ADIndex = y
        except ValueError:
            sys.stderr.write('ERROR: can not find tag: "%s", from input vcf FORMAT field.\n'%(tags))
            sys.exit(-1)

    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        out = ss[:vcfMetaCols]
        setADIndex(ss[8])               #set index line by line.
        for x in ss[vcfMetaCols:]:
            out.append(reformat(x))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
