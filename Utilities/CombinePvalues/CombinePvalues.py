#!/usr/bin/env python3

"""

    Combine multiple pvalues.
    @Author: wavefancy@gmail.com

    Usage:
        CombinePvalues.py -k indexs [-s]
        CombinePvalues.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin and output results to stdout, add one column for combined pvalue.
        2. See example by -f.

    Options:
        -k indexs      Column index for input pvalues, eg 1|1,3,4.
        -s             Specify use 'stouffer' method for combine, default 'fisher' method.
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
# input example:
# echo -e '0.5 0.1\\n2.8784e-21 8.6420e-01\\n8.7935e-04 5.8147e-04' | python3 CombinePvalues.py -k 1,2 -s
--------------------------
0.5	0.1	1.8242e-01
2.8784e-21	8.6420e-01	2.2398e-09
8.7935e-04	5.8147e-04	3.2638e-06
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    pvindex = [int(x)-1 for x in args['-k'].split(',')]

    method = 'fisher'
    if args['-s']:
        method = 'stouffer'

    from scipy import stats
    #api: print(stats.binom_test.__doc__)
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                ipv = [float(ss[i]) for i in pvindex]

                pv = stats.combine_pvalues(ipv, method=method)
                #print(pv)
                ss.append('%.4e'%(pv[1]))
            except ValueError:
                ss.append('CombinedPValue')

            sys.stdout.write('%s\n'%('\t'.join(ss)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
