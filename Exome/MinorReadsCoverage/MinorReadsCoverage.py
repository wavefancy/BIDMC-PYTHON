#!/usr/bin/env python3

"""

    Calculate minor reads coverage.
    Minor-read ratio (MRR), which was defined as the ratio of reads for the less
    covered allele (reference or variant allele) over the total number of reads
    covering the position at which the variant was called. (Only applied to hetero sites.)

    @Author: wavefancy@gmail.com

    Usage:
        MinorReadsCoverage.py (-o| -f cutoff)
        MinorReadsCoverage.py -h | --help | -v | --version

    Notes:
        1. Read vcf file from stdin.
        2. MinorReadsCoverage only calculated from hetero sites.
        3. Output results to stdout.

    Options:
        -o              Output MinorReadsCoverage statistics.
        -f cutoff       Filter out sites if MRC < cutoff.
        -t tags         Comma separated tag list.
        -h --help       Show this screen.
        -v --version    Show version.
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

    # if(args['--format']):
    #     ShowFormat()
    #     sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = ['GT','AD']       #GATK, AD: reads depth for ref and alt allele.

    cutoff = 1
    if args['-f']:
        cutoff = float(args['-f'])

    # def depth(geno):
    #     '''reformat a genotype record'''
    #     ss = geno.split(':')
    #     if ss[outGenoArrayIndex[0]][0] != '.' and :
    #
    #
    #     try:
    #         out = [ss[x] for x in outGenoArrayIndex]
    #         return out
    #     except IndexError:
    #         sys.stderr.write('ERROR: Index out of range. geno: %s, out index: %s\n'%(geno, str(outGenoArrayIndex)))
    #         sys.exit(-1)

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
    if args['-f']:
        sys.stdout.write(str(infile.header))

    if args['-o']:
        sys.stdout.write('#CHROM\tPOS\tREF\tALT\tMRR\n')
        
    for line in infile:
        ss = str(line).strip().split()

        setoutGenoArrayIndex(ss[8])     #Check format line by line.
        ref = 0
        alt = 0
        for x in ss[vcfMetaCols:]:
            #if not outGenoArrayIndex:
            #    setoutGenoArrayIndex(ss[8])
            #out.append(reformat(x))
            temp = x.split(':')
            if temp[outGenoArrayIndex[0]][0] != '.' and temp[outGenoArrayIndex[0]][0] != temp[outGenoArrayIndex[0]][2]:
                ad =[int(y) for y in temp[outGenoArrayIndex[1]].split(',')]
                ref += ad[0]
                alt += sum(ad[1:])


        out = ss[:2] + ss[3:5]
        mrc = 1
        if ref == 0 and alt == 0:
            mrc = 1
        else:
            minor = min(alt*1.0/(alt + ref), ref*1.0/(alt + ref))
            mrc = minor

        if args['-o']:
            out = ss[:2] + ss[3:5] + ['%.4f'%(mrc)]
            sys.stdout.write('%s\n'%('\t'.join(out)))

        if args['-f']:
            if mrc >= cutoff:
                sys.stdout.write('%s'%(str(line)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
