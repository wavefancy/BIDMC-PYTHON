#!/usr/bin/env python3

"""
    Prepare input file for RIGER.
    @Author: wavefancy@gmail.com

    Usage:
        RIGERinput.py
        RIGERinput.py -h | --help | -v | --version | -f | --format

    Notes:
        2. Read results from stdin, and output results to stdout.
        3. See example by -f.

    Options:
        -a string     Anchor string for guide-RNA, default(GTGGAAAGGACGAAACACCG,GTTTTAGAGCTAGAAATAGC)
        -l int        Length for guide-RNA, default 20.
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
    # input, columns: sgRNA_name, GeneName, ctrl_sgRNA_count, treatment_sgRNA_count
    ------------------------
sgRNA   GENE    ctrl    treatment
A1  A   2   10
A2  A   3   30
B1  B   30  2
B2  B   10  5
    # output:
------------------------
WELL_ID,GENE_ID,biorep1
A1,A,1.8168e+00
A2,A,2.8965e+00
B1,B,-3.4269e+00
B2,B,-9.3218e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    data = [[],[],[],[]] #array for sgRNA_name, geneName, ctrl_sgRNA_count, treatment_sgRNA_count.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                cn = float(ss[2]) +1 #ctrl count
                tn = float(ss[3]) +1 #treatment_sgRNA_count.

                data[0].append(ss[0])
                data[1].append(ss[1])
                data[2].append(cn)
                data[3].append(tn)
            except ValueError:
                sys.stderr.write('Warning, parse value error: %s\n'%(line))

    #normalized
    cn_total = sum(data[2])
    tn_total = sum(data[3])
    nor_cn = [x/cn_total for x in data[2]]
    nor_tn = [x/tn_total for x in data[3]]
    #
    # print(nor_cn)
    # print(nor_tn)

    #log2 flod change.
    import math
    log_change = [math.log2(x/y) for x,y in zip(nor_tn, nor_cn)]

    #outpu results.
    sys.stdout.write('WELL_ID,GENE_ID,biorep1\n')
    for i in range(len(log_change)):
        sys.stdout.write('%s,%s,%.4e\n'%(data[0][i], data[1][i], log_change[i]))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
