#!/usr/bin/env python

'''
    HapmixResultsSummary

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Algorithms:

'''
import sys
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def help():
    sys.stderr.write('''
    -------------------------------------
    HapmixResultsSummary
    -------------------------------------

    @Author: wavefancy@gmail.com
    @Version: 1.0

    @Usages:
    Para1: [1], output switch actin, see note below.
    Para2: name list file.

    @Notes:
    1. Get the summary results from hapmix output[LOCAL_ANC, PROB model].
    2. Read name list from para2, and output results to stdout according to para1.
    3. Para1 action:
        1: output POP1 expected proportion to stdout sum(2*col1 + 1*col2)/(2N).
        2: output site level expected POP1 copies(2*col1 + 1*col2), one individual one column,
           ordered by the input file name[Para2].
        3: output the most likely ancestry for each individual at each sites,
           0/1/2 copy of POP1 alleles. Each person one column.
        4: output the aggregation of hapmix output.
           Each person three columns, order as input files, Probabilities of 2/1/0 copy of pop1 ancestry.

    -------------------------------------
    \n''')
    sys.stderr.close()
    sys.exit(-1)

class P(object):
    actionMap = {'1':'POP1EPROPORTION', '2' : 'SITELEVELPOP1EPROPORTION', '3': 'MOSTLIKEANCESTRY', '4': 'HAPMIXOUT'}
    action = ''
    flist = ''

if __name__ == '__main__':
    if len(sys.argv) != 3:
        help()

    if sys.argv[1] not in P.actionMap.keys():
        sys.stderr.write('*** Please set proper action in Para1\n')
        help()
    else:
        P.action = P.actionMap[sys.argv[1]]
    P.flist = sys.argv[2]


    def readLOCAL_ANC_PROBFile(fname):
        '''Read results from LOCAL_ANC_PROB file, 3 colums, 2/1/0 Copy of Pop1'''
        resluts = ([],[],[]) # [[column1 list],[ column2 list],[column3 list]]
        for line in open(fname):
            line = line.strip()
            if line:
                ss = line.split()
                for i,v in enumerate(resluts):
                    v.append(float(ss[i]))

        return resluts

    def getSiteLevelPOP1Proportion():
        '''Site level pop1 expected proportion.'''
        indE = [] #[[individual expected proportion],[]]
        fileList = [] #input file name list.
        for fn in open(P.flist):
            fn = fn.strip()
            fileList.append(fn)
            rr = readLOCAL_ANC_PROBFile(fn)
            ie = []
            for i in range(0, len(rr[0])):
                ie.append(2* rr[0][i] + rr[1][i])

            indE.append(ie)

        #check file content length.
        for i in range(1, len(indE)):
            if len(indE[0]) != len(indE[i]):
                sys.stderr.write('ERROR: file: "%s" has different line numbers with the first input file: "%s"\n'%(fileList[i], fileList[0]))
                sys.exit(-1)

        return indE

    def checkContect(matrix, fileList):
        '''Check data integrity of each file.'''
        indE = matrix
        #check file content length.
        for i in range(1, len(indE)):
            if len(indE[0]) != len(indE[i]):
                sys.stderr.write('ERROR: file: "%s" has different line numbers with the first input file: "%s"\n'%(fileList[i], fileList[0]))
                sys.exit(-1)

    def checkContect2(matrix, fileList):
        '''Check data integrity of each file.'''
        indE = matrix
        #check file content length.
        for i in range(1, len(indE)):
            if len(indE[0][0]) != len(indE[i][0]): #different here.#
                sys.stderr.write('ERROR: file: "%s" has different line numbers with the first input file: "%s"\n'%(fileList[i], fileList[0]))
                sys.exit(-1)


    if P.action == 'POP1EPROPORTION':
        indE = getSiteLevelPOP1Proportion()

        for c in range(0, len(indE[0])):
            total = 0
            for v in indE:
                total += v[c]
            total = total/(2.0 * len(indE))
            sys.stdout.write('%.4e\n'%(total))

    elif P.action == 'SITELEVELPOP1EPROPORTION':
        indE = getSiteLevelPOP1Proportion()

        for c in range(0, len(indE[0])):
            out = []
            for v in indE:
                out.append( '%.4f'%(v[c]) )

            sys.stdout.write('%s\n'%('\t'.join(out)))

    elif P.action == 'MOSTLIKEANCESTRY':
        maxAncestry = [] #[[individual most likely ancestry],[]]
        fileList = [] #input file name list.
        for fn in open(P.flist):
            fn = fn.strip()
            fileList.append(fn)
            rr = readLOCAL_ANC_PROBFile(fn)
            ie = []
            for i in range(0, len(rr[0])):
                tt = (rr[0][i], rr[1][i], rr[2][i])
                pos = tt.index(max(tt))
                ie.append(2-pos)

            maxAncestry.append(ie)

        checkContect(maxAncestry, fileList)
        #output results.
        for c in range(0, len(maxAncestry[0])):
            out = []
            for v in maxAncestry:
                out.append( '%d'%(v[c]) )

            sys.stdout.write('%s\n'%('\t'.join(out)))

    elif P.action == 'HAPMIXOUT': #aggregation of hapmix output.
        Ancestry = [] #[[individual Probabilities of 2/1/0 copy of pop1 ancestry],[]]
        fileList = [] #input file name list.
        for fn in open(P.flist):
            fn = fn.strip()
            fileList.append(fn)
            rr = readLOCAL_ANC_PROBFile(fn)
            ie = []
            Ancestry.append(rr)

        checkContect2(Ancestry, fileList)
        #print(Ancestry[0][0])
        #output results.
        for c in range(0, len(Ancestry[0][0])):
            out = []
            for v in Ancestry:
                for x in v:
                    out.append( '%.3f'%(x[c]) )

            sys.stdout.write('%s\n'%('\t'.join(out)))


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
