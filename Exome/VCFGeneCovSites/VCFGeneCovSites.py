#!/usr/bin/env python3

"""

    Count the number of coverage sites for each gene.

    @Author: wavefancy@gmail.com

    Usage:
        VCFGeneCovSites.py -a file
        VCFGeneCovSites.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output results to stdout.
        3. Output results to stdout.

    Options:
        -a file         Sites annotation file.
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
    input vcf example(-a):
----------------------
chr1    13200   G       T   GeneName1
chr1    13273   G       T   GeneName2
chr1    13289   CCT     C   GeneName3

    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    annofile = args['-a']
    annoMap = {}
    with open(annofile, 'r') as af:
        for line in af:
            line = line.strip()
            if line:
                ss = line.split(None, 5)
                key = '-'.join(ss[:4])
                if key in annoMap:
                    sys.stderr.write('Warning: duplicate site (only keep the first one): %s\n'%(line))
                else:
                    annoMap[key] = ss[4]

    # infile.close()
    output = False
    seqStart = 9
    covMap = {}
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split()
                key = '-'.join(ss[:2] + ss[3:5])
                if key not in annoMap:
                    pass
                    #sys.stderr.write('ERROR: can not find annotation for site: %s\n'%(key))
                    #sys.exit(-1)
                else:
                    gene = annoMap[key]
                    if gene not in covMap:
                        covMap[gene] = 0
                    covMap[gene] = covMap[gene] + len([x for x in ss[seqStart:] if x[0] != '.'])

            else:
                if line.startswith('##'):
                    pass
                    #sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    #sys.stdout.write('%s\n'%(line))

    #print(annoMap)
    #print(covMap)
    #output results
    sys.stdout.write('GeneName\tTotalCov\n')
    for k,v in covMap.items():
        sys.stdout.write('%s\t%d\n'%(k,v))

sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
