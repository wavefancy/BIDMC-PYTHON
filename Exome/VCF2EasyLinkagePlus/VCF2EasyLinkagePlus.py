#!/usr/bin/env python3

"""

    Convert VCF to easyLinkagePlus format. easyLinkagePlus mannual page 20.
    @Author: wavefancy@gmail.com

    Usage:
        VCF2EasyLinkagePlus.py
        VCF2EasyLinkagePlus.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. *** ref allele recode as A, alt allel recode as B, missing allele recode as 0.
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

#output
------------------------
SNP_ID  HG00096 HG00097
rs576797222     AB      AA
rs7757931       AB      BA
rs575636863     BA      AB
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #version 2.0
    # 1. add function to output allele as 0/1 format
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    seqCol = 10 -1 #0 based.

    def recodeOneLine(ss):
        '''recode one line content as easyLinkagePlus format'''
        out = [ss[2]]

        for x in ss[seqCol:]:
            code = ''
            if x[0] == '0':
                code = 'A'
            elif x[0] == '1':
                code = 'B'
            else:
                out.append('00')
                continue

            if x[2] == '0':
                code += 'A'
            elif x[2] == '1':
                code += 'B'
            else:
                out.append('00')
                continue
            out.append(code)
        return out

    outTitle = True
    title = ''
    for line in sys.stdin:
        line = line.strip()
        if line:
            if not line.startswith('#'):
                if outTitle:
                    ss = title.strip().split()
                    out = ['SNP_ID'] + ss[seqCol:]
                    sys.stdout.write('%s\n'%('\t'.join(out)))
                    outTitle = False

                ss = line.split()
                sys.stdout.write('%s\n'%('\t'.join(recodeOneLine(ss))))

            else:
                title = line

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
