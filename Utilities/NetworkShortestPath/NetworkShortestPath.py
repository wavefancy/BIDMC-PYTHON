#!/usr/bin/env python3

"""

    Calculate the shortest path between gene set on network.
    Sum{min[Shortest_path(gene_i, known_gene)]}
    :
    1. Check the shortest path of gene_i with all known gene,
        and pick up the minimal one as m_i.
    2. Take the sum of m_i, i interate of all genes in input set.


    @Author: wavefancy@gmail.com

    Usage:
        NetworkShortestPath.py -k file (-i file | -r int [-b int])
        NetworkShortestPath.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read network structure from stdin, and output results to stdout.

    Options:
        -k file       Gene list for known genes, line by line, each line two genes as edge.
        -i file       Gene list for checking shortest distance with known gene.
        -r int        Randomly pick up 'int' number of genes and checking the shortest distance with known gene.
        -b int        Bootstrap the random pick process 'int' number of times, default 1.
        -h --help     Show this screen.
        -v --version  Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
# input network without weight
-------------------------------------------
A   B
A   C
C   D

# input network with weight
-------------------------------------------
A   B   10
A   C   1
C   D   2
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)
    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    kfile = args['-k']
    ifile = ''
    if args['-i']:
        ifile = args['-i']

    rPickNumber = ''
    if args['-r']:
        rPickNumber = int(args['-r'])

    BootstrapNumber = 1
    if args['-b']:
        BootstrapNumber = int(args['-b'])

    #read known gene set.
    knownGenes = set()
    with open(kfile,'r') as rkfile:
        for line in rkfile:
            line = line.strip()
            if line:
                knownGenes.add(line)

    #read network structure.
    withWeight = False
    check = True
    import networkx as nx
    G = nx.Graph()
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if check:
                check = False
                if len(ss) == 3:
                    G.add_edge(ss[0], ss[1], weight=float(ss[2]))
                    withWeight = True
                else:
                    G.add_edge(ss[0], ss[1])
                    withWeight = False
            else:
                if withWeight:
                    G.add_edge(ss[0], ss[1], weight=float(ss[2]))
                else:
                    G.add_edge(ss[0], ss[1])
            #G.add_edge(ss[0], ss[1])

    #print(G.edges())
    #print(G.is_directed())
    #print(nx.shortest_path_length(G,i,j,weight='weight'))
    #check all known genes actually in network.
    netwrokGeness = set(G.nodes())
    diff = knownGenes.difference(netwrokGeness)
    if diff:
        sys.stderr.write('ERROR: below known genes can not be found in network:\n')
        for x in diff:
            sys.stderr.write('%s\n'%(x))

    inGenes = set()
    if ifile:
        with open(ifile,'r') as rifile:
            for line in rifile:
                line = line.strip()
                if line:
                    inGenes.add(line)

        diff = inGenes.difference(netwrokGeness)
        if diff:
            sys.stderr.write('ERROR: below input genes can not be found in network:\n')
            for x in diff:
                sys.stderr.write('%s\n'%(x))

    #checking the sum of shortest path.
    def sumOfShortestPath(igenes, kgenes, network):
        '''
            Checking the shortest path of each igenes with all kgenes, and pick the
            minimal one is m_i. Take the sum of m_i, i iterate all igenes.
        '''
        m_i = []
        for i in igenes:
            if withWeight:
                m_i.append(min([nx.shortest_path_length(network,i,j,weight='weight') for j in kgenes]))
            else:
                m_i.append(min([nx.shortest_path_length(network,i,j) for j in kgenes]))

        return sum(m_i)

    if ifile:
        sys.stdout.write('%d\n'%(sumOfShortestPath(inGenes, knownGenes, G)))
        sys.exit(-1)

    #output results
    #remove known genes when bootstrap.
    bootGeneList = [x for x in G.nodes() if x not in knownGenes]
    if rPickNumber:
        import random
        for i in range(BootstrapNumber):
            inGenes = random.sample(bootGeneList, rPickNumber)
            sys.stdout.write('%d\n'%(sumOfShortestPath(inGenes, knownGenes, G)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
