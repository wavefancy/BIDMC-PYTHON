#!/usr/bin/env python3

"""

    Estimate the expected success rate for each gene.

    @Author: wavefancy@gmail.com

    Usage:
        EstimateExpectedSuccessRate.py -b bgCount -s sCount (-a|-e)
        EstimateExpectedSuccessRate.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output results to stdout.
        3. Output results to stdout.

    Options:
        -b bgCount      Column index for background count(totoal numnber of trials).
        -s sCount       Column index for the number of successful trails.
        -a              Output average rate for each gene, totalSuccessTrails4AllGenes/totalTrails4AllGenes.
        -e              Output empirical rate for each gene, totalSuccessTrails/totalTrails4Gene,
                        *** If the successful rate is 0, replaced as average rate.
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
    input example:
----------------------
x1      3   1
x2      5   2
x3      10  0

#output: cat test.txt | python3 EstimateExpectedSuccessRate.py -b 2 -s 3 -a
----------------------
1.6667e-01

#output: cat test.txt | python3 EstimateExpectedSuccessRate.py -b 2 -s 3 -e
----------------------
x1      3       1       3.3333e-01
x2      5       2       4.0000e-01
x3      10      0       1.6667e-01
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    bIndex = int(args['-b']) -1
    sIndex = int(args['-s']) -1

    content = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            try:
                b = int(ss[bIndex])
                s = int(ss[sIndex])

                ss.append(b) #background
                ss.append(s) #success
                content.append(ss)
            except ValueError:
                sys.stderr.write('Warning, parse int error at(SKIPPED): %s\n'%(line))

    #compute average rate.
    sTotal = sum([x[-1] for x in content])
    bTotal = sum([x[-2] for x in content])

    if args['-a']:
        sys.stdout.write('%.4e\n'%(1.0*sTotal/bTotal))

    if args['-e']:
        for x in content:
            out = x[:-2]
            if x[-1] == 0:
                out.append('%.4e'%(1.0*sTotal/bTotal))
            else:
                out.append('%.4e'%(x[-1]*1.0/x[-2]))

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
