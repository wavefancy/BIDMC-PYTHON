#!/usr/bin/env python3

"""
    Trios filters for exome data.
    @Author: wavefancy@gmail.com

    Usage:
        TriosFilter.py -p pedfile
        TriosFilter.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -p pedfile     Pedfile for trio family.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');

class Family(object):
    """docstring for Family"""
    FatherName = ''
    MotherName = ''
    ChildName = ''
    FatherIndex = -1 #genotye index in vcf file.
    MotherIndex = -1
    ChildIndex = -1


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #process ped file.
    with open(args['-p'], 'r') as pfile:
        for line in pfile:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[2] != '0' and ss[3] != '0':
                    if not Family.ChildName:
                        Family.FatherName = ss[2]
                        Family.MotherName = ss[3]
                        Family.ChildName = ss[1]
                    else:
                        sys.stderr.write('WARNING: More than one family detected in ped file,"
                        + "only process the first one !\n')

    #read vcf file from stdin.
    

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
