#!/usr/bin/env python3

"""
    Extract guide-RNA for CRISPR screening
    @Author: wavefancy@gmail.com

    Usage:
        ExtractgRNA.py [-a anchor] [-l gRNALen]
        ExtractgRNA.py -h | --help | -v | --version | -f | --format

    Notes:
        2. Read results from stdin, and output results to stdout.
        3. See example by -f.

    Options:
        -a string     Anchor string for guide-RNA, default(GTGGAAAGGACGAAACACCG,GTTTTAGAGCTAGAAATAGC)
        -l int        Length for guide-RNA, default 20.
        -s int        Start number for haplotype index, default 1.
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
    # in Fastq file, each elements contain 4 lines, refer fastq format.
    # https://en.wikipedia.org/wiki/FASTQ_format.
    ------------------------
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from Bio.Seq import Seq
    def getReverse_complement(x):
        '''get reverse complement string for x'''
        return str(Seq(x).reverse_complement())

    Anchors = ['GTGGAAAGGACGAAACACCG','GTTTTAGAGCTAGAAATAGC']
    if args['-a']:
        Anchors = args['-a'].split(',')
    gRNALen = 20
    if args['-l']:
        gRNALen = int(args['-l'])

    def extractGuideRNA(data):
        '''extract guide rna for input data.
            [data] = ['SeqName', 'String4Seq', '+', 'String4Quality']

            return ('Output string', 'True/False')
            : True, OK to stdout.
            : False, error raised, should be output to stdout.
        '''
        #print(data)
        indexs = [data[1].find(x) for x in Anchors]
        rc = ''
        error = ''
        if min(indexs) < 0: #failed to find anchor string in input.
            rc = getReverse_complement(data[1])
            indexs = [rc.find(x) for x in Anchors]
            if min(indexs) < 0: #failed even reverse and complement string.
                error = 'NO_ANCHOR'
                #print('NO_ANCHOR')
                #output
                return '%s\n%s\n%s\n%s\n'%(data[0]+' ' + error, data[1], data[2], data[3]), False

        #find index successfully.
        if indexs[0] >= indexs[1]:
            error = 'INDEX_ERROR'
            return '%s\n%s\n%s\n%s\n'%(data[0]+' ' + error, data[1], data[2], data[3]), False

        elif (indexs[1] - indexs[0]) - len(Anchors[0]) != gRNALen:
            error = 'gRNA_LEN_ERROR'
            return '%s\n%s\n%s\n%s\n'%(data[0]+' ' + error, data[1], data[2], data[3]), False
        else:
            x,y = indexs[0]+ len(Anchors[0]), indexs[1]
            if rc:
                return '%s\n%s\n%s\n%s\n'%(data[0], rc[x:y], data[2], data[3][::-1][x:y]), True
            else:
                return '%s\n%s\n%s\n%s\n'%(data[0], data[1][x:y], data[2], data[3][x:y]), True

    def output(data):
        '''[data] = ['SeqName', 'String4Seq', '+', 'String4Quality']'''
        #print(data)
        if data[0][0] != '@':
            sys.stderr.write('ERROR: input format error. Fastq seq name not started by @: %s\n'%(data[0]))
            sys.exit(-1)
        else:
            x,y = extractGuideRNA(data)
            if y:
                sys.stdout.write('%s'%(x))
            else:
                sys.stderr.write('%s'%(x))

    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data.append(line)
            if len(data) == 4:
                output(data)
                data = []

    if data:
        output(data)

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
