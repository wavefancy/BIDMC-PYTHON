#!/usr/bin/env python3

"""

    Organize genes by families.
    @Author: wavefancy@gmail.com

    Usage:
        FamilyHitByGene.py
        FamilyHitByGene.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

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
    #two columns, genename family_structure
    ------------------------
    g1 (CHOPAA1[CHOPAA11:1/1:0,53],CHOPAA1:0/0:44,0,CHOPAA10:0/1:78,102)
    g2 (FGNN[FGNN11:1/1:0,8])
    g1 (FGNN[FGNN11:1/1:0,8])
    g1 (FGNM1[FGNM11:1/1:0,49]),(FGJC[FGJC11:1/1:0,32])

    #output:
    ------------------------
    FamilyName      #SeqedIDs       #HitGene        GeneName
    CHOPAA1 3       1       g1
    FGNN    1       2       g1
    FGNN    1       2       g2
    FGNM1   1       1       g1
    FGJC    1       1       g1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='2.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    import collections
    familyGeneMap = {} # familyname -> [g1,g2 ... ])
    familySizeMap = {} # familyname -> numberOfSeqedIDs(int)
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            for f in ss[1].split('(')[1:]:
                fnames = f.split('[')[0]
                #check family size.
                if fnames not in familySizeMap:
                    fsize = len(f.split('/')) -1
                    familySizeMap[fnames] = fsize

                if fnames not in familyGeneMap:
                    familyGeneMap[fnames] = set()
                familyGeneMap[fnames].add(ss[0])

    #order output by family size(number of seqed person in a family).
    out = [] #(familyname, familysize, geneSet),() ...
    for k in familyGeneMap.keys():
        out.append((k, familySizeMap[k], familyGeneMap[k]))

    #out = sorted(out, key=lambda x: (x[1],x[0]), reverse=True)
    out = sorted(out, key=lambda x: (x[1],x[2]), reverse=True)

    sys.stdout.write('FamilyName\t#SeqedIDs\t#HitGene\tGeneName\n')
    for n in out:      #iterate on family.
        for g in n[2]: #iterate on gene name.
            sys.stdout.write('%s\t%d\t%d\t%s\n'%(n[0], n[1], len(n[2]), g))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
