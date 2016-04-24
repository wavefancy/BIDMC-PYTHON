#!/usr/bin/env python3

"""

    Re-format and/or subset format fields for vcf file.

    @Author: wavefancy@gmail.com

    Usage:
        VCFreFORMATGeno.py -t tags
        VCFreFORMATGeno.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, only output listed tags for FORMAT field.
            keep output order decleared in -t.
        3. Output results to stdout.

    Options:
        -t tags         Comma separated tag list.
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
GT:AD:DP:GQ:PL       1/1:0,9:9:27:258,27,0   ./.     1/1:0,2:2:6:49,6,0

    out vcf example: -t PL,GT,GQ
----------------------
PL:GT:GQ        258,27,0:1/1:27      .       49,6,0:1/1:6
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.1')
    # version 1.1
    # Check format at each line. FORMAT may different line by line.
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = args['-t'].upper().split(',')
    otags = ':'.join(tags)

    def reformat(geno):
        '''reformat a genotype record'''
        if geno[0] == '.':
            return '.'
        else:
            ss = geno.split(':')
            #out = [ss[x] for x in outGenoArrayIndex]
            #return ':'.join(out)
            try:
                out = [ss[x] for x in outGenoArrayIndex]
                return ':'.join(out)
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
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        out = ss[:vcfMetaCols]
        out[8] = otags                  #update tags genotyp tags info.
        setoutGenoArrayIndex(ss[8])     #Check format line by line.
        for x in ss[vcfMetaCols:]:
            #if not outGenoArrayIndex:
            #    setoutGenoArrayIndex(ss[8])
            out.append(reformat(x))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
