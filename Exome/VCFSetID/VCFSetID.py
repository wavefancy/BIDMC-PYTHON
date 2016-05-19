#!/usr/bin/env python3

"""

    Set/Replace ID for VCF file. setID as : chr:pos:ref:alt

    @Author: wavefancy@gmail.com

    Usage:
        VCFSetID.py
        VCFSetID.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, setID as : chr:pos:ref:alt.
        3. Output results to stdout.

    Options:
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
    input vcf example(abstracted):
----------------------
chr2    13649   .  G       C

    out vcf example:
----------------------
chr2    13649   chr2:13649:G:C  G       C
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from pysam import VariantFile

    vcfMetaCols=9       #number of colummns for vcf meta information.
    infile = VariantFile('-', 'r')
    sys.stdout.write(str(infile.header))
    for line in infile:
        ss = str(line).strip().split(None, maxsplit=7)
        ss[2] = ss[0] + ':' + ss[1] + ':' + ss[3] + ':' + ss[4]

        sys.stdout.write('%s\n'%('\t'.join(ss)))

    infile.close()
sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
