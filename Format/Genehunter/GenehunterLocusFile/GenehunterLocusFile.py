#!/usr/bin/env python3

"""
    Generate genehunter locus file.

    @Author: wavefancy@gmail.com

    Usage:
        GenehunterLocusFile.py -o oprefix [(-w windowSize -l overlap)] [-r]
        GenehunterLocusFile.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin.
        2. The smallest genetic distance were set as 0.00000001.

    Options:
        -r              Output locus as recessive model.
        -o oprefix      Output file prefix.
        -w windowSize   Window size.
        -l overlap      Overlap of two sliding window.
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

# single slice
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


    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    smallestDistance = 0.00000001 # if the genetic distance less than this, set as this number.
    windowSize = ''
    if args['-w']:
        windowSize = int(args['-w'])

    if args['-w'] and args['-l']:
        step = windowSize - int(args['-l'])

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

    #output results
    if not windowSize:
        step = len(markers)
        windowSize = len(markers)

    from math import expm1
    def distance2RecombinationRate(d):
        '''Convert genetic distance to recombination rate'''
        #return 0.5 * ( 1 - exp(-2*(d/100.0))) #morgen unit.
        re = 0.5 * ( 0 - expm1(-2*(d/100.0)))
        if re < smallestDistance:
            re = smallestDistance
        return re #morgen unit.

    tempIndex = 0
    for i in range(0, len(markers)-1, step):
        tempIndex += 1
        with open(args['-o']+'_s'+str(tempIndex)+'.dat', 'w') as of:
            data = markers[i:i+windowSize]
            #output for headers.
            temp = ['%d'%(x+1) for x in range(len(data)+1)] #include disease mark. +1
            oh = [x for x in headers]
            oh[2] = ' '.join(temp)
            oh[0] = str(len(data)+1) + oh[0]
            of.write('%s\n'%('\n'.join(oh)))

            for x in data:
                out = ['3 2 # '+x[0]]
                out.append('%s %s'%(x[1],x[2]))
                of.write('%s\n'%('\n'.join(out)))

            of.write('0 0  << SEX DIFFERENCE, INTERFERENCE (IF 1 OR 2)\n')

            temp = [float(x[3]) for x in data]
            rec = [distance2RecombinationRate(temp[1] - temp[0])]
            for i in range(1,len(temp)):
                rec.append(distance2RecombinationRate(temp[i] - temp[i-1]))

            of.write('%s %s\n'%(' '.join(['%.8f'%(x) for x in rec]),'<< RECOMB VALUES'))
            of.write('1 0.1 0.45  << REC VARIED, INCREMENT, FINISHING VALUE\n')

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
