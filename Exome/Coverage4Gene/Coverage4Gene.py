#!/usr/bin/env python3

"""

    Compute reads coverage for regions.

    @Author: wavefancy@gmail.com

    Usage:
        Coverage4Region.py -b bedFile
        Coverage4Region.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read read coverage data from stdin.
        2. Output results to stdout.
        3. Read 4 colums from stdin: 'contigName, exonStarts, exonEnds, geneName'
        4. See example by -f.

    Options:
        -b bedFile    bed file which defined the region.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

    Dependency:
        https://github.com/intiocean/pyinter
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    #'contigName, exonStarts, exonEnds, geneName'
    ------------------------
chr16   30395111,30395779,30397329, 30395578,30395873,30400108, ZNF48
chr1    101,120    110,130   T1
chr1    115  150  T1

    #output: contigName, regionStart, regionEnd, geneName+regionID.
    ------------------------
chr16   30395010        30395973        ZNF48+1
chr16   30397228        30400208        ZNF48+2
chr1    0       250     T1+1
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    joinSubRegion = True # whether joinSubRegion, subRegion was define as name+index.

    from pyinter import interval, interval_set
    contigGeneMap = {} # contigName -> {geneName: (interval,min,max), geneName: (interval, min,max) ... }
    with open(args['-b'], 'r') as bedFile:
        for line in bedFile:
            line = line.strip()
            if line:
                ss = line.split()
                if ss[0] not in contigGeneMap:
                    contigGeneMap[ss[0]] = {}
                if joinSubRegion:
                    geneName = ss[3].split('+')[0]
                else:
                    geneName = ss[3]
                if geneName not in contigGeneMap[ss[0]]:
                    contigGeneMap[ss[0]][geneName] = (interval_set.IntervalSet(), 0, 0) # intervalSet, min, max

                temp = contigGeneMap[ss[0]][geneName]
                left = int(ss[1])
                right = int(ss[2])
                if left < temp[1]:
                    temp[1] = left
                if right > temp[2]:
                    temp[2] = right
                



    from collections import OrderedDict
    dataMap = OrderedDict() # name[contigName+geneName] -> (contigName, geneName, IntervalSet)
    from pyinter import interval, interval_set
    # https://github.com/intiocean/pyinter

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            exonStart = ss[1].strip(',').split(',')
            exonEnd = ss[2].strip(',').split(',')

            name = ss[0] + ss[3]
            if name not in dataMap:
                dataMap[name] = (ss[0], ss[3], interval_set.IntervalSet())

            for s, e in zip(exonStart, exonEnd):
                s = int(s) -1 - padding # bed file 0 based.
                if s < 0:
                    s = 0
                e = int(e) + padding # end not include, therefore do not need -1.
                dataMap[name][2].add(interval.closed(s, e)) #auto aggregate overlap.

    #output results.
    for _,v in dataMap.items():
        index = 0
        for i in v[2]:
            index += 1
            sys.stdout.write('%s\t%d\t%d\t%s+%d\n'%(v[0], i.lower_value, i.upper_value, v[1], index))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
