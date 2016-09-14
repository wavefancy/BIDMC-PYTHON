#!/usr/bin/env python

'''
    MatchCaseControlPCA

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:
        Best match cases and controls based on the PCA results.
'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    MatchCaseControlPCA
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 2.0

    @Usages:
    para1: case input file
    para2: control input file.

    @Notes:
    1. Best match cases and controls based on the PCA results.
    2. Output matched results to stdout.
    3. Input format: First column for name, second to N, for PCA dementional values.
        Name1   x   y   z   .....
        Name2   x   y   z   .....

    4. Find an matching individual for case by minimize D = [(x_i-x_case)^2 + (y_i - y_case)^2 + ....],
        Iterate i for all controls.
    5. If weights have been assigned, use weighted distance.
        D = [(x_i-x_case)^2*w1 + (y_i - y_case)^2*w2 + ....]/(sum(w))
    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    case_f = '' # case file
    control_f = '' # control file.
    weight_f = '' #weight file

if __name__ == '__main__':
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        help()

    P.case_f = sys.argv[1]
    P.control_f = sys.argv[2]
    if len(sys.argv) == 4:
        P.weight_f = sys.argv[3]

    controls = [] #[(name, [val1, val2]) , (name, [val1, val2])  ...]
    for line in open(P.control_f):
        line = line.strip()
        if line:
            ss = line.split()
            vals = list(map(float, ss[1:]))
            controls.append((ss[0], vals))

    weights = [] #weight for each demention, like the proportion of variance explained by each pc.
    if P.weight_f:
        with open(P.weight_f, 'r') as f:
            for line in f:
                [weights.append(float(x)) for x in line.strip().split()]

    def distance(vals1, vals2):
        '''Compute the sequared distance between point1 and point2'''
        if len(vals1) != len(vals2):
            sys.stderr.write('Error: Point1 and Point2 have different dimension:\n')
            sys.stderr.write('%s\n'%('\t'.join(map(str, vals1))))
            sys.stderr.write('%s\n'%('\t'.join(map(str, vals2))))
            sys.exit(-1)

        if weights:
            if len(vals1) != len(weights):
                sys.stderr.write('Error: PCA and weight have different dimension:\n')
                sys.exit(-1)
            else:
                return sum([(x-y)*(x-y)*z for x,y,z in zip(vals1, vals2, weights)])/sum(weights)

        else:
            return sum( [(x-y)*(x-y) for x,y in zip(vals1, vals2)])

    matchIds = set()
    def findMatch(case_values):
        '''Find the best match of controls for this case'''
        temp = []
        for names, vals in controls:
            temp.append((names, distance(case_values, vals)))
        #from small to large by distance
        temp = sorted(temp, key=lambda x: x[1])
        #print(temp)
        for n, _ in temp:
            if n not in matchIds:
                matchIds.add(n)
                return n

        # all controls were used.
        return ''

    for line in open(P.case_f):
        line = line.strip()
        if line:
            ss = line.split()

            mname = findMatch(list(map(float, ss[1:])))
            if mname:
                sys.stdout.write('%s\t%s\n'%(ss[0], mname))
            else:
                sys.stderr.write('Can not find match for %s, all controls were used, please add more controls!\n'%(ss[0]))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
