#!/usr/bin/env python3

"""

    Compute the last non-NA value for each category.
    @Author: wavefancy@gmail.com

    Usage:
        VCFHapFreq.py -c int
        VCFHapFreq.py -h | --help | -v | --version | -f | --format

    Notes:
        1. *** Input file should be ordered ***
           When check last non-NA value, program use input order.
        2. Read results from stdin, and output results to stdout.
        3. See example by -f.

    Options:
        -c int        Column index for category name, index starts from 1.
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

    col = int(args['-c']) -1
    from collections import OrderedDict
    data = OrderedDict() #category name -> [[recode1],[recode2]...]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[col] not in data:
                data[ss[col]] = []
            data[ss[col]].append(ss)

    #collapse data and output
    for k,v in data.items():
        #print(v)
        out = []
        for i in range(len(v[0])):
            val = v[-1][i] #default last value.
            for j in reversed(range(len(v))):
        #        print('j:'+str(j))
                if v[j][i].upper() != 'NA':
                    val = v[j][i]
        #            print(val)
                    break
            out.append(val)
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
