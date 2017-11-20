#!/usr/bin/env python3

"""

    Format the genotype output from ExomeModelFilter.
    @Author: wavefancy@gmail.com

    Usage:
        FormatGeno.py [(-l -c int)]
        FormatGeno.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -c int        Column index for reformating.
                        The contect of other columns will be copyed to output.
        -l            Only list individual names.
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
    #Genotype column from: ExomeModelFilter
    ------------------------
(FGGU1[FGGU11:0/1:16,13;FGGU117:0/1:14,19;FGGU1112:./.;FGGU114:0/1:13,18];FGGU1110:./.)
(FGGU1[FGGU11:0/1:19,23;FGGU117:0/1:13,12;FGGU1112:./.:3,0;FGGU114:0/1:17,14];FGGU1110:0/0:13,0)

    #output:
    ------------------------
FGGU11  FGGU117 FGGU1112        FGGU114 FGGU1110
0/1:16,13       0/1:14,19       ./.     0/1:13,18       ./.
0/1:19,23       0/1:13,12       ./.:3,0 0/1:17,14       0/0:13,0

#input:
------------------------
(FGGU1[FGGU11:0/1:16,13;FGGU117:0/1:14,19;FGGU1112:./.;FGGU114:0/1:13,18];FGGU1110:./.) COL1
(FGGU1[FGGU11:0/1:19,23;FGGU117:0/1:13,12;FGGU1112:./.:3,0;FGGU114:0/1:17,14];FGGU1110:0/0:13,0) COL2

#output: -l -c 1
------------------------
COL1    FGGU11
COL1    FGGU117
COL1    FGGU1112
COL1    FGGU114
COL1    FGGU1110
COL2    FGGU11
COL2    FGGU117
COL2    FGGU1112
COL2    FGGU114
COL2    FGGU1110
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    onlyListIDName = False
    col = -1
    if args['-l']:
        onlyListIDName = True
        col = int(args['-c']) -1

    from collections import OrderedDict
    idGeno = OrderedDict() #{idName - [geno list.]}
    for line in sys.stdin:
        line = line.strip()
        if line:
            #print(line)
            out = []
            if col >= 0:
                kk = line.split()
                line = kk[col]
                out = [kk[i] for i in range(len(kk)) if i != col]

            ss = line.split(';')
            for i in range(len(ss)):
                temp = ss[i].split('[')
                if len(temp) == 2:
                    ss[i] = temp[1]
                    # if onlyListIDName:
                    #     sys.stdout.write('%s\t '%(temp[0][1:])) #list family name.
                if ss[i][-1] == ']' or ss[i][-1] == ')':
                    ss[i] = ss[i][0:-1]

            #only list in names
            if onlyListIDName:
                for x in ss:
                    temp = x.split(':',maxsplit=1)
                    # out.append(temp[0])
                    sys.stdout.write('%s\t'%('\t'.join(out)))
                    sys.stdout.write('%s\n'%(temp[0]))
                # sys.stdout.write('%s\n'%('\n'.join(out)))
            else:
                #store data.
                for x in ss:
                    temp = x.split(':',maxsplit=1)
                    if temp[0] not in idGeno:
                        idGeno[temp[0]] = []
                    idGeno[temp[0]].append(temp[1])

    if onlyListIDName:
        pass
    else:
        #output results
        sys.stdout.write('%s\n'%('\t'.join(idGeno.keys())))
        genoArr = []
        for k in idGeno.keys():
            genoArr.append(idGeno[k])
        #print(genoArr)
        for i in range(len(genoArr[0])):
            out = []
            for x in genoArr:
                out.append(x[i])
            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
