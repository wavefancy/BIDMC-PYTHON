#!/usr/bin/env python3

"""

    Equally divide genome by bed file.
    Divide genome to 'Number' of chucks with equal size.
    Bed file spec.: https://genome.ucsc.edu/FAQ/FAQformat.html#format1
    @Author: wavefancy@gmail.com

    Usage:
        EqualDividGenomeByBed.py -n chuckNumber -o outputNameBase
        EqualDividGenomeByBed.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read genome contig_size from stdin, and output results to files.
        2. See example by -f.

    Options:
        -n chuckNumber     Number of chucks.
        -o outputNameBase  Output
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
    ''');

class P:
    index = 1 #index for file.

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    numOfChuck = int(args['-n'])
    outputBase = args['-o']

    data = [] #[(contigName, [0, contigsize]), (), ....]
    total = 0
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            len = int(ss[1])
            total += len
            data.append((ss[0], [0, len]))

    chuckLen = 0
    if total % numOfChuck == 0:
        chuckLen = total/numOfChuck
    else:
        chuckLen = int(total/(numOfChuck)) + 1
    #print(chuckLen)

    def newOutFile():
        '''creat a output file'''
        oFile = open('%s_a%d_%d.bed'%(outputBase,numOfChuck,P.index), 'w')
        P.index += 1
        return oFile
    outFile = newOutFile()

    c_data = data.pop(0)
    in_index  =  0  #index for contig.
    requireMore = chuckLen
    while True:
        #print('requireMore: %d\n'%(requireMore))
        if c_data[1][1] - c_data[1][0] > requireMore :
            c_data[1][0] += requireMore
            outFile.write('%s\t%d\t%d\n'%(c_data[0], c_data[1][0] - requireMore, c_data[1][0]))

            outFile.flush()
            outFile.close()
            outFile = newOutFile()
            requireMore = chuckLen

        elif c_data[1][1] - c_data[1][0] == requireMore:
            outFile.write('%s\t%d\t%d\n'%(c_data[0], c_data[1][0], c_data[1][1]))
            outFile.flush()
            outFile.close()

            requireMore = chuckLen
            if data:
                c_data = data.pop(0)
                outFile = newOutFile()
            else:
                break

        elif c_data[1][1] - c_data[1][0] < requireMore:
            outFile.write('%s\t%d\t%d\n'%(c_data[0], c_data[1][0], c_data[1][1]))
            requireMore -= (c_data[1][1] - c_data[1][0])

            if data:
                c_data = data.pop(0)
            else:
                outFile.flush()
                outFile.close()
                break

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
