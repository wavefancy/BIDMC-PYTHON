#!/usr/bin/env python3

"""

    FisherExactTest for 2by2 table.
    @Author: wavefancy@gmail.com

    Usage:
        FisherExactTest.py -c cols -t cols
        FisherExactTest.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout, add two column for pvalue and odds ratio.
            *** If there are 0 in some cells, add each cell by 0.5 for estimate odds ratio.
        2. See example by -f.

    Options:
        -c cols        Column indexes for treat1, eg: 1,2. Index started from 1.
        -t cols        Column indexes for treat2, eg: 3,4. Index started from 1.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
#example input
-----------------------------
x1  7   0   186 95
x2  31  10  3183    1731
x3  x   x   x   x

# cat test.txt | python3 FisherExactTest.py -c 2,3 -t 4,5
-----------------------------
x1      7       0       186     95      7.6810  5.8515e-02
x2      31      10      3183    1731    1.6859  9.7437e-02
WARNING: parse int error for line(skipped): x3  x   x   x   x
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #api:
    #http://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.fisher_exact.html
    alternative = 'greater'
    t1Index = [int(x) -1 for x in args['-c'].split(',')]
    t2Index = [int(x) -1 for x in args['-t'].split(',')]

    import scipy.stats as stats
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                c1 = [int(ss[x]) for x in t1Index]
                c2 = [int(ss[x]) for x in t2Index]

                #print(c1)
                #print(c2)
                oddsratio, pvalue = stats.fisher_exact([c1, c2], alternative=alternative)

                if float('Inf') == oddsratio:
                    oddsratio = (c1[0]+0.5) / (c1[1] + 0.5) / ((c2[0] + 0.5) / (c2[1] + 0.5))

                sys.stdout.write('%s\t%.4f\t%.4e\n'%('\t'.join(ss), oddsratio, pvalue))

            except ValueError:
                sys.stderr.write('WARNING: parse int error for line(skipped): %s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
