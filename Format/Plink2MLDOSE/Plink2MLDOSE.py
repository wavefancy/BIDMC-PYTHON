#!/usr/bin/env python3

"""
    Conver plink ped/map format to MACH MLDOSE format.
    Usage:
        Plink2MLDOSE.py -m map -s snpinfo -i idfile
        Plink2MLDOSE.py -h | --help | -v | --version | -f | --format

    Notes:
        1. Output MLDOSE file to stdout. Read ped file from stdin.
        2. See example by -f.

    Options:
        -m map         Plink map file.
        -s snpinfo     Output file name for snp information.
        -i idfile      Output file name for individual ids.
        -h --help      Show this screen.
        -v --version   Show version.
        -f --format    Show input/output file format example.
"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) #prevent IOError: [Errno 32] Broken pipe. If pipe closed by 'head'.

def ShowFormat():
    '''Input File format example:'''
    print('''
    1. input: plink PED/MAP file.
    2. output file: ProbABEL manual.
    ''');


if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    #print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    #pedfile = args['-p']
    mapfile = args['-m']
    snpfile = args['-s']
    idfile = args['-i']

    data = [] #snp data file [[oneline], [] ...]
    ids = []  #if list.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            ids.append(ss[1])
            data.append(ss[6:])
    ifile = open(idfile,'w')
    ifile.write('id\n')
    [ifile.write('%s\n'%(x)) for x in ids]
    ifile.flush()
    ifile.close()
    #read map file
    mapdata = [] #snp data file [[oneline], [], ...]
    for line in open(mapfile,'r'):
        line = line.strip()
        if line:
            mapdata.append(line.split())
    #print(mapdata)
    #output mldos file:
    #chr->rsid MLDOSE DOSE for allele 1.
    if len(data[0])%2 != 0:
        sys.stderr.write('ERROR: format error from ped file, genotype columns not in even number.\n')
        sys.exit(status=-1)

    def readAlleles(idIndex):
        '''Read allele set of a genotype locus'''
        aset = set()
        for r in range(len(data)):
            if data[r][2*idIndex] != '0':
                aset.add(data[r][2*idIndex])
            if data[r][2*idIndex+1] != '0':
                aset.add(data[r][2*idIndex+1])
            #if len(aset) == 2:
            #    return list(aset)

        aset = list(aset)
        if len(aset) == 0: #all missing.
            sys.stderr.write('ERROR: all data were missing at marker %d, 0 based index.\n'%(idIndex))
            sys.exit(-1)
        if len(aset) == 1: #not a polymorphim site here.
            aset.append('N')
        elif len(aset) > 2:
            sys.stderr.write('ERROR: not a biallelic site for marker %d: %s, 0 based index.\n'%(idIndex, '-'.join(aset)))
            sys.exit(-1)

        return aset

    sfile = open(snpfile, 'w')
    sfile.write('SNP AL1 AL2 Freq1 MAF Quality Rsq\n')
    #mldose output.
    out = []
    for i in range(len(ids)):
        y = ['%d->%s'%(i+1,ids[i]),'MLDOSE']
        out.append(y)

    #print(int(len(data[0])/2))
    for i in range(int(len(data[0])/2)): #marker level.
        allels = readAlleles(i)
        #sys.stdout.write('%s->%s\tMLDOSE'%(mapdata[i][0], mapdata[i][1]))

        tcount = 0 # allele 1 count.
        idcount = 0 #number of indiviudals.
        for r in range(len(data)): #individual level.
            dose = ''
            idcount += 1
            # try:
            if data[r][2*i] == data[r][2*i +1]:
                if data[r][2*i] == allels[0]:
                    dose = '2'
                    tcount += 2
                elif data[r][2*i] == allels[1]:
                    dose = '0'
                else: #0
                    dose = 'NaN'
                    idcount -= 1
            else:
                dose = '1'
                tcount += 1
            out[r].append(dose)
            #sys.stdout.write('\t%s'%(dose))
            # except IndexError:
            #     sys.stderr.write('%s--%d--%d--%d\n'%(str(allels),r, 2*i, len(data[r])))
            #     sys.exit(-1)

        #sys.stdout.write('\n')
        #output snpinfo file.
        af = tcount/(2.0 * idcount)
        maf = min(af, 1-af)
        sfile.write('%s %s %.4f %.4f 1 1\n'%(mapdata[i][1], ' '.join(allels),af, maf))

    #output mldose file.
    for x in out:
        sys.stdout.write('%s\n'%(' '.join(x)))

    #close open files.
    sfile.flush()
    sfile.close()

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
