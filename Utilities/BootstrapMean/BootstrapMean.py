#!/usr/bin/env python3

"""

    Bootstrap values to estimate confidence interval for mean.

    @Author: wavefancy@gmail.com

    Usage:
        BootstrapMean.py -n times -c confidence
        BootstrapMean.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read content from stdin, and output results to stdout.
        2. Input separated by 'white' characteres, including '\\n'.

    Options:
        -n times      Number of times for bootstrapping
        -c confidence Confidence interval, float1, float2 ..., eg. 0.8,0.95
        -h --help     Show this screen.
        -v --version  Show version.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    ntimes = 100
    confidence = []
    if args['-n']:
        ntimes = int(args['-n'])
    if args['-c']:
        confidence = [float(x) for x in args['-c'].split(',')]

#-------------------------------------------------
    data = []
    for line in sys.stdin:
        line = line.strip()
        if line:
            data = data + [float(x) for x in line.split()]
    #print(data)
    import numpy
    npData = numpy.array(data)
    means = numpy.empty(ntimes)
    for x in range(ntimes):
        # resampling with replacement.
        # print(numpy.random.choice(npData, len(npData), True))
        means.put(x, numpy.mean(numpy.random.choice(npData, len(npData), True)))
    sortedMeans = numpy.sort(means)
    # print(sortedMeans)
    sys.stdout.write('CI\tLeft\tRight\n')
    for x in confidence:
        skip = numpy.rint(len(means) * (1-x)/2)
        # print(skip)
        sys.stdout.write('%.4f\t%.4e\t%.4e\n'%(x, sortedMeans[skip], sortedMeans[len(means)-skip-1]))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
