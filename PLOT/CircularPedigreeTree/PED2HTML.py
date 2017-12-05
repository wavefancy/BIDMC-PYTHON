#!/usr/bin/env python3

"""

    Convert ped file to circular pedigree figure.
    @Author: wavefancy@gmail.com

    Usage:
        PED2HTML.py
        PED2HTML.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read results from stdin, and output results to stdout.
        2. See example by -f.

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
#input example
------------------------
c1  1
c2  2
c3  5
    ''');

class Node(object):

    def __init__(self, name, children, mateName):
        self.name = name
        self.children = children
        self.mateName = mateName

    def addOneChild(self, childName):
        self.children.append(childName)

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
            ped_data[ss[0]] = ss

    


sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
