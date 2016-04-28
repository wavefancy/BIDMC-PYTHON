#!/usr/bin/env python3

"""

    Check 100% Penetrance for Recessive model.
    *** All individual with Alt homo genotype should be in disease status.

    @Author: wavefancy@gmail.com

    Usage:
        VCFRecessive100Penetrance.py -p pedFile
        VCFRecessive100Penetrance.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin.
        2. ***Output records if a record failed 100% penetrance recessive checking***
        3. Output results to stdout.

    Options:
        -p pedFile      Cohort Ped file.
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
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #from pysam import VariantFile
    import vcf
    #read disease status from ped file.
    diseaseMap = {}  # idname-->diseaseStatus.
    with open(args['-p'], 'r') as pfile:
        for line in pfile:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[1] in diseaseMap:
                    sys.stderr.write('WARNING: duplicate id name, only use the first record: %s\n'%(ss[1]))
                else:
                    diseaseMap[ss[1]] = ss[5]

    #infile = VariantFile('-', 'r')
    vcf_reader = vcf.Reader(sys.stdin)
    sys.stdout.write('#CHROM\tPOS\tREF\tALT\n')
    for line in vcf_reader:
        #only check hom_alts,
        for call in line.get_hom_alts():
            if diseaseMap[call.sample] != '2': #not get disease, failed check, ouput.
                alts = [str(x) for x in line.ALT]
                sys.stdout.write('%s\t%s\t%s\t%s\n'%(line.CHROM, line.POS, line.REF, ','.join(alts)))
                break

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
