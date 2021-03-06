#!/usr/bin/env python3

"""

    Check vcf genotype consistence at each genotype level.

    @Author: wavefancy@gmail.com

    Usage:
        VCFOverlap.py <input1> <input2>
        VCFOverlap.py -h | --help | -v | --version | -f | --format

    Notes:
        1.
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
    ''');

from pysam import VariantFile
class Record:
    def __init__(self, inFile):
        self.currentMap = {}
        self.currentContig = ''
        self.min = -1
        self.max = -1
        self.file = inFile        #
        self.step = 1000000 #pre-load 1000000, 1M.

    def getRecord(self, key, contigName, pos):
        '''
            Get record according to input key.
            key = r.contig + r.pos + r.alleles[0] + r.alleles[1] #contigName, pos, ref, alt.
        '''
        if pos < self.min or pos > self.max or contigName != self.currentContig:
            self.min = pos
            self.max = pos + self.step
            self.loadRecords(contigName, pos, pos + self.step)
            self.currentContig = contigName
            #self.loadRecords(contigName, 13273, 13649)

        if key in self.currentMap:
            return self.currentMap[key]
        else:
            return None

    def loadRecords(self, contigName, pos, end):
        '''
            clear current cache, and load records from file.
            *** both end inclusive.
        '''
        #sys.stderr.write('load cache!\n')
        self.currentMap.clear()
        for r in self.file.fetch(contigName, pos-1, end):
            if len(r.alleles) != 2:
                sys.stderr.write('ERROR: please decompose the input vcf, only one alt allele permited each line, error record:\n%s\n'
                %(r))
                sys.exit(-1)
            else:
                key = r.contig + str(r.pos) + r.alleles[0] + r.alleles[1]
                if key in self.currentMap:
                    sys.stderr.write('ERROR: repeated records detected, same meta info, error record:\n%s\n'%(r))
                else:
                    self.currentMap[key] = r

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    vcfMetaCols=9       #number of colummns for vcf meta information.
    inF1 = VariantFile(args['<input1>'], 'r')
    inF2 = VariantFile(args['<input2>'], 'r')
    Record = Record(inF2)
    #check smaples in two input file, same samples, and same order.
    if len(inF1.header.samples) != len(inF2.header.samples):
        sys.stderr.write('ERROR: different number of samples in two input files.\n')
        sys.exit(-1)
    else:
        for x, y in zip( inF1.header.samples, inF2.header.samples):
            if x != y:
                sys.stderr.write('ERROR: two input files should have the same samples, and ordered in same order.\n')
                sys.exit(-1)

    #output vcf header
    sys.stdout.write('%s'%(str(inF1.header)))
    for line in inF1.fetch():
        if len(line.alleles) != 2:
            sys.stderr.write('ERROR: please decompose the input vcf, only one alt allele permited each line, error record:\n%s\n'
            %(line))
            sys.exit(-1)
        ss = str(line).strip().split()
        #print(ss[0])
        key = ss[0] + ss[1] + ss[3] + ss[4]
        line2 = Record.getRecord(key, ss[0], int(ss[1]))
        if line2:
            out = ss[:vcfMetaCols]
            ss2 = str(line2).strip().split()
            for x, y in zip(ss[vcfMetaCols:], ss2[vcfMetaCols:]):
                if x[0] == '.' or y[0] == '.':
                    out.append('.')
                elif x[0] == y[0] and x[2] == y[2]:
                    out.append(x)
                else:
                    out.append('.')
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
