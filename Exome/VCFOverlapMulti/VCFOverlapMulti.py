#!/usr/bin/env python3

"""

    Check vcf genotype consistence at each genotype level for multiple input files.

    @Author: wavefancy@gmail.com

    Usage:
        VCFOverlapMulti.py -n num [-c cacheLoadnum] [-s] <inputs>...
        VCFOverlapMulti.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Skip phase information, only compare genotype(0/1, or 0|1 for hetero sites.).
            **** Don't put hetero as 1/0 or 1/0.
            Only output consistence sites, which were supported by at least "supportNum" of input files,
            skip failed sites. At genotype level, mask failed genotype as missing '.'. Output consistence
            getnotype according to the priority as the input order of input files, copy genotype from the
            first consistence file, check according to the file order listed in <inputs> paramter.

            Example, if the genotype of three input files as(same individual, same location):
            0/1 1/1:0,5 1/1:0,2:2:6:49,6,0
            The consistence genotype is 11, the output is 1/1:0,5 (no format checking).

        2. Copy meta data from the first input vcf files, including header, INFO, FORMAT, etc. The input
            files may have different format, like above example, this scripts **do not** check format,
            please make sure the output has consistence format.

        3. Output results to stdout.

    Options:
        -n num          Output threshold, at least 'num' of inputs have consistence call.
        -c cacheLoadnum The number of lines were pre-loaded for cache, default 1000000.
        -s              Skip repeated records, only use the first one. otherwise system will exit if met repeated records.
                        Repeated records defined as same location and same ref and alt allele.
        <inputs>...     Input vcf files.
        -h --help       Show this screen.
        -v --version    Show version.
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

class allKeys:
    keyset = set()

    def getOrderedKeyList():
        '''get Ordered key list by position, only return sorted keys,
           After this call, keyset will be cleared.
           Should be reloaded by Record.loadRecords() if need another call.
        '''
        if allKeys.keyset:
            x = sorted(list(allKeys.keyset), key=lambda x: x[1])
            re = [y[0] for y in x]
            allKeys.keyset.clear()
            return re
        else:
            return []

class Record:
    def __init__(self, inFile):
        self.currentMap = {}
        self.file = inFile
        # self.currentContig = ''
        # self.min = -1
        # self.max = -1
        # self.step = 1000000 #pre-load 1000000, 1M.

    def getRecord(self, key):
        '''
            Get record according to input key.
            key = r.contig + r.pos + r.alleles[0] + r.alleles[1] #contigName, pos, ref, alt.
        '''
        # if pos < self.min or pos > self.max or contigName != self.currentContig:
        #     self.min = pos
        #     self.max = pos + self.step
        #     self.loadRecords(contigName, pos, pos + self.step)
        #     self.currentContig = contigName
        #     #self.loadRecords(contigName, 13273, 13649)

        if key in self.currentMap:
            return self.currentMap[key]
        else:
            return None

    def loadRecords(self, contigName, start, end):
        '''
            clear current cache, and load records from file.
            *** both end inclusive.
        '''
        #sys.stderr.write('load cache!-->%s\n'%(contigName))
        self.currentMap.clear()
        #for r in self.file.fetch(contigName, pos-1, end):
        for r in self.file.fetch(contigName, start, end):
            if len(r.alleles) != 2:
                sys.stderr.write('ERROR: please decompose the input vcf, only one alt allele permited each line, error record:\n%s\n'
                %(r))
                sys.exit(-1)
            else:
                key = r.contig + str(r.pos) + r.alleles[0] + r.alleles[1]
                if key in self.currentMap:
                    if skipRepeat:
                        sys.stderr.write('Warning: repeated records detected, only keep the first one, same meta info, error record:\n%s\n'%(r))
                    else:
                        sys.stderr.write('ERROR: repeated records detected, same meta info, error record:\n%s\n'%(r))
                        sys.exit(-1)
                else:
                    self.currentMap[key] = r
                    allKeys.keyset.add((key, r.pos))

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    vcfMetaCols=9       #number of colummns for vcf meta information.
    cacheStep = 1000000
    if args['-c']:
        cacheStep = int(args['-c'])

    supportNum = int(args['-n'])
    infiles = [VariantFile(f, 'r') for f in args['<inputs>']]
    skipRepeat = False
    if args['-s']:
        skipRepeat = True
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
                sys.exit(-1)

    if not contigs:
        sys.stderr.write('ERROR: Please make sure contig has been deleared in header, like: ##contig=<ID=chr1,length=248956422>\n')
        sys.exit(-1)
    #print(contigs)
    #sys.exit(-1)

    #check smaples in input files, same samples, and same order.
    for x in infiles[1:]:
        if len(infiles[0].header.samples) != len(x.header.samples):
            sys.stderr.write('ERROR: different number of samples in input files.\n')
            sys.exit(-1)
        else:
            for m,n in zip(infiles[0].header.samples, x.header.samples):
                if m != n:
                    sys.stderr.write('ERROR: input files should have the same samples, and ordered in same order.\n')
                    sys.exit(-1)

    #output vcf header
    sys.stdout.write('%s'%(str(infiles[0].header)))

    #compare and output results.
    from collections import Counter
    #load cache into memory, check and output.
    Records = [Record(x) for x in infiles]
    for con, conLen in contigs:
        for start in range(0, conLen, cacheStep):
            end = start + cacheStep
            #locad caches for each input files.
            [x.loadRecords(con, start, end) for x in Records]
            #iterate all possible keys,
            keys = allKeys.getOrderedKeyList()
            for key in keys:
                lines = [x.getRecord(key) for x in Records if x.getRecord(key)]
                if len(lines) >= supportNum: # meet threshold at site level. output records, otherwise skip.
                    #check threshold at genotype level.
                    sites = [str(x).strip().split() for x in lines]
                    out = sites[0][:vcfMetaCols]
                    for col in range(vcfMetaCols, len(sites[0])): #check at genotype level.
                        genos = [x[col][0] + x[col][2] for x in sites if x[col][0] != '.']
                        if len(genos) >= supportNum:
                            count = Counter(genos)
                            genoCounts = sorted(count.items(), key=lambda x: x[1], reverse=True)
                            #sys.stderr.write(str(genoCounts))
                            if genoCounts[0][1] >= supportNum: #meet condition, add one records.
                                for x in sites:
                                    if x[col][0] != '.' and x[col][0] + x[col][2] == genoCounts[0][0]:
                                        out.append(x[col])
                                        break
                            else:
                                out.append('.')
                        else:
                            out.append('.')
                    #output one records.
                    sys.stdout.write('%s\n'%('\t'.join(out)))

    [f.close() for f in infiles]
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
