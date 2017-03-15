#!/usr/bin/env python

"""

    Extract a subset of samples from haps/sample format.
    @Author: wavefancy@gmail.com

    Usage:
        HapsSampleSubset.py (-r|-k) --sample sampleFile --subset subset --out-sample outSample [-n]
        HapsSampleSubset.py -h | --help | -v | --version | -f | --format

    Notes:
        Read haps file from stdin and output subseted haps file to stdout.

    Options:
        -h --help                  Show this screen.
        -v --version               Show version.
        -f --format                Show input/output file format example.
        --subset <subset>          File name for ID list file, see example.
                                   *** FamilyName and IndiviudalName,
                                   if -n is on: only read the fist column as indiviudal name.

        --sample <sampleFile>      File name for sample file corresponding to input haps file.
        --out-sample <outSample>   File name for sample file corresponding to output haps file.
        -k                         Keep samples indicated in --out-sample file
        -r                         Remove samples indicated in --out-sample file
        -n                         Only check indiviudal name, default check family name and indiviudal name.

"""
import sys
from docopt import docopt
from signal import signal, SIGPIPE, SIG_DFL

def ShowFormat():
    '''File format example'''
    print('''
    #haps format example: chr rsID pos A0 A1 hap1 hap2 hap1 hap2
        One snp one line, each individual two haps, two columns.
    ------------------------
    11 rs2280544 204062 C T 0 1 1 1 0 1
    11 rs2280544 204062 C T 0 1 1 1 0 0

    #Sample format:
        Two title lines + One individual one line.
        At lease three columns: ID_1 ID_2 missing.
    ------------------------
    ID_1 ID_2 missing father mother sex plink_pheno
    0 0 0 D D D B
    1 23110108 0 0 0 2 -9
    2 23116433 0 0 0 2 -9
    3 23116434 0 0 0 2 -9

    #ID list file.
        No title line, One individual one line.
        At least two columns for ID_1 and ID_2, in order.
    ----------------------------
    2 23116433
    3 23116434
          ''');

if __name__ == '__main__':
    args = docopt(__doc__, version='1.0')
    # print(args)

    if(args['--format']):
        ShowFormat()
        sys.exit(-1)

    idNameOnly = False
    if args['-n']:
        idNameOnly = True  #only check individual name
    #out id list
    ids=set()
    for line in open(args['--subset']):
        line = line.strip()
        if line:
            ss = line.split()
            if idNameOnly:
                ids.add(ss[0])
            else:
                ids.add(ss[0] + ss[1])

    keep = True
    if args['-r']:
        keep = False

    #output id index
    outIDs = []
    index = 0
    subSample = []
    for line in open(args['--sample']):
        line = line.strip()
        if line:
            index += 1
            if index > 2: #skip two title line
                ss = line.split()

                name = ''
                if idNameOnly:
                    name = ss[1]
                else:
                    name = ss[0] + ss[1]

                if keep:
                    if name in ids:
                        outIDs.append(index -3) # 0 based.
                        subSample.append(line)
                else:
                    if name not in ids:
                        outIDs.append(index -3) # 0 based.
                        subSample.append(line)
            else:
                subSample.append(line)

    #output subsamples.
    osub = open(args['--out-sample'], 'w')
    osub.write('%s\n'%('\n'.join(subSample)))
    osub.flush()
    osub.close()

    check=False; #check data integrity.
    for line in sys.stdin:
        line = line.strip()
        if line:
            ss = line.split()
            if check == False:
                check = True
                if len(ss)%2  == 0:
                    sys.stderr.write('Error: number of haplotypes in input should be an even number, please check!\n')
                    sys.stderr.write('Current total number of haplotypes: %d\n'%(len(ss)-5))
                    sys.exit(-1)
                if (len(ss)-5) != (index-2)*2:
                    sys.stderr.write('The number of haplotypes is not equal with 2*the_number_of_samples[--sample].\n')
                    sys.exit(-1)

            out = ss[0:5]
            ss = ss[5:]
            for i in outIDs:
                m = 2*i; n = m +1 # each individual two columns.
                out.append(ss[m])
                out.append(ss[n])

            sys.stdout.write('%s\n'%(' '.join(out)))

sys.stdout.flush()
sys.stdout.close()
sys.stderr.flush()
sys.stderr.close()
