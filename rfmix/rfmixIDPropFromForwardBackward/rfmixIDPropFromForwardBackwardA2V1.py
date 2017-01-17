#!/usr/bin/env python

"""

    Estimate expected individual level ancestry and it's SD from rfmix ForwardBackword output.
    ***Version A2V1, special design to 2 ancestries, 2 haplotyps each person.

    @Author: wavefancy@gmail.com

    Usage:
        rfmixIDPropFromForwardBackwardA2V1.py [-s|(-i --ms file)]
        rfmixIDPropFromForwardBackwardA2V1.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read rfmix ForwardBackword output from stdin, and output to stdout.
        2. Output each person one line, for expected_Ancestry1 expected_Ancestry2 ...

    Options:
        -n nancestry     Number of reference ancestry.
        -s               Output summary data for ancestry mean and std.
        -i               Output individual level normalized data: (x - Mean(X))/(STD(X)).
        --ms file        Mean and STD file (output from -s option).
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
    #rfmix output, 2 person, 3 snps
    ------------------------
0.1 0.9 0.2 0.8 0.4 0.6 0.5 0.5
0.1 0.9 0.2 0.8 0.4 0.6 0.3 0.7
0.5 0.5 0.3 0.7 0.2 0.8 0.6 0.4

    #output: -n 2 -s
    ------------------------
anc1    anc2
0.2333  0.7667
0.4000  0.6000

    #output: -n 2 -i
    # 2 persons, 2 ancestries, 3 snps.
    ------------------------
-0.7071 0.7071  1.2247  -1.2247
-0.7071 0.7071  -1.2247 1.2247
1.4142  -1.4142 -0.0000 0.0000
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='A2V1')
    # print(args)
    # sys.exit(0)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    # nanc = int(args['-n']) # number of ancestry.
    nanc = 2

    import numpy as np
    # psum = numpy.empty(0)
    # total = 0
    data = [] #row snp, column expected each ancestry for a person.
    for line in sys.stdin:
        line = line.strip()
        if line:
            # total += 1
            ss = line.split()
            #prob = np.array([float(x) for x in ss])
            prob = [float(x) for x in ss]
            out = []
            for i in range(0, len(prob), nanc*2): #2 for 2 copies of chromosome.
                t = prob[i] + prob[i+nanc]
                out.append(t)
            data.append(out)

    # total = total * 2 # for 2 copies.
    #output title:

    npdata = np.array(data)
    ancMean = npdata.mean(axis=0)
    ancSTD  = npdata.std(axis=0)

    if args['-s']:
        sys.stdout.write('%s\t%s\n'%('\t'.join([ 'AVEanc' + str(x+1) for x in range(nanc) ]),
            '\t'.join([ 'SDanc' + str(x+1) for x in range(nanc) ])))
        for i in range(0, len(ancMean)):
            out = []
            out.append(ancMean[i])
            out.append(2-ancMean[i])
            #for j in range(nanc):
            out.append(ancSTD[i])
            out.append(ancSTD[i])
            sys.stdout.write('%s\n'%('\t'.join([ '%.4f'%(x) for x in out ])))

    if args['-i']:
        msdata = np.loadtxt(args['--ms'], dtype=float, comments='#', delimiter='\t', converters=None, skiprows=1, usecols=None, unpack=False, ndmin=0)
        ancMean = msdata[:,0]
        ancSTD = msdata[:,2]

        # #print(msdata)
        # for row in msdata:
        #     #print(len(row))
        #     #print(row)
        #     for col in range(0, int(len(row)/2)):
        #         ancMean.append(row[col])
        #     for col in range(int(len(row)/2), len(row)):
        #         ancSTD.append(row[col])

        normalizedAnc = (npdata - ancMean)/ancSTD
        for x in normalizedAnc:
            sys.stdout.write('%s\n'%('\t'.join(['%.4f'%(i) for i in x])))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
