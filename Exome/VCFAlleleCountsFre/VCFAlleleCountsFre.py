#!/usr/bin/env python3

"""

    Count the number of alleles for VCF.
    alt, ref allele count, and alt allele frequency.

    @Author: wavefancy@gmail.com

    Usage:
        VCFAlleleCountsFre.py
        VCFAlleleCountsFre.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        3. Output results to stdout.

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
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile


    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = ['GT']

    def getGeno(geno):
        '''get genotype info.'''
        if geno[0] == '.':
            return './.'
        else:
            ss = geno.split(':')
            try:
                return ss[outGenoArrayIndex[0]]
            except IndexError:
                sys.stderr.write('ERROR: Index out of range. geno: %s, out index: %s\n'%(geno, str(outGenoArrayIndex)))
                sys.exit(-1)

    outGenoArrayIndex = []
    def setoutGenoArrayIndex(oldFormatTags):
        outGenoArrayIndex.clear()
        ss = oldFormatTags.upper().split(':')
        for x in tags:
            try:
                y = ss.index(x)
                outGenoArrayIndex.append(y)
            except ValueError:
                sys.stderr.write('ERROR: can not find tag: "%s", from input vcf FORMAT field.\n'%(x))
                sys.exit(-1)

    infile = VariantFile('-', 'r')
    #sys.stdout.write(str(infile.header))
    sys.stdout.write('#CHROM\tPOS\tREF\tALT\tTotalCount\tAltCount\tAltFre\n')
    for line in infile:
        ss = str(line).strip().split()
        out = ss[0:2] + ss[3:5]
        setoutGenoArrayIndex(ss[8])
        allels = []
        for x in ss[vcfMetaCols:]:
            genotye = getGeno(x)
            if genotye[0] != '.':
                allels.append(genotye[0])
            if genotye[2] != '.':
                allels.append(genotye[2])

        alt = 0
        ref = 0
        for x in allels:
            if x == '0':
                ref += 1
            else:
                alt += 1

        if alt + ref == 0:
            sys.stdout.write('%s\t%d\t%d\tNA\n'%('\t'.join(out), ref+alt, alt))
        else:
            sys.stdout.write('%s\t%d\t%d\t%.4f\n'%('\t'.join(out), ref+alt, alt, alt*1.0/(alt + ref)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
