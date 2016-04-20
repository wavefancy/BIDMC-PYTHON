#!/usr/bin/env python3

"""

    Check vcf genotype consistence at each genotype level.

    @Author: wavefancy@gmail.com

    Usage:
        VCFOverlapMulti.py -n num <inputs>...
        VCFOverlapMulti.py -h | --help | -v | --version | -f | --format

    Notes:
        1.
        2. Output results to stdout.
        3. See example by -f.

    Options:
        -n num        Output threshold, at least 'num' of inputs have consistence call.
        <inputs>...   Input vcf files.
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
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    vcfMetaCols=9       #number of colummns for vcf meta information.
    supportNum = int(args['-n'])
    infiles = [VariantFile(f, 'r') for f in args['<inputs>']]
    #read contig and its length.
    contigs = [] # [(contigName, len),....]
    for line in str(infiles[0].header).split():
        if line.startswith('##contig'):
            ss = line[:-1].split(',')
            try:
                l = int(ss[1].split('=')[-1])
                contigs.append((ss[0].split('=')[-1], l))
            except ValueError:
                sys.stderr.write('ERROR: Please make sure contig in header has length info, like: ##contig=<ID=chr1,length=248956422>\n')

    if not contigs:
        sys.stderr.write('ERROR: Please make sure contig has been deleared in header, like: ##contig=<ID=chr1,length=248956422>\n')
    print(contigs)
    sys.exit(-1)

    #check smaples in two input file, same samples, and same order.
    for x in infiles[1:]:
        if len(infiles[0].header.samples) != len(x.header.samples):
            sys.stderr.write('ERROR: different number of samples in input files.\n')
            sys.exit(-1)
        else:
            for m,n in zip(infiles[0].header.samples, x.header.samples):
                if m != n:
                    sys.stderr.write('ERROR: input files should have the same samples, and ordered in same order.\n')
                    sys.exit(-1)

    # if len(inF1.header.samples) != len(inF2.header.samples):
    #     sys.stderr.write('ERROR: different number of samples in two input files.\n')
    #     sys.exit(-1)
    # else:
    #     for x, y in zip( inF1.header.samples, inF2.header.samples):
    #         if x != y:
    #             sys.stderr.write('ERROR: two input files should have the same samples, and ordered in same order.\n')
    #             sys.exit(-1)

    #output vcf header
    sys.stdout.write('%s'%(str(infiles[0].header)))

    #compare and output results.
    


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
