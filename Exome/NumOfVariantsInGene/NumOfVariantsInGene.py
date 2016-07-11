#!/usr/bin/env python3

"""

    Count the number of variants in a gene.

    @Author: wavefancy@gmail.com

    Usage:
        NumOfVariantsInGene.py
        NumOfVariantsInGene.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        2. *** Variants have been annotated by gene name (Software: genmod annotate) in INFO fields, format as ;Annotation=GeneName;.
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
    input vcf example(annotated by: genmod annotate):
----------------------
##meta
#CHROM  POS     ID      REF     ALT     QUAL    FILTER  INFO    FORMAT  CH012
chr1    494515  .       T       A       3404.42 PASS    Annotation=OR4F29,OR4F16,OR4F3  GT:AD:DP:GQ:PL:PP       .:.:.:.:.:.
chr1    926133  .       G       A       110.07  PASS    Annotation=SAMD11       GT:AD:DP:GQ:PL:PP       .:.:.:.:.:.
chr1    972540  .       C       G       4280.95 PASS    LEN=1;TYPE=snp;Annotation=PLEKHN1       GT      0|0
chr1    972540  .       C       T       4280.95 PASS    LEN=1;TYPE=snp;Annotation=PLEKHN1       GT      0|0
chr1    972790  .       C       G       11113.8 PASS    Annotation=PLEKHN1      GT:AD:DP:GQ:PL:PP       0/0:5,0:5:22:0,12,180:0,22,206

    output example:
----------------------
GeneName        Count
OR4F29,OR4F16,OR4F3     1
SAMD11  1
PLEKHN1 2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)


    from collections import OrderedDict
    geneNum = OrderedDict() # geneName -> count.
    previous = [] #record previous record, for checking duplicate sites.
    output = False
    maxSplit  = 9
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results. check results from here.
                ss = line.split(None, maxSplit)
                if ss[:2] != previous:
                    previous = ss[:2]
                    geneName = ss[7].split('Annotation=')[1].split(';')[0] #get gene name.
                    if geneName in geneNum:
                        geneNum[geneName] = geneNum[geneName] +1
                    else:
                        geneNum[geneName] = 1

            else:
                if line.startswith('##'):
                    pass
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    pass

    #output results.
    sys.stdout.write('GeneName\tCount\n')
    for k,v in geneNum.items():
        sys.stdout.write('%s\t%d\n'%(k, v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
