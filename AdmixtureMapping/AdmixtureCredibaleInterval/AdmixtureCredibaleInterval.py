#!/usr/bin/env python

"""

    Admixture credibale interval calculation based on Log likehood ratio.
    LogLikehoodRatio = 2*(Log(AlternativeModel,e) - Log(nullModel,e))

    @ref: Admixture mapping identifies 8q24 as a prostate cancer risk locus in African-American men.(2006).

    @Author: wavefancy@gmail.com

    Usage:
        AdmixtureCredibaleInterval.py (-d | -c) [-t threshold] -s position -p CIproportion
        AdmixtureCredibaleInterval.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read data from stdin (two columns: position 2*LogLikehoodRatioValue),
            and output to stdout.

    Options:
        -d               output normalized probability density.
        -c               output credibale interval.
        -t float         threshold for define a region around peakValue, default: 3.84, Pvalue of X2(1) = 0.05.
        -s int           Position for a center of a regoin, usually the position of max value.
        -p float         Proportion of credibale interval, eg: 0.95.
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
#examle input
----------------------
1   1
2   2
3   3
4   4
5   5
6   4
7   3
8   2
9   1

#output:-d -t 4 -s 5 -p 0.9
----------------------
2       7.0345e-02
3       1.1598e-01
4       1.9122e-01
5       3.1526e-01
6       1.9122e-01
7       1.1598e-01
8       7.0345e-02

#output:-c -t 3 -s 5 -p 0.5
----------------------
CILeftPos       CIRightPos
4       6
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    outDensity = False
    outInterval = False
    if args['-d']:
        outDensity = True
    if args['-c']:
        outInterval = True
    threshold = 3.84
    if args['-t']:
        threshold = float(args['-t'])

    proportion = float(args['-p'])  #proportion of credibale interval.
    endProp = (1 - proportion) / 2  #proportion for each end.
    position = int(args['-s'])

    pos = []        #positoins
    values = []     #LogLikehoodRatio values.
    pos_index = -1
    index = -1
    import math
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            index += 1
            p = int(ss[0])
            v = math.pow(math.e, float(ss[1]) / 2) #convert 2*LogLikehoodRatio to BayesianFactor.
            if p == position:
                pos_index = index
            pos.append(p)
            values.append(v)

    left_index = 0              #minimum one
    right_index = len(values)-1 #maximum one
    #find right end
    for i in range(pos_index+1, len(values)):
        if values[i] < threshold:
            right_index = i
            break
    #find left end
    for i in range(pos_index-1, -1, -1):
        if values[i] < threshold:
            left_index = i
            break

    #print(left_index)
    #print(right_index)
    #area under curve
    area = 0
    for i in range(left_index+1, right_index+1):
        area += (pos[i] - pos[i-1]) * values[i]
    #print('area:'+str(area))
    #normalized density
    if outDensity:
        nDen = []
        for i in range(left_index, right_index+1):
            nDen.append(values[i]/area)
        for x,y in zip(pos[left_index:right_index+1], nDen):
            sys.stdout.write('%d\t%.4e\n'%(x,y))

    #postion for CI
    if outInterval:
        left_pos = 0    #left pos for CI.
        left_area = 0
        for i in range(left_index+1,right_index+1):
            left_area += (pos[i] - pos[i-1]) * values[i]
            #print('left_area: ' +str(left_area))
            if left_area / area >=  endProp:
                left_pos = pos[i]
                break

        right_pos = 0
        right_area = 0
        for i in range(right_index,left_index-1,-1):
            right_area += (pos[i] - pos[i-1]) * values[i]
            #print('right_area: ' +str(right_area))
            if right_area/area >= endProp:
                right_pos = pos[i]
                break

        sys.stdout.write('CILeftPos\tCIRightPos\n')
        sys.stdout.write('%d\t%d\n'%(left_pos, right_pos))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
