#!/usr/bin/env python3

"""
    Aggregate genehunter results.

    @Author: wavefancy@gmail.com

    Usage:
        GenehunterResults.py <infiles>...
        GenehunterResults.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read sliced results from genehunter.
        2. Read the snp id information from the 'use' command.
        3. Read the linkage results from the 'total stat' conmmand.
        4. If there are overlap between marks, choose the the one with largest LOD score.
        5. ***import*** please set 'off end 0' when perform linkage analysis by genehunter.

    Options:
        -h --help       Show this screen.
        -v --version    Show version.
        -f --format     Show format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE, SIG_DFL)

def ShowFormat():
    '''Input File format example:'''
    print('''
    ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    files = args['<infiles>']

    AllData = []
    #print(files)
    for f in files:
        readMap = False
        readResults = False
        mapData = []
        reData = []
        with open(f,'r') as inf:
            for line in inf:
                line = line.strip()
                if line.startswith('.'):
                    continue
                if line:
                    if line.startswith('Current map'):
                        readMap = True
                        continue
                    if readMap:
                        mapData += line.split()

                    if line.startswith('Totalling pedigrees'):
                        readResults = True
                        continue
                    if line.startswith('file to store postscript plot'):
                        readResults = False
                        break

                    if readResults:
                        reData.append(line)

                else:
                    if readMap:
                        readMap = False
                    if readResults:
                        readResults = False
                        break

        #organize data for this input file.
        if (not mapData) or (not reData):
            sys.stderr.write('ERROR: no data found in file: %s\n'%(f))
            sys.exit(-1)

        #print(mapData)
        #print(reData)
        reData = [x.replace('(','') for x in reData]
        reData = [x.replace(')','') for x in reData]
        reData = [x.replace(',','') for x in reData]
        reData = [x.split() for x in reData]
        mapData = mapData[::2]
        #print(mapData)
        #print(reData)
        #compute step.
        stepSize = int((len(reData)-2)/(len(mapData)-1))
        #print(stepSize)
        fResults = []
        fResults.append(['ID'] + reData[0])
        for i in range(len(mapData)-1):
            j = i*stepSize
            for k in range(stepSize):
                fResults.append([mapData[i] + '_' + str(k)] + reData[j + k + 1]) # +1 for skip title

        #append the last one.
        fResults.append([mapData[-1] + '_0'] + reData[-1])
        if AllData:
            AllData += fResults[1:]
        else:
            AllData = fResults

    #prepare output. keep the best lod score if there are overlap between variants.
    def outElements(d):
        '''Skip the second elements'''
        return [d[0]] + d[2:]
    #output title
    sys.stdout.write('%s\n'%('\t'.join(outElements(AllData[0]))))

    #find the position for NPL_score
    NPL_score_pos = 0
    try:
        NPL_score_pos = AllData[0].index('NPL_score')
    except ValueError:
        sys.stderr.write('Can not find keyword "NPL_score" in title line, please check !\n')
        sys.exit(-1)

    AllData = sorted(AllData[1:], key=lambda x: (int(x[0].split(':')[1]), x[0])) #sort by physical location, then by suffix.
    outData = [AllData[0]]
    for k in AllData[1:]:
        #sys.stdout.write('%s\n'%('\t'.join(k)))
        if k[0] != outData[-1][0]:
            outData.append(k)
        else:
            if float(k[NPL_score_pos]) > float(outData[-1][NPL_score_pos]): # the third column is lod score.
                outData[-1] = k
    #print(AllData)
    for k in outData:
        sys.stdout.write('%s\n'%('\t'.join(outElements(k))))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
