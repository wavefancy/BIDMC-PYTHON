#!/usr/bin/env python3

"""

    Remove a vcf record if alt_homo is present.

    @Author: wavefancy@gmail.com

    Usage:
        VCFRemoveAltHomo.py [(-p file -m)]
        VCFRemoveAltHomo.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, mask genotype as miss if DP tage value < 'num'.
        3. Output results to stdout.

    Options:
        -p file         ped file for check gender.
        -m              Keep record if alt_homo is present on male X-chromosome.
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
GT:AD:DP:GQ:PL       0/0:11,0:11:33:0,33,484 ./.     0/0

    out vcf example: -n 9
----------------------
PL:GT:GQ        0/0:11,0:11:33:0,33,484 .       .
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)
    #sys.exit(-1)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import vcf

    pedfile = ''
    keepAltHomoOnMaleX = False
    if args['-p']:
        pedfile = args['-p']
    if args['-m']:
        keepAltHomoOnMaleX = True

    #read ped file if need.
    genderMap = {} #name -> gender
    if keepAltHomoOnMaleX:
        with open(pedfile, 'r') as pfile:
            for line in pfile:
                print(line)
                line = line.strip()
                if line:
                    ss = line.split()
                    if ss[4] != '2' or ss[4] != '1':
                        sys.stderr.write('Warning: skip gender related checking for this individual, gender info. error for :%s-%s\n'%(ss[1],ss[4]))
                    else:
                        if ss[1] in genderMap:
                            sys.stderr.write('ERROR: repeated individual: %s'%(ss[1]))
                            sys.exit(-1)
                        else:
                            genderMap[ss[1]] = ss[4]
    print(genderMap)

    import vcf
    vcf_reader = vcf.Reader(sys.stdin)
    vcf_writer = vcf.Writer(sys.stdout, vcf_reader)
    for record in vcf_reader:
        #print(record.get_hom_alts())
        #print(record.CHROM)
        if keepAltHomoOnMaleX:
            althomos = record.get_hom_alts()
            if not althomos:
                 vcf_writer.write_record(record)
            else:
                if str(record.CHROM).lower().startswith('chrx'): #checking male x.
                    skip = False
                    for call in althomos:
                        if str(call.sample) not in genderMap:
                            sys.stderr.write('ERROR: this individual not in ped file: %s\n'%(call.sample))
                            sys.exit(-1)
                        elif genderMap[call.sample] != '1':
                            skip = True
                            break
                    if not skip:
                        vcf_writer.write_record(record)
        else:
            if not record.get_hom_alts():
                vcf_writer.write_record(record)

    #vcf_reader.close()
    vcf_writer.flush()
    vcf_writer.close()
#sys.stdout.flush()
#sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
