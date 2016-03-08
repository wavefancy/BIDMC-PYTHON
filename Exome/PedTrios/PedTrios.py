#!/usr/bin/env python3

"""

    Extract trio family from ped file.
    @Author: wavefancy@gmail.com

    Usage:
        PedTrios.py
        PedTrios.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read ped from stdin, and output results to stdout.
        2. ***Only output family two parents unaffected by disease, child affected.***
        3. See example by -f.

    Options:
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
    #Output from: FamilyHitByGene.py
    ------------------------
    S27     S27     0       0       2       2
    S28     S28     0       0       1       2
    S29     S29A    0       0       1       1
    S29     S29B    0       0       2       1
    S29     S29     S29A    S29B    2       2

    #output:
    ------------------------
    S29     S29A    0       0       1       1
    S29     S29B    0       0       2       1
    S29     S29     S29A    S29B    2       2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    from collections import OrderedDict
    families = OrderedDict() #[familyname->[individual lines]]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0] not in families:
                families[ss[0]] = []
            families[ss[0]].append(ss)


    #check families and output.
    #only output trio family, and two parents unaffected, child affected.
    for _,v in families.items():
        if len(v) == 3:
            parents = set()
            childLine = ''
            for x in v:
                if x[2] == '0' and x[3] == '0' and x[5] == '1':
                    parents.add(x[1])
                else:
                    childLine = x

            if childLine[5] == '2' and childLine[2] in parents and childLine[3] in parents:
                #candiate family output.
                for x in v:
                    sys.stdout.write('%s\n'%('\t'.join(x)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
