#!/usr/bin/env python3

"""

    Use paired T-test to test the balance of reads coverage for ref. and alt allele.
    Only use data from heterozygous sites, all homo or all missing return pvalue 1.
    TWO INDEPENDENT samples T-test, Unequal variance.
    http://docs.scipy.org/doc/scipy-0.16.0/reference/generated/scipy.stats.ttest_ind.html
    @Author: wavefancy@gmail.com

    Usage:
        ReadsCoverageBalanceTest.py
        ReadsCoverageBalanceTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read VCF file from stdin, and output results to stdout.
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
    #Input vcf data.
    ------------------------
##fileformat=VCFv4.0
##FORMAT=<ID=HQ,Number=2,Type=Integer,Description="Haplotype Quality">
#CHROM  POS ID  REF ALT QUAL    FILTER  INFO    FORMAT  NA00001 NA00002 NA00003 NA4 NA5 NA6 NA7
20  14372   rs6054257   G   A   29  PASS    NS=3;DP=14;AF=0.5;DB;H2 GT:AD:DP:GQ:PL 0/1:9,1:10:27:0,27,303   0/1:9,6:15:24:0,24,360   0/1:22,10:32:60:0,60,900 0/1:13,5:18:30:0,30,450 ./.     ./.     ./.
20  14373   rs6054257   G   A   29  PASS    NS=3;DP=14;AF=0.5;DB;H2 GT:AD:DP:GQ:PL ./.     0/1:9,1:10:27:0,27,303     0/1:9,6:15:24:0,24,360     ./.     ./.     ./.     ./.
20  14373   rs6054257   G   A   29  PASS    NS=3;DP=14;AF=0.5;DB;H2 GT:AD:DP:GQ:PL ./.     .     0/1:9,6:15:24:0,24,360     ./.     ./.     ./.     ./.
20  14373   rs6054257   G   A   29  PASS    NS=3;DP=14;AF=0.5;DB;H2 GT:AD:DP:GQ:PL 0/1:3,5,0:8:86:.:.:147,0,86,156,101,257 0/1:1,5,0:6:9:.:.:159,0,9,162,24,185    0/1:7,4,0:11:99:.:.:106     ./.     ./.     ./.     ./.

    #output:
    ------------------------
#CHROM  POS     P_BAL
20      14372   8.3460e-02
20      14373   2.7160e-01
20      14373   1.0000e+00
20      14373   6.3019e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #import numpy as np
    from scipy.stats import ttest_ind
    def unblanceTest(genoArr):
        '''Using two samples T-test for test balance of reads coverage for ref. and alt allele.'''
        ref = []
        alt = []
        for x in genoArr:
            ss = x.split(':')
            try:
                r = int(ss[1].split(',')[0]) #ref coverage
                a = int(ss[2]) - r           #alt coverage   0/1:0,0,0:.:39:0|1:73146216_G_A:39,0,65,42,68,110

                ref.append(r)
                alt.append(a)
            except ValueError:
                pass
        # ref = np.arange(len(genoArr)) #int array
        # alt = np.arange(len(genoArr))
        # for i in range(len(genoArr)):
        #     try:
        #         ss = genoArr[i].split(':')
        #         r = int(ss[1].split(',')[0]) #ref coverage
        #         a = int(ss[2]) - r           #alt coverage
        #         ref[i] = r
        #         alt[i] = a
        #     except ValueError:
        #         sys.stderr.write(genoArr[i])
        #         sys.exit(-1)
        #print(ref)
        #print(alt)
        #at least two elements are necessary for t-test.
        if len(ref) <= 1:
            return 1
        else:
            return ttest_ind(ref, alt, equal_var=False)[1] #only return pvalue.

    seqStartCol = 9
    output = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                ss = line.split()
                ##check format.
                if not ss[8].startswith('GT:AD:DP'):
                    sys.stderr.write('VCF format ERROR: VCF format should start with these 3 flags: GT:AD:DP\n')
                    sys.exit(-1)

                #prepare output
                out = ss[0:2]
                hetro = [x for x in ss[seqStartCol:] if x[0] != '.' and x[0] != x[2]]
                if hetro:
                    #print(unblanceTest(hetro))
                    out.append('%.4e'%(unblanceTest(hetro)))
                else: #all homo or all missing sites.
                    out.append('1')

                sys.stdout.write('%s\n'%('\t'.join(out)))

            else:
                if line.startswith('##'):
                    pass
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    sys.stdout.write('#CHROM\tPOS\tP_BAL\n')


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
