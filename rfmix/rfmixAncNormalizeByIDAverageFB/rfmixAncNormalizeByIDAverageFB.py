#!/usr/bin/env python

"""

    Normalize site observed ancestry by genome-wide average.
    2*ID_average - ObservedExpected.
    @Author: wavefancy@gmail.com

    Usage:
        rfmixAncNormalizeByIDAverageFB.py -a IDaverage -i index -n nanc
        rfmixAncNormalizeByIDAverageFB.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read rfmix ForwardBackward output from stdin, and output to stdout.

    Options:
        -a IDaverage     Individual average, one line one person.
        -i index         Which ancestry does [-a] corresponding to, [1-n], index starts from 1.
        -n nanc          Total number of reference ancestry.
        -h --help        Show this screen.
        -v --version     Show version.
        -f --format      Show input/output file format example.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
    #rfmix output, 3 person, 2 snps
    ------------------------
0.1 0.9 0.2 0.8 0.4 0.6 0.5 0.5
0.1 0.9 0.2 0.8 0.4 0.6 0.3 0.7
0.5 0.5 0.3 0.7 0.2 0.8 0.6 0.4

    #id average:
    ------------------------
0.8
0.2

    #output:
    ------------------------
0.1000  0.7000
0.1000  0.9000
-0.4000 0.8000
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    nanc = int(args['-n'])     # total number of ancestry.
    index = int(args['-i']) -1 # ancestry index for global average corresponding to. shift to 0 based.

    idav = [] # 2*ID_average
    with open(args['-a'],'r') as ifile:
        for line in ifile:
            line = line.strip()
            if line:
                idav.append(2 * float(line))

    checkLen = True
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            ss = [float(x) for x in ss] #number of pop1 copy for each haplotype.
            obs = []
            for i in range(0, len(ss), 2*nanc):
                obs.append(ss[i+index] + ss[i+nanc+index])

            if checkLen:
                if len(obs) != len(idav):
                    sys.stderr.write('Error: numbr of individuals in ID_average file is not the same as that in sys.stdin.\n')
                    sys.exit(-1)
                else:
                    checkLen = False

            out = [ '%.4f'%(y-x) for x,y in zip(idav, obs)]
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
