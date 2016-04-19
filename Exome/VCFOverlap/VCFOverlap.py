#!/usr/bin/env python3

"""

    Check vcf genotype consistence at each genotype level.

    @Author: wavefancy@gmail.com

    Usage:
        VCFOverlap.py <input1> <input2>
        VCFOverlap.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read VCF from stdin.
        2. Output results to stdout.
        3. See example by -f.

    Options:
        <input1>      Input vcf file1.
        <input2>      Input vcf file2.
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
    #'contigName, Length
    ------------------------
chr1    11
chr2    22

    #output:
    ------------------------
##FORMAT=<ID=NV,Number=.,Type=Integer,Description="Number of reads containing variant in this sample">
##contig=<ID=chr1,length=11>
##contig=<ID=chr2,length=22>
#CHR
    ''');

class Record:
    def __init__(self):
        self.currentMap = {}
        self.currentPos = -1
        self.currentContig = ''
        self.next = []

    def loadOne(self, infile):
        if self.next:
            ss = self.next
            # self.currentPos = int(ss[1])
            # self.currentContig = ss[0]
            # key = ss[0] + ss[1] + ss[3] + ss[4]
            # self.currentMap.clear()
            # self.currentMap[key] = ss
        else: #first time load
            line = infile.readline().strip()
            ss = line.split()

        self.currentPos = int(ss[1])
        self.currentContig = ss[0]
        key = ss[0] + ss[1] + ss[3] + ss[4]
        self.currentMap.clear()
        self.currentMap[key] = ss

        #try load all possible same position one, sample location.
        while True:
            line = infile.readline()
            if line:
                line = line.strip()
                self.next = line.split()
                ss = self.next
                if ss[0] = self.currentContig && int(ss[1]) = self.currentPos: #load same location one.
                    key = ss[0] + ss[1] + ss[3] + ss[4]
                    self.currentMap[key] = ss
                else:
                    break
            else: #file end.
                self.currentMap.clear() #empty map for file end.

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    inF1 = open(args['<input1>'], 'r')
    inF2 = open(args['<input2>'], 'r')

    def readTitle(infile):
        '''read title from intput vcf file'''
        for line in infile:
            line = line.strip()
            if line and line.startswith('#CHROM'):
                return line

    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split()
                sys.stdout.write('%s\n'%('\t'.join([ss[x] for x in idIndex])))

            else:
                if line.startswith('##'):
                    sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    #compare title line, require same title.

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
