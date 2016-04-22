#!/usr/bin/env python3

"""

    Filter hetero. genotype based on sample AD(read depth) tags.

    @Author: wavefancy@gmail.com

    Usage:
        VCFDPFilter.py -a minDP
        VCFDPFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as miss if AD tage value < 'minDP'.
        2. ***Only apply to hetero sites.***
        3. Output results to stdout.

    Options:
        -a minDP        Minimum value for alt allele read depth,int.
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
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    tags = 'AD'
    altMinDP = int(args['-a'])

    def reformat(geno):
        '''mask geno type according DP value.'''
        if geno[0] == '.':
            return '.'
        else:
            if geno[0] != geno[2]: #only check for hetero genotype.
                ss = geno.split(':')
                try:
                    altDPvalue = int(ss[ADIndex].split(',')[1]) #read depth for alt allele.
                    if altDPvalue < altMinDP:
                        return '.'
                    else:
                        return geno
                except (IndexError,ValueError) as e:
                    return '.'
            else:
                return geno

    ADIndex = -1
    def setADIndex(oldFormatTags):
        global ADIndex
        ss = oldFormatTags.upper().split(':')
        try:
            y = ss.index(tags)
            ADIndex = y
        except ValueError:
            sys.stderr.write('ERROR: can not find tag: "%s", from input vcf FORMAT field.\n'%(x))
            sys.exit(-1)

    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split()
        out = ss[:vcfMetaCols]
        for x in ss[vcfMetaCols:]:
            if ADIndex < 0:
                setADIndex(ss[8])
            out.append(reformat(x))

        sys.stdout.write('%s\n'%('\t'.join(out)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
