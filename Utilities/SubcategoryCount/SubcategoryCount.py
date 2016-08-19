#!/usr/bin/env python3

"""

    Count the number of elements in each subcategory.
    @Author: wavefancy@gmail.com

    Usage:
        SubcategoryCount.py -g groups
        SubcategoryCount.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin (two columns, main_category_name sub_category_name), and output results to stdout.
        2. See example by -f.

    Options:
        -g groups      Group labels for each subcategory, eg: L1,L2:L3 (two groups, one with label L1 and L2, the other L3.).
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
#input example
--------------------
C1  S1
C1  S2
C1  S1
C2  S1
C2  S2
C2  S3
C1  S2

# cat test.txt | python3 SubcategoryCount.py -g S1:S2,S3
--------------------
Name    S1      S2,S3
C1      2       2
C2      1       2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    groups = args['-g'].split(':')
    gsets = [set(x.split(',')) for x in groups]
    iArray = [0] * len(gsets)

    from collections import OrderedDict
    gMap = OrderedDict()

    def findGroupIndex(name):
        '''find the group index for name'''
        for k,v in enumerate(gsets):
            if name in v:
                return k
        return -1 #if not found in any group.

    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if ss[0] not in gMap:
                gMap[ss[0]] = iArray.copy()

            index = findGroupIndex(ss[1])
            if index < 0:
                sys.stderr.write('WARNING: can not find group label defination for this line(skipped): %s\n'%(line))
            else:
                gMap[ss[0]][index] += 1

    #output results
    sys.stdout.write('Name\t%s\n'%('\t'.join(groups)))
    for k,v in gMap.items():
        sys.stdout.write('%s\t%s\n'%(k,'\t'.join(map(str, v))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
