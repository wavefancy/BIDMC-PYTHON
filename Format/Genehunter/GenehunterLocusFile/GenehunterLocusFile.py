#!/usr/bin/env python3

"""

    Generate genehunter locus file.

    @Author: wavefancy@gmail.com

    Usage:
        GenehunterLocusFile.py [-r]
        GenehunterLocusFile.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin.
        2. Output results to stdout.

    Options:
        -r              Output locus as recessive model.
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
# input
# -----------------------------
chr1:11008:C:G 0.9343 0.0657 0
chr1:11012:C:G 0.9343 0.0657 0.1
chr1:13110:G:A 0.9293 0.0707 0.5

# cat in.test.txt | python3 GenehunterLocusFile.py
# -----------------------------
3 0 0 5  << NO. OF LOCI, RISK LOCUS, SEXLINKED (IF 1) PROGRAM
0 0.0 0.0 0  << MUT LOCUS, MUT RATE, HAPLOTYPE FREQUENCIES (IF 1)
1 2 3
1  2  << AFFECTATION, NO. OF ALLELES
0.990000 0.010000  << GENE FREQUENCIES
1  << NO. OF LIABILITY CLASSES
0.001000 0.999000 0.999000
3 2 #chr1:11008:C:G
0.9343 0.0657
3 2 #chr1:11012:C:G
0.9343 0.0657
3 2 #chr1:13110:G:A
0.9293 0.0707
0 0  << SEX DIFFERENCE, INTERFERENCE (IF 1 OR 2)
0.000000 0.100000 0.400000 << RECOMB VALUES
1 0.1 0.45  << REC VARIED, INCREMENT, FINISHING VALUE
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

#'12 0 0 5  << NO. OF LOCI, RISK LOCUS, SEXLINKED (IF 1) PROGRAM',
    headers = [
' 0 0 5  << NO. OF LOCI, RISK LOCUS, SEXLINKED (IF 1) PROGRAM',
'0 0.0 0.0 0  << MUT LOCUS, MUT RATE, HAPLOTYPE FREQUENCIES (IF 1)',
'1 2 3 4 5 6 7 8 9 10 11 12',
'1  2  << AFFECTATION, NO. OF ALLELES',
'0.990000 0.010000  << GENE FREQUENCIES',
'1  << NO. OF LIABILITY CLASSES',
'0.001000 0.999000 0.999000']

    markers = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            markers.append(line.split())

    temp = ['%d'%(x+1) for x in range(len(markers))]
    headers[2] = ' '.join(temp)
    headers[0] = str(len(markers)) + headers[0]

    sys.stdout.write('%s\n'%('\n'.join(headers)))
    for x in markers:
        out = ['3 2 #'+x[0]]
        out.append('%s %s'%(x[1],x[2]))
        sys.stdout.write('%s\n'%('\n'.join(out)))

    sys.stdout.write('0 0  << SEX DIFFERENCE, INTERFERENCE (IF 1 OR 2)\n')

    temp = [float(x[3]) for x in markers]
    rec = [temp[0]]
    for i in range(1,len(temp)):
        rec.append(temp[i] - temp[i-1])

    sys.stdout.write('%s %s\n'%(' '.join(['%.6f'%(x) for x in rec]),'<< RECOMB VALUES'))
    sys.stdout.write('1 0.1 0.45  << REC VARIED, INCREMENT, FINISHING VALUE\n')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
