#!/usr/bin/env python3

"""

    Clean pedigree, output minimal pedigree which connecting marked(sequenced) individuals.
    @Author: wavefancy@gmail.com

    Usage:
        PedigreeClean.py
        PedigreeClean.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read ped from stdin, and output results to stdout.
        2. Add fake individual if necessay to complete the pedigree.
        3. See example by -f.

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
    #ped file + one more column for indicating marked or not, 0/1.
    ------------------------
S29     S27     S29A    S29B    2       2   1
S29     S28     0       0       1       2   0
S29     S29A    0       0       1       1   0
S29     S29B    0       0       2       1   0
S29     S29     S29A    S29B    2       2   1

    #output:
    ------------------------
S29     S27     S29A    S29B    2       2       1
S29     S29     S29A    S29B    2       2       1
S29     S29B    0       0       2       1       0
S29     S29A    0       0       1       1       0
    ''');

class Node(object):

    def __init__(self, name, father, mother, rawData):
        self.name = name
        self.father = father
        self.mother = mother
        self.visit = 0
        self.rawData = rawData

    def addOneVisit(self):
        self.visit += 1

    def getVisitTimes(self):
        return self.visit

    def getFather(self):
        return self.father
    def getMother(self):
        return self.mother
    def getName(self):
        return self.name
    def getRawData(self):
        return self.rawData

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    colSeq = 7-1 #column index for indicating sequenced or not. 0/1, 1 for sequenced.

    #data = []
    dataMap = {}
    familyName = ''
    for line in sys.stdin:
        line = line.strip()
        if line:
            #data.append(line.split())
            ss = line.split()
            dataMap[ss[1]] = ss
            if not familyName:
                familyName = ss[0]

    #sort data, first creat parental and isolated node.
    #data = sorted(data, key=lambda x: (x[2],x[3]))

    #creat nodes
    nodeMap = {} #name -> nodeClass.
    matingPair = {} # marrage pair.
    def createNewNode(idname, sex='1'):
        '''creat new nodes, if necessay create recussively.'''
        if idname in nodeMap:
            return nodeMap[idname]
        else:
            ss = dataMap.get(idname)
            if ss:
                name = idname
                if ss[2] != '0':
                    father = createNewNode(ss[2], '1')
                else:
                    raw = [ss[0], name+'F', '0', '0', '1', '0', '0']
                    father = Node(name+'F', None, None, raw)
                    nodeMap[name+'F'] = father
                if ss[3] != '0':
                    mother = createNewNode(ss[3], '2')
                else:
                    raw = [ss[0], name+'M', '0', '0', '2', '0', '0']
                    mother = Node(name+'M', None, None, raw)
                    nodeMap[name+'M'] = mother

                matingPair[father.getName()] = mother.getName()
                matingPair[mother.getName()] = father.getName()
                n = Node(name, father, mother,ss)
                nodeMap[name] = n
                return n
            else:
                raw = [familyName, idname, '0', '0', sex, '0', '0']
                n = Node(idname, None, None,raw)
                nodeMap[idname] = n
                return n

    for x in dataMap.keys():
        createNewNode(x)

    # print(nodeMap.keys())
    # [print(x.getRawData()) for k,x in nodeMap.items()]

    #Count visit.
    countlist = []
    outpulist = []
    for x in dataMap.keys():
        if dataMap[x][colSeq] == '1':
            countlist.append(nodeMap.get(x))
            outpulist.append(nodeMap.get(x))

    # print(countlist)
    # [print(x.getRawData()) for x in countlist]
    #count vist number.
    maxVisitTimes = 0
    while(countlist):
        x = countlist.pop(0)
        x.addOneVisit()
        if x.getVisitTimes() > maxVisitTimes:
            maxVisitTimes = x.getVisitTimes()

        if not (x.getMother() is None):
            countlist.append(x.getMother())
        if not (x.getFather() is None):
            countlist.append(x.getFather())

    #output results.
    # fix if only one sequenced individual in a family.
    if maxVisitTimes ==1:
        sys.stderr.write('Error: only one marked(sequenced) individual in input family: %s, please check, at least two !!!\n'%(familyName))
        sys.exit(-1)

    outed = set()
    #print(maxVisitTimes)
    while(outpulist):
        #print([x.getName() + '-' + str(x.getVisitTimes()) for x in outpulist])
        x = outpulist.pop(0)
        if x in outed or x.getVisitTimes() == 0:
            continue
        #print('here')
        if matingPair.get(x.getName()) and (matingPair[x.getName()][-1] == 'F' or matingPair[x.getName()][-1] == 'M') and x.getVisitTimes() < maxVisitTimes and x.getName() not in dataMap:
            continue

        #print('here2')
        outed.add(x)
        #print([x.getName() + '-' + str(x.getVisitTimes()) for x in outed])
        if x.getVisitTimes() < maxVisitTimes:
            if x.getMother():
                outpulist.append(x.getMother())
            if x.getFather():
                outpulist.append(x.getFather())

        #update output data
        out = x.getRawData()
        if out[2] == '0' and x.getFather() and  x.getVisitTimes() < maxVisitTimes:
            out[2] = x.getFather().getName()
        if out[3] == '0' and x.getMother() and x.getVisitTimes() < maxVisitTimes:
            out[3] = x.getMother().getName()
        sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
