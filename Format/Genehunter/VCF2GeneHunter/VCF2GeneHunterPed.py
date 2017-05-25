#!/usr/bin/env python3

"""

    Convert VCF to genehunter ped format.

    @Author: wavefancy@gmail.com

    Usage:
        VCF2GeneHunterPed.py -p pedfile
        VCF2GeneHunterPed.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Read vcf file from stdin, output to stdout.
        2. Ref allele code as 1, alt allele code as 2.
        3. Only read the first 6 colummns of ped file.
        4. Output results to stdout.

    Options:
        -p pedfile      input ped file.
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

    #load ped array.
    from collections import OrderedDict
    pedArrayMap = OrderedDict() # idname -> ped array.
    with open(args['-p'], 'r') as pf:
        for line in pf:
            line = line.strip()
            if line:
                ss = line.split()
                pedArrayMap[ss[1]] = ss[0:6]

    genoCol = 9 # 0 based.
    #read vcf from stdin
    content = [] #fist line idname, after genotype.
    missing = '0 0' #missing allele code as 0.
    output = False
    for line in sys.stdin:
        line = line.strip()
        if line:
            if output:
                #output results.
                ss = line.split()
                out = []
                for x in ss[genoCol:]:
                    if x[0] == '.':
                        out.append(missing)
                        continue
                    temp = ''
                    if x[0] == '0': #ref code as 1.
                        temp = '1 '
                    else:
                        temp = '2 ' #alt code as 2.

                    if x[2] == '0':
                        temp += '1'
                    else:
                        temp += '2'
                    out.append(temp)

                content.append(out)

            else:
                if line.startswith('##'):
                    pass
                    #sys.stdout.write('%s\n'%(line))
                elif line.startswith('#C') or line.startswith('#c'):
                    output = True
                    ss = line.split()
                    content.append(ss[genoCol:])

    #print(content)
    #output for typed individluas.
    typed = set()
    for i in range(len(content[0])):
        out = pedArrayMap[content[0][i]]
        typed.add(content[0][i])

        for row in range(1,len(content)):
            out.append(content[row][i])

        sys.stdout.write('%s\n'%('\t'.join(out)))

    #output untyped individluas
    for x in pedArrayMap.keys():
        if x not in typed:
            out = pedArrayMap[x]

            for row in range(1,len(content)):
                out.append('0 0')

            sys.stdout.write('%s\n'%('\t'.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
