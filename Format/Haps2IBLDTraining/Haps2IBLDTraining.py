#!/usr/bin/env python3

"""
    Convert haps/samples haps file to IBDLD training file.
    Usage:
        Haps2IBLDTraining.py [-s]
        Haps2IBLDTraining.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. See example by -f.

    Options:
        -s             Only keep SNP sites, ref/alt allele length 1.
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
#haps format:
------------------------------------
13 rs140871821:19020095:C:T 19020095 C T 0 0 0 0
13 rs2344776:19022254:T:C 19022254 T C 1 1 1 0
13 13:19022245:C:A 19022245 C A 0 1 1 0

# output:
------------------------------------
#chromosome     Marker  Ind1    Ind2
13      13:19020095:C:T C|C     C|C
13      13:19022254:T:C C|C     C|T
13      13:19022245:C:A C|A     A|C
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    def replaceCode(code, ss):
        '''Replace 0/1 to ref and alt'''
        if code == '0':
            return ss[3]
        elif code == '1':
            return ss[4]
        else:
            sys.stderr.write('ERROR: unrecognized code for "%s" at line: %s\n'%(code, '\t'.join(ss)))
            sys.exit(-1)

    snpOnly = False
    if args['-s']:
        snpOnly = True

    title = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if snpOnly:
                if len(ss[3]) != 1 or len(ss[4]) != 1:
                    continue

            out = []
            out.append(ss[0])
            out.append('%s:%s:%s:%s'%(ss[0], ss[2], ss[3], ss[4]))
            alleles = [replaceCode(x, ss) for x in ss[5:]]
            for i in range(0, len(alleles), 2):
                out.append('%s|%s'%(alleles[i], alleles[i+1]))

            if not title:
                title.append('#chromosome')
                title.append('Marker')
                [title.append('Ind%d'%(i+1)) for i in range(len(out)-2)]
                sys.stdout.write('%s\n'%('\t'.join(title)))

            #output
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
