#!/usr/bin/env python3

"""

    Add contig length in vcf header.

    @Author: wavefancy@gmail.com

    Usage:
        AddContigLength4VCF.py -c contigLen
        AddContigLength4VCF.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read VCF from stdin.
        2. Output results to stdout.
        3. See example by -f.

    Options:
        -c contigLen  Contig length file, two columns, ContigName,Length
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

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    lenMap = {}
    for line in open(args['-c'], 'r'):
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0] in lenMap:
                sys.stderr.write('WARNING: repeated contig name: %s, use only the first entry.\n'%(ss[0]))
            else:
                lenMap[ss[0]] = ss[1]

    #process vcf files.
    for line in sys.stdin:
        line = line.strip()
        if line:
            if line.startswith('##contig='):
                out = line.split('=')
                cname = out[2][:-1]
                if cname not in lenMap:
                    sys.stderr.write('ERROR: can not find contig name:"%s", from -c contigLen file.\n'%(cname))
                    sys.exit(-1)

                out[2] = cname + ',' + 'length=' + lenMap[cname] + '>'
                sys.stdout.write('%s\n'%('='.join(out)))

            else:
                sys.stdout.write('%s\n'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
