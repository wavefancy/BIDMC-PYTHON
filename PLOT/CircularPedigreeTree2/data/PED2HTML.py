#!/usr/bin/env python3

"""

    Convert ped file to newick format.
    @Author: wavefancy@gmail.com

    Usage:
        PED2HTML.py [--html base_file]
        PED2HTML.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read sigle family ped file from stdin, and output results to stdout.
        2. See example by -f.

    Options:
        --html base_file  html template file, default base.html
        -h --help         Show this screen.
        -v --version      Show version.
        -f --format       Show input/output file format example.

"""
import sys
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

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    basehtml = args['--html'] if args['--html'] else 'base.html'

    from ete3 import Tree,TreeNode
    #read ped file from stdin.
    ped_data = {} #map for name -> raw data.
    node_data = {} #map for name -> TreeNode
    for line in sys.stdin:
        line = line.strip()
        if line and line[0] != '#': #skip comment line.
            ss = line.split()
            ped_data[ss[1]] = ss
            n = TreeNode(name=ss[1])
            n.add_feature('raw',ss)
            node_data[ss[1]] = n

    # for k,v in node_data.items():
    #     print(v.write(format=2,features=['raw']))

    #find the root node, and convert results to josn.
    #Check data integrity.
    m_error = False
    for _, data in ped_data.items():
        if data[2] != '0' and data[2] not in ped_data.keys():
            m_error = True
            sys.stderr.write('ERROR: missing declearation for father: %s\n'%(data[2]) )
        if data[3] != '0' and data[3] not in ped_data.keys():
            m_error = True
            sys.stderr.write('ERROR: missing declearation for mother: %s\n'%(data[3]) )
    if m_error:
        sys.exit(-1)

    T = Tree()
    # def checkAddNode(name):
    #     if name != '0' and name not in NodeMap:
    #         NodeMap[name] = Node(name)

    for name,data in ped_data.items():
        #set node children.
        [node_data[x].add_child(child=node_data[data[1]]) for x in data[2:4] if x != '0']
        #set mating info.
        if data[2] != '0' and data[3] != '0':
            node_data[data[2]].add_feature('mate',node_data[data[3]].raw)
            node_data[data[3]].add_feature('mate',node_data[data[2]].raw)
        elif data[2] == '0' and data[3] == '0':
            pass
        else:
            sys.stderr.write('ERROR: Please set full parent info. Error at: %s\n'%('\t'.join(data)))
            sys.exit(-1)

    # T.add_child(child=node_data['f1'])
    # print(T.write(format=1))
    # for k,v in node_data.items():
    #     print(v.name)
    #     print(v.write(format=2,features=['name','mate']))

    root = ''
    for name,data in ped_data.items():
        if data[2] == '0' and data[3] == '0':
            # mateName = node_data[name]
            if 'mate' in node_data[name].features:
                mdata = node_data[name].mate
                # print(mdata)
                if mdata[2] == '0' and mdata[3] == '0':
                    # print("ROOT NAME:" + name)
                    # Indeed we have two roots, but we chose abitrary one as root.
                    root = node_data[name]
                    break

    # print(root)
    # update node name for output.
    for k,v in node_data.items():
        n = '_'.join(v.raw)
        if 'mate' in v.features:
            n = n + '||' + '_'.join(v.mate)
        v.name = n

    T.add_child(root)
    treeData = T.write(format=1)[:-1] + 'root||root:1;'
    # print(out)

    with open(basehtml,'r') as bf:
        for line in bf:
            line = line.replace('__treeData__',treeData)
            # line = line.replace('__annotation__',annotation)
            sys.stdout.write('%s'%(line))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
