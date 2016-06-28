#!/usr/bin/env python3

"""
    Sampling haplotype based on haplotype frequency, and output as fasta format.
    @Author: wavefancy@gmail.com

    Usage:
        SampleHap2Fasta.py -n nhap -l label [-s indexstart]
        SampleHap2Fasta.py -h | --help | -v | --version | -f | --format

    Notes:
        2. Read results from stdin, and output results to stdout.
        3. See example by -f.

    Options:
        -n int        Number of haplotypes to output.
        -l string     Fasta name label.
        -s int        Start number for haplotype index, default 1.
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

    nhap = int(args['-n'])
    label = args['-l']
    start = 1
    if args['-s']:
        start = int(args['-s'])

    hapfreq = []
    haps = [] #[[hap1],[hap2]....]

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if not hapfreq:
                hapfreq = [float(x) for x in ss]
                haps = [[] for x in ss]
            else:
                for h,s in zip(haps, ss):
                    h.append(s)

    import numpy
    oHapFre = [x/sum(hapfreq) for x in hapfreq]
    # print(oHapFre)
    oHapNum = [int(numpy.rint(x*nhap)) for x in oHapFre]
    # print(oHapNum)
    index = start
    for f,h in zip(oHapNum, haps):
        for x in range(f):
            sys.stdout.write('>%d.%s\n'%(index, label))
            sys.stdout.write('%s\n'%(''.join(h)))
            index += 1

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
