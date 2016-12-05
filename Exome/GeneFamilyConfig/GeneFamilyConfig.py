#!/usr/bin/env python3

"""

    Compute the family configuration for each gene.

    @Author: wavefancy@gmail.com

    Usage:
        GeneFamilyConfig.py [-i]
        GeneFamilyConfig.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin, and output to stdout.
        2. ***IMPORTANT*** please make sure that each family record for each gene is uniq.
        3. Column index starts from 1.
        4. See example by -f.

    Options:
        -i            Indicate input is three columns input, see example by -f.
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
#INPUT (default format): two columns, geneName, familyConfig
------------------------
L1TD1   (CHOPBA[CHOPBA32C:0/1:11,13])
NEBL    (CPMC6[CPMC6:0/1:77,62])
NEBL    (CHOPAQ1[CHOPAQ11:0/1:8,9;CHOPAQ12:0/1:5,4])
L1TD1   (SPD30[SPD30:0/1:21,13])

#INPUT (-i): three columns, geneName, familyName, familyMemebr.
------------------------
L1TD1   CHOPBA    CHOPBA32C
NEBL    CPMC6   CPMC6
NEBL    CHOPAQ1 CHOPAQ11
NEBL    CHOPAQ1 CHOPAQ12
L1TD1   SPD30   SPD30

#output:
------------------------
GeneName        SeqedCount*FamCount
L1TD1   1*2
NEBL    2*1+1*1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    gindex = 0
    findex = 1

    from collections import OrderedDict
    dataMap = OrderedDict() #genaName -> [seqNum for each family]

    if args['-i']:
        geneMap = OrderedDict() # geneName ->[familyName familyMemebr,...]
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split()
                gene = ss[0]
                if gene not in geneMap:
                    geneMap[gene] = []
                geneMap[gene].append(ss[1:])

        #iterate for each gene.
        for gene, v in geneMap.items():
            familyMap = {} #familyName -> set(members)
            for x in v:
                if x[0] not in familyMap:
                    familyMap[x[0]] = set()
                familyMap[x[0]].add(x[1])

            #count family member number of each family.
            if gene not in dataMap:
                dataMap[gene] = []

            for fam , members in familyMap.items():
                dataMap[gene].append(len(members))

    else: #input is two columns format.
        for line in sys.stdin:
            line = line.strip()
            if line:
                ss = line.split()
                gene = ss[gindex]
                famLen = len(ss[findex].split(';'))

                if gene not in dataMap:
                    dataMap[gene] = []

                dataMap[gene].append(famLen)

    #output results.
    sys.stdout.write('GeneName\tSeqedCount*FamCount\n')
    from collections import Counter
    for k,v in dataMap.items():
        config = Counter(v)
        cstring = []
        for i in sorted(config.keys(),reverse=True):
            cstring.append(str(i) + '*' + str(config[i]))

        sys.stdout.write('%s\t%s\n'%(k, '+'.join(cstring)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
