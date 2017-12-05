#!/usr/bin/env python3

"""

    Convert ped file to circular pedigree figure.
    @Author: wavefancy@gmail.com

    Usage:
        PED2HTML.py
        PED2HTML.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read sigle family ped file from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format   Show input/output file format example.

"""
import sys
import json
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
#input example
------------------------
c1  1
c2  2
c3  5
    ''');

class Node(object):

    def __init__(self, name):
        self.name = name
        self.children = []
        self.mateName = ''

    def addOneChild(self, childName):
        self.children.append(childName)
    def setMateName(self, name):
        self.mateName = name
    def getMateName(self):
        return self.mateName
    def toMapString(self):
        smap = self.__dict__
        # print(smap)
        if self.children:
            stemp = ''
            for x in self.children:
                stemp += x.toMapString()
            smap['children'] = '[' + stemp + ']'
        else:
            smap.pop('children')
        # print(smap)
        return str(smap).replace("\"",'')

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #read ped file from stdin.
    ped_data = {} #map for name -> raw data.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            ped_data[ss[1]] = ss

    root = '';
    NodeMap = {} #name -> Node
    def checkAddNode(name):
        if name != '0' and name not in NodeMap:
            NodeMap[name] = Node(name)

    JsonMap = {}
    for name,data in ped_data.items():
        #create node
        [checkAddNode(x) for x in data[1:4]]
        #set node children.
        [NodeMap[x].addOneChild(NodeMap[data[1]]) for x in data[2:4] if x != '0']
        #set mating info.
        if data[2] != '0' and data[3] != '0':
            NodeMap[data[2]].setMateName(data[3])
            NodeMap[data[3]].setMateName(data[2])
        elif data[2] == '0' and data[3] == '0':
            pass
        else:
            sys.stderr.write('ERROR: Please set full parent info. Error at: %s\n'%('\t'.join(data)))
            sys.exit(-1)

        #add data to JsonMap
        JsonMap[name] = {
            'name': name,
            'father': data[2],
            'mother': data[3],
            'sex': data[4],
            'affected': data[5]
        }

    #find the root node, and convert results to josn.
    print(ped_data)
    for name,data in ped_data.items():
        if data[2] == '0' and data[3] == '0':
            mateName = NodeMap[name].getMateName()
            if mateName:
                mdata = ped_data[mateName]
                if mdata[2] == '0' and mdata[3] == '0':
                    # print("ROOT NAME:" + name)
                    # Indeed we have two roots, but we chose abitrary one as root.
                    root = NodeMap[name]
                    break

    print(root.toMapString())
    print(JsonMap)
    # j = json.dumps(root.toMapString(), sort_keys=True,indent=4, separators=(',', ': '))
    # sys.stdout.write('%s\n'%(j))


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
