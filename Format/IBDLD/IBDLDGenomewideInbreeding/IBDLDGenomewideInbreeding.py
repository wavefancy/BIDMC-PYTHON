#!/usr/bin/env python3

"""
    Compute genome-wide inbreeding coefficient from IBDLD(-ibc) output
    Usage:
        IBDLDGenomewideInbreeding.py
        IBDLDGenomewideInbreeding.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read chromosome specific inbreeding coefficient from stdin, and output to stdout.
        2. See example by -f.

    Options:
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
#IBDLD output (-ibc):
------------------------------------
Sample_M_FS-H1_012_012        Sample_M_FS-H1_012_012        21  1031  0.4672
M_FG-MH12                     M_FG-MH12                     21  1031  0.29
Sample_M_FS-H1_012_012        Sample_M_FS-H1_012_012        22  1031  0.4672
M_FG-MH12                     M_FG-MH12                     22  1031  0.29

# output:
------------------------------------
Sample_M_FS-H1_012_012  Sample_M_FS-H1_012_012  0.4672
M_FG-MH12       M_FG-MH12       0.2900
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    idData = {} # idname -> [chromosome specific data]
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            name = ss[0] + '\t' + ss[1]
            if name not in idData:
                idData[name] = []
            idData[name].append([float(x) for x in ss[3:]])

    #compute individual level inbreeding coefficient
    out = []
    for k,v in idData.items():
        tLen = sum([x[0] for x in v])
        tCoeff = sum([x[0]*x[1] for x in v])
        out.append((k, tCoeff/tLen))

    #output data
    for k,v in sorted(out, key=lambda x:x[1], reverse=True):
        sys.stdout.write('%s\t%0.4f\n'%(k,v))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
